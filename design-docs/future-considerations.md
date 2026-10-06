# Future Considerations

Things I've deliberately deferred to keep the first cut focused. These are the
improvements I'd want to come back to once the core agents are working.

## Collection Agent

### Parse a deterministic schema out of the facility's policies

Right now completeness and severity are LLM judgments grounded in retrieved
policy. I dropped the idea of a hand-authored incident config (per-type required
fields + severity rules) because it duplicates what's already written in the
policies, and two sources of truth drift apart.

But I still want the determinism — "all required fields present" as a set check,
"severity = rule table" as pure logic — without asking a facility to author and
maintain a second artifact by hand. So the plan is to **derive the structured
schema from the policies themselves, offline:**

- An offline job reads each facility's policy corpus and extracts, per incident
  type, the required fields and the severity criteria into a typed structure
  (the `IncidentConfig` I sketched earlier). This is an LLM extraction step, but
  it runs **offline and is human-reviewed** before it's ever used — the LLM never
  touches the live completeness/severity path.
- The parsed schema is **versioned and pinned to a policy version**. When the
  policies change, the extraction re-runs and a human re-approves the diff, so the
  schema can't silently drift from the prose it came from.
- At runtime the agent uses the approved schema for deterministic gates, and still
  cites the underlying policy for grounding. Best of both: author once (the
  policy), get a deterministic gate (the parsed schema).

This gives us back the original "LLM out of the safety path" principle without the
double-authoring cost that made me drop the config in the first place. It's a
bigger lift (extraction quality, review tooling, versioning), which is why it's
here and not in the first build.

### Link actions to the people involved

Right now an `ActionTaken` links only to the policies that required it. I'd like
each action to also reference the people it involved — who performed it, who was
notified, who witnessed it. That turns the report into a proper audit graph:
"show me every action involving staff member X," or "which notifications went to
the physician."

The catch is the same lesson `add_policy` taught me: linking by name is fragile
(typos, "Dr. Patel" vs "the cardiologist"), so this only works once people are
first-class, id'd entities rather than the flat `people` list they are today. The
plan:

- **Known issue — people tracking is lossy today.** People are a flat `list[dict]`
  de-duped by exact `(name, role)` in the `add_people` reducer, so "Dr. Patel",
  "Patel, MD", and "the cardiologist" land as three separate entries and a patient
  who is also a witness can split across roles. There's no entity resolution, so
  the `people` list overcounts and can't be reliably linked against. Fixing this is
  the prerequisite for everything below.
- Give each `Person` a stable id and register them the way policies get added, so
  there's an authoritative set to link against.
- Add `related_people: list[str]` to `ActionTaken`, validated against that set in
  `record_action` — same rejection pattern as unknown policy ids.
- Mind the PHI split: patients are PHI, staff/witnesses are workforce data. The
  `role` field already distinguishes them; the de-identification layer should key
  off it.

I deferred this because nothing consumes the linkage yet — it pays off when the
manager view lands and wants to query the report as a graph.

### Back `search_incidents` with a real precedent store

The agent already calls `search_incidents` to shape sharper questions, but the
tool is a stub today: a hardcoded `_INCIDENTS` list in `tools.py`, matched by an
exact `incident_type` equality filter and sorted. It proves the *shape* of the
feature — de-identified precedent feeding the questioning, never surfaced to the
practitioner — without any real retrieval behind it.

The plan is to make it a proper vector store, mirroring what `policy_chunks` and
`PolicyService` already do for policies:

- A new `incident_summaries` table in Postgres, with a pgvector `embedding`
  column (same `text-embedding-3-small` / 1536-dim setup as `PolicyChunk`) and an
  `IncidentService.search(query, k)` doing cosine-distance retrieval. The agent
  then searches by *semantic similarity* to the incident at hand, not by an exact
  type string — "unwitnessed fall in an anticoagulated patient" should surface the
  anticoagulation precedent even when the type labels differ.
- **PII/PHI scrubbing happens before the summary is ever embedded**, not at read
  time. When a report is finalized, an offline step de-identifies its summary
  (the same de-identification layer the report export needs) and only the scrubbed
  text is embedded and stored. That keeps the raw precedent out of the vector store
  entirely — the "never surface to the practitioner" rule in the prompt becomes a
  property of the data, not just an instruction to the model.
- Wire the tool to the service through the same dependency/`by_name` path the
  policy tools use, so the in-memory stub drops out cleanly.

I deferred the real store because the stub is enough to exercise the prompt's
"precedent for question-shaping only" behavior, and the scrubbing pipeline is a
dependency it shares with the manager-facing export — better to build both against
one de-identification layer than to grow a throwaway one here.

### Tighten the factor/action prompts to cut redundancy and warm the tone

The `factors` and `actions` phases still occasionally ask overlapping questions —
the same underlying fact probed once as a contributing factor and again as an
action — despite the `FACTOR_VS_ACTION` boundary and the "check the recorded
factors and actions before asking" guidance already in both prompts. The current
defenses are mostly *instructional* ("never ask the same thing twice"); the model
follows them well but not perfectly, and the failure mode is a practitioner being
asked something they just answered.

Two directions I'd iterate on:

- **Reduce the redundancy structurally, not just by instruction.** The plan items
  already carry ids and `satisfies` tracking; I'd lean on that harder — e.g. feed
  each phase an explicit "already settled" digest built from recorded
  factors/actions and their `satisfies` ids, so the model is steered by state
  rather than re-deriving what's left from prose each turn. Prompt iteration on the
  litmus wording helps, but the durable fix is making the open-vs-settled set
  unambiguous in context.
