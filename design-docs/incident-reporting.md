# Incident Reporting Agent

A conversational agent that walks a practitioner through filing a clinical
incident report, grounded in the facility's **own policies** (retrieved with
RAG). It gathers the basics, autonomously discovers every relevant policy, then
works through the contributing factors and the policy-required actions — recording
each with a citation to the exact policy text that grounds it.

## Architecture at a glance

- **Policy corpus → RAG.** Policy PDFs are ingested (PDF → markdown + metadata via
  one LLM call → markdown-aware chunks → embeddings) into a `policy_chunks` table
  in Postgres/pgvector. `PolicyService` does the vector retrieval. See the
  ingestion pipeline in `CareAI/ingestion/` and the store in `CareAI/database/`.
- **Agent.** A semi-structured LangGraph with four fixed stages; the reasoning
  *within* each stage is the LLM's (`CareAI/agents/reporting/`).
- **API.** FastAPI: a reporting router (chat + SSE stream + state) and a policies
  router (upload + list), behind a shared `X-API-Key` and CORS
  (`CareAI/api/`).
- **UI.** A thin Streamlit client that streams the agent over SSE and renders the
  report-so-far (`CareAI/ui/`).

## Design principle

The LLM drives the conversation and the reasoning within each stage. The
**structure** (the stages) and the **safety-critical checks** (grounding and
completeness) are deterministic code, not prompt promises:

- **Grounding is enforced in code.** Every citation must name a policy that was
  actually added to the grounding set *and* a chunk index that exists in it.
  `_validate_links` rejects anything else and enriches valid citations with the
  chunk's text, so each stored item carries its exact grounding for review.
- **Completeness is a deterministic gate.** Intake can only finish once **every
  `action` item in the intake plan has been assessed** — i.e. each has a recorded
  action referencing its id (`finish_report` checks `unmet_action_items`). The
  agent's own policy selection drives the plan, and the plan defines "done"; the
  code enforces it. Gating on distinct *requirements* rather than per added policy
  means over-discovering several overlapping policies no longer forces a redundant
  per-policy action question. This recovers a deterministic completeness signal
  without a per-incident-type schema.
- **Actions carry a disposition.** Each policy-required action is classified
  `done_correctly` / `omission` / `commission` (the omission/commission framing
  from clinical root-cause analysis). Omissions and commissions *are* the
  procedure gaps a reviewer and the manager view care about.

We deliberately did **not** build a per-incident-type field/severity config —
policies are the single source of truth, and duplicating them into hand-authored
config invites drift. Parsing a deterministic schema *out of* the policies offline
remains a future consideration (`future-considerations.md`).

## The four stages

The stage is tracked in `ReportingState.phase`, so a new user message resumes the
right stage and a tool loop returns to the stage it came from.

1. **basics** — `extract_basics` pulls the header fields out of the conversation
   (incident type, when, where, a one-line summary, people involved).
   `ask_basics` asks for whatever is still missing in **one combined question**.
   These basics are a fixed, universal set — every report has them — not a
   per-type schema.
2. **discover** — an **autonomous, reasoned policy loop** with no practitioner
   involvement. It searches the policy library, adds every relevant policy, and
   follows the threads *between* policies (a needlestick → sharps handling →
   bloodborne-pathogen exposure → employee-health timelines) until further
   searches surface nothing new. Capped at N rounds so it can't run away.
3. **factors** — a grounded Q&A loop: *why* did it happen? Confounding/
   contributing factors are recorded (optionally cited to a policy chunk when the
   factor is a deviation from a standard). It may re-search and add policies if a
   new facet appears, and ends by calling `advance_to_actions`. Its questioning
   emphasis is the "why", but if the practitioner volunteers an action and whether
   it was done, it records that action right then rather than deferring it.
4. **actions** — a grounded Q&A loop, requirement by requirement: what action each
   plan item requires and whether it was done, recorded with a **disposition** and
   a chunk citation (and it still records a contributing factor if a new one
   surfaces). `finish_report` gates on every plan `action` item being assessed;
   then `wrap_up` emits a deterministic markdown summary.

Between **discover** and **factors**, a transition node drafts the **intake
plan**: it reads the full text of the added policies and produces the concrete
factor probes and action checks to work through. The plan **consolidates across
policies** — a requirement shared by several policies becomes one item citing all
of them (`PlanItem.policy_ids`), so each distinct thing is asked once, not once
per policy. Each item gets a stable id (`factor-1`, `action-2`, assigned in code);
the recording tools mark an item addressed via their `satisfies` argument, so the
deep-dive loops ask only what is still outstanding and never re-ask a settled
item. The plan stays internal — it steers the factors/actions prompts and is not
shown to the practitioner.

## Grounding model (the heart of it)

- `search_policies(query)` → candidate **chunks**, each labelled with its
  `policy_id` and `chunk_index`.
- `add_policy(policy_id)` → adds that policy (and all its chunks) to the grounding
  set. Only added policies may be cited.
- `record_action` / `record_contributing_factor` cite a `PolicyLink`
  (`policy_id` + `chunk` index + `reason`). The code checks the chunk exists in an
  added policy and attaches its text; invalid citations are rejected with the list
  of valid chunk indices. Each record also carries a `satisfies` list naming the
  plan item id(s) it addresses — that is what the completeness gate counts and what
  lets the loops drop settled items.

## Tools

`search_policies`, `add_policy`, `search_incidents` (de-identified precedent,
currently a mock), `record_report_info`, `record_contributing_factor`,
`record_action`, `advance_to_actions`, `finish_report`. Each stage is bound the
tools it should use, and a shared `ToolNode` executes whichever was called. Both
deep-dive stages are bound **both** record tools (`record_contributing_factor`
*and* `record_action`): the stage sets the questioning emphasis via its prompt,
but either can capture whatever the practitioner volunteers to the bucket it
belongs in — so an action mentioned mid-factors isn't dropped or re-asked later.

## The report