- **Make the questions friendlier.** The output is currently "concise and
  clinical" by instruction. Within the Just Culture framing we already load, I'd
  soften the phrasing toward how a supportive manager actually talks — less
  interrogative, more "walk me through…", acknowledging the previous answer before
  the next question — without losing the one-question-at-a-time discipline. This is
  pure prompt-engineering iteration (and worth an eval harness: a handful of
  scripted incidents, graded for repeated questions and tone), which is why it sits
  here rather than being a one-line change I'd make blind.

## Deployment & Infrastructure

### Abstract the infra seams so the app can deploy to a cloud provider

Right now the app binds directly to its infrastructure. The services are
constructed as `lru_cache` singletons in `api/dependencies.py` that each reach
straight for a concrete implementation — `PolicyService`/`IncidentService` build
their own SQLAlchemy `Session` against a Postgres URL, embeddings go straight to
`OpenAIEmbeddings`, tracing is wired in `telemetry.py`. That's fine for a single
docker-compose deployment, but there's no seam to swap a managed cloud backend in,
so a move to AWS or Azure would mean editing construction sites all over the code.

The plan is to introduce a thin abstraction layer per infra dependency and inject
the implementation, the way I did it in `scoreguy`. There the media-storage
dependency is a single `MediaStorage` `Protocol` with two backends — a local
directory in dev, Azure Blob in prod — selected by a `build_storage()` factory off
settings, and handed to the app through FastAPI `Depends`. The same shape applies
here:

- **Define `Protocol` contracts for each infra seam** — the database/session
  source, the embedding client, and the tracing/telemetry exporter — capturing
  only the methods the app actually uses. The existing services depend on the
  protocol, not the concrete class.
- **Select the backend with a `build_*` factory driven by settings**, resolved in
  `get_settings`/`config`, so `dev` wires Postgres + local OTEL and `prod` wires a
  managed DB (RDS / Azure Postgres), a managed embedding endpoint if we move off
  OpenAI, and a hosted OTEL collector — without touching the services. The
  `lru_cache` singletons stay, but they construct through the factory.
- **Keep the dependency-injection discipline through the FastAPI layer** so tests
  can inject fakes at the seam (matching the `mocks/` fixture pattern the testing
  standards already call for) instead of monkeypatching construction.

Once those seams exist, the deployment itself is **Terraform**, split the way
`scoreguy`'s is: a long-lived `platform/` layer (resource group / VPC, the managed
database with pgvector, secrets, networking) and a redeployable `app/` layer (the
container service running the API, wired to the platform's outputs). The app reads
connection details from environment/secrets the Terraform provisions, which the
config tree already centralizes — so standing up a cloud environment is
`terraform apply` plus the image, not a code change.

I deferred this because the single-node docker-compose setup is enough to run and
demo the system, and the abstraction only earns its keep once there's a real target
environment to deploy to. But designing the seams early is cheap, and retrofitting
them after the services have hardwired their backends everywhere is not — so this is
the first infrastructure item I'd pick up.

## PII / PHI Handling

The system handles patient PII/PHI but has no scrubbing layer yet. The telemetry
is already written to be PHI-free (`telemetry.py` records only structural span
attributes), and `search_incidents` *claims* its results are PII-redacted — but
nothing enforces that today, and raw practitioner narrative (names, MRNs, dates of
birth) flows straight through the routes and on to OpenAI. There are two distinct
scrubbing seams I'd add, and they do different jobs.

### Scrub incoming PII at the edge, in middleware

Add an ASGI middleware that inspects request bodies before they reach the routes,
alongside the `CORSMiddleware` already wired in `create_app()`. The goal is a
boundary guarantee: PII that doesn't need to be stored never gets persisted in the
first place.

- Detect identifiers (names, MRNs, SSNs, phone numbers, dates of birth) with a
  detector — a library like Presidio, or a regex/NER pass for the structured ones —
  and redact or reject at the edge depending on the field's contract.
- This is the coarse, defensive net: it runs on every route uniformly and doesn't
  understand the clinical workflow, so it errs toward catching obvious identifiers
  rather than preserving meaning. It's what keeps raw PII out of logs, the request
  trace, and any field we never intended to hold it.

### Reversible tokenization inside the AI workflow

The middleware can't simply strip everything, because the reporting agent *needs*
the narrative to reason — "the physician wasn't notified for 45 minutes" is the
whole point. So within the AI workflow there's a second, meaning-preserving seam:
before any content is sent to an AI service, replace each identifier with a stable
**placeholder token** (`[PATIENT_1]`, `[PHYSICIAN_2]`, `[MRN_1]`) and keep the
mapping in process.

- The model reasons over the tokenized text — it can still track who did what and
  when, because the tokens are *consistent* within a conversation — but no real
  identifier ever leaves the boundary to OpenAI.
- On the way back, re-hydrate the tokens for anything shown to the practitioner,
  who is authorized to see the real names; the stored report keeps the tokenized
  form plus the mapping under the same PHI/workforce split noted elsewhere.
- This is exactly the de-identification layer the incident-store section depends on
  (summaries are tokenized before they're ever embedded) — so building it once
  serves both the live AI path and the precedent store, rather than growing two.

I deferred both because the current single-tenant demo runs inside a trusted
boundary, but this is the item with the clearest compliance stakes (HIPAA), so the
middleware net in particular is near the top of the real-build list.