`IncidentReport` = header (`incident_type`, `occurred_at`, `location`, `summary`,
`people`), `actions_taken` (each `{description, disposition, related_policies}`),
and `contributing_factors` — each recorded item carrying its own
`related_policies` chunk citations (with the cited chunk's text enriched in).
There is no separate top-level policy set: the grounding travels with the items
that cite it. `report_id` / `reporter_id` / `reported_at` are system-set. Once
intake finishes, the **escalation agent** populates `severity` + `escalation`
(see *Escalation* below); `status` is still unused.

## Escalation (severity)

Severity is **not** a scale we impose — the facility's policies define it, so the
escalation agent reads it out of them. The moment a thread finalizes
(`_persist_if_done`), the finalized `IncidentReport` is saved and then handed to a
small, **self-contained** LangGraph subagent (`CareAI/agents/escalation/`,
`gather` → `assess`).

**It starts from a fresh context.** The route hands the subagent *only* the
finalized report dict — never the reporting conversation. Its state has no
`messages` channel and it compiles with no checkpointer, so the intake chat
cannot leak in and nothing persists between runs; it rebuilds its own two-message
prompt from scratch every time. (Pinned by
`tests/agents/escalation/test_isolation.py`.)

**The policies are re-fetched, not passed through.** The report carries only the
chunks cited by each recorded item, not the full grounding set — so the subagent
retrieves what it needs itself:

- **gather** reads the policy ids cited across the report's actions and factors
  (`_cited_policy_ids`) to learn *which* policies are relevant, then refetches the
  *full* text of each via `PolicyService.get` — not just the cited chunks — so a
  policy's "Severity & Reporting" table is in view even if intake never cited it.
- **assess** makes one grounded, structured-output call. It finds the severity
  criteria the policies specify (per-policy tables, plus the facility-wide scale
  they reference — e.g. `SEV-1…SEV-3` / Near Miss in `POL-RM-013`), matches the
  incident against them, and returns an `EscalationAssessment`:
  `severity` (the policy's own label, or `null` when the policies define no
  applicable criteria → human triage), a `rationale`, and `sources` (chunk
  citations, same `PolicyLink` shape used throughout).

It is **best-effort and off the finalization critical path**: the report is saved
first, severity is attached in a second upsert, and an assessment failure is
logged and leaves the finalized report intact (without a severity).

> **Relevance travels via citations.** The subagent only sees policies that some
> recorded action/factor cites. Today the completeness gate ties every plan
> `action` item to a recorded (and therefore cited) action, so by the time intake
> finishes every relevant policy is cited. If a future change let an
> added-but-uncited policy survive to finalization, it would be invisible here —
> making the handover explicit (a `policy_ids` field set on the report in
> `from_graph_state`) would close that gap.

## Flow

```mermaid
graph TD
    classDef stage fill:#0F766E,stroke:#0D9488,color:#FFFFFF,stroke-width:2px
    classDef io fill:#1E293B,stroke:#0F172A,color:#FFFFFF,stroke-width:2px
    classDef store fill:#374151,stroke:#4B5563,color:#FFFFFF,stroke-width:2px

    START([New or resumed message]):::io
    WAIT([Ask the user · pause thread]):::io
    WRAP([wrap_up · markdown summary]):::io
    POL[(policy_chunks · pgvector)]:::store

    START -->|enters at the saved phase| basics

    subgraph PIPE [Four fixed stages]
        direction TB
        basics["① basics<br/>extract header fields"]:::stage
        discover["② discover<br/>autonomous policy loop"]:::stage
        factors["③ factors<br/>grounded Q&A · why?"]:::stage
        actions["④ actions<br/>grounded Q&A · per policy"]:::stage

        basics -->|complete| discover
        discover -->|no new policies| factors
        factors -->|advance_to_actions| actions
    end

    basics -. missing fields .-> WAIT
    factors -. ask a question .-> WAIT
    actions -. ask a question .-> WAIT
    actions -->|finish_report · all action items assessed| WRAP

    discover <-. search / add .-> POL
    factors  <-. search / add .-> POL
    actions  <-. search / add .-> POL

    WRAP --> SAVE[(incident_reports · finalized)]:::store
    SAVE -->|hand over report only| ESC["escalation subagent<br/>gather → assess · fresh context"]:::stage
    ESC -. refetch cited policies .-> POL
    ESC -->|severity + rationale| SAVE
```

## API

All `/api/v1/*` routes require a valid `X-API-Key`; `/health` is unauthenticated.

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/reporting/threads/{id}/messages` | Send a message, get the full reply |
| POST | `/api/v1/reporting/threads/{id}/stream` | SSE: `token` / `tool` / `done` events |
| GET  | `/api/v1/reporting/threads/{id}` | The report collected so far |
| POST | `/api/v1/policies/upload` | Upload PDF(s); ingested concurrently |
| GET  | `/api/v1/policies` | List ingested policies |

The SSE stream emits incremental `token` text from the user-facing stages, plus
**human-readable `tool`** events ("Searching policies for '…'", "Adding policy
POL-EH-001") so the UI can show what the agent is doing — especially during the
otherwise-silent discovery stage.

## Built vs. planned

**Built:** policy ingestion + pgvector RAG; the four-stage agent; code-enforced
chunk grounding; action dispositions; the deterministic completeness gate; the
policy-grounded **escalation (severity) agent**; the reporting + policies API with
API-key auth, CORS, and SSE streaming; the Streamlit UI.

**Planned / not yet built:**

- **Role-based access** (employee sees own reports; manager sees all, plus past
  incidents and procedure gaps) — enforced at the store layer, not the prompt.
- **Escalation routing** — notifications & deadlines drafted from the cited
  policy prose, building on the severity the escalation agent now assigns.
- **Review pass** — deterministic checks (Pydantic validity, every citation points
  at a real chunk — already enforced at record time) plus one LLM pass (narrative
  vs. recorded data, policy conflicts) that decides when a human must review.
- **Notifications & deadlines** extracted from the cited policy prose and drafted.
- **Audit logging** (append-only who/what/when, identifiers only — no PHI).
- **Past-incident RAG** — `search_incidents` is a mock today; the real
  de-identified corpus is a separate feature.

## Open questions

- **De-identification for the incidents corpus.** Deterministic PII stripping
  (regex/NER) vs. an LLM redaction pass, when past-incident RAG lands.
- **Do we need severity at all** given the omission/commission dispositions, or is
  severity better derived from the dispositions + policy deadlines?
- **Discovery cap tuning.** Is a fixed round cap right, or should discovery stop on
  a "no new policies" signal with the cap only as a backstop?
- **Abandoned / partial intake.** A thread can stop mid-flow; how does a partial
  report get surfaced for human follow-up?
- **Human review outcome.** Approve/reject only, or edit-and-re-check — and does an
  edit re-enter review?
