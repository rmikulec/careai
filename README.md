# CareAI

**Chose Use Case** Incident Reporting and Escalation

### Problem

Incident Reporting is an inconsistent process defined and implemented thousands of ways
across all hospitals / facilities. Reporting relies solely on the expectation that nurses, doctors,
and other practitioners will self-report incidents in full and accurate detail.

One of the biggest problems facing Incident Reporting is underreporting, caused by many factors such
as `time-consuming paper forms`, `not knowing *what* to report`, `fear of repercussions`, and many more. [1]

### Solution
 A friendly, data-driven AI Agent that has complete access to a facility's policies and
previous incidents, allowing it to know **what** to ask, and **when** to ask it.

   - `time-consuming paper forms`: An easy-to-use chatbot, where reporters now just "talk" to an
   agent rather than filling out mundane forms
   - `not knowing *what* to report`: Agent can structure all incidents, with linkage to specific
   policies, allowing it to prompt the practitioner about incidents proactively, rather than
   reactively
   - `fear of repercussions`: Asking specific questions in a friendly, easy-to-approach way can
   lead to a higher response rate, and gathering the correct data when needed. Rather than relying
   on blank text blocks and the practitioner's judgement on what is relevant.

#### Agent Workflow
The workflow is broken up into many different "Phases", each with access to a different set of tools
and goals. The workflow is designed to fully understand the facility's policies, and based on that,
get the most accurate and relevant information from the reporting physician.

The Reporting Agent has access to a pre-chunked VectorDB containing all of the facility's policies.
The agent can search these policies, and add any relevant ones to the report, to be used later.
After reading these policies, it operates in two phases:
  1. Contributing factors: Try to identify any factors that may have contributed to the incident. The
  goal here is to make it easier for the reporter to get all of the relevant information down, with
  little to no pressure. These questions are planned out based on the related policies, and / or
  related past incidents.
  2. Actions Taken: After getting the complete picture of the incident, the agent then tries to
  identify what actions have been taken, directly linking the incident to specific policies.

The finalized report is then sent to an Escalation Agent, which is a separate process to ensure no bias from the
reporting agent's conversation. It is given the finalized report as well as relevant policies,
and determines what severity level the incident is, grounded in multi-step reasoning, linked to
specific policy sections. Based on this severity level, the escalation agent can then draft
notifications to be sent.

In order to ensure the best results, both agents are grounded in guidelines defined as "Just Culture". [2]
The goal of that framework is to create an open space for reporting, in order to gain the most accurate
and complete report to prevent future incidents.

The full stage-by-stage design — the grounding model, the completeness gate, and the escalation
subagent — is written up in the incident reporting design doc. [3]

### Architecture

This will be a multi-agent workflow engine, deployed in the cloud, and working alongside a managed
vector database that stays synced with the facility's policies.

 - Agents: `Langgraph`
 - VectorDB: `postgres` with `pgvector`
 - Backend: FastAPI
 - Frontend Demo: Streamlit

### A note on the policy documents

Real facility policies are confidential, so I couldn't use any here. The policy PDFs in this repo
are not real — I used Claude to generate a synthetic corpus so there was something realistic to
build and test retrieval, grounding, and severity against. They live in `policy_corpus/documents/`,
and the scripts that produced them are in `policy_corpus/generators/`. The facility ("Riverside
Regional Medical Center") and every name in them are made up; the standards they cite (OSHA, CMS,
EMTALA, The Joint Commission, etc.) are real, so retrieval behaves against plausible content.

### Running it with Docker Compose

The whole stack runs from one compose file. You need Docker and an OpenAI key.

1. Put your key in a `.env` file at the repo root (it is git-ignored):

   ```
   OPENAI_API_KEY=sk-...
   # optional: OPENAI_MODEL=gpt-5.6-luna
   ```

2. Build and start everything:

   ```
   docker compose up --build
   ```

   The database comes **pre-seeded**: on its first boot it restores `db/seed.sql.gz`, which holds
   the whole compiled policy corpus (all 67 policies, embeddings included) plus a few example
   reports and their conversations. So the stack comes up ready — no re-ingesting, and you don't
   need an OpenAI key just to explore what's there. Add `-d` to run detached.

   To start from an empty database instead, reset the volume with `docker compose down -v` and
   bring it back up; then upload your own policy PDFs (for example the ones in
   `policy_corpus/documents/`) through `POST /api/v1/policies/upload` — easiest from the API docs
   page below — with the header `X-API-Key: dev-local-key`.

> Note: filing a *new* report still calls OpenAI (to embed the search query and run the agents),
> so the key in step 1 is needed for a live conversation — just not to load the policy corpus.

Once it is up, these URLs are available:

| URL | Service | Notes |
|---|---|---|
| http://localhost:8501 | Streamlit UI | The demo. Chat on the left, the report / severity / drafted notifications on the right. The seeded example reports show in the **Report history** sidebar — click one to open its report, severity, and notifications. Sends the API key for you. |
| http://localhost:8000 | API (FastAPI) | All `/api/v1/*` routes need the header `X-API-Key: dev-local-key`. |
| http://localhost:8000/docs | API docs | Interactive Swagger UI — the simplest way to upload policies and poke endpoints. |
| http://localhost:8000/health | Health check | Unauthenticated liveness probe. |
| http://localhost:16686 | Jaeger (traces) | OpenTelemetry trace explorer; the API exports spans here over OTLP. Spans carry no PHI. Dev only, in-memory. |
| http://localhost:5050 | pgAdmin | Inspect the database. The CareAI server is pre-registered; connect with password `florence`. |
| localhost:5432 | Postgres (pgvector) | Direct DB access if you want it: user / password / db are all `florence`. |

All credentials here are throwaway local-dev values — this is not a production manifest.


### References

 - [1] "Incident Reporting in Healthcare," QUASR. https://www.quasrplus.com/blog/incident-reporting-in-healthcare/
 - [2] Just Culture framework (PMC3776518), US National Library of Medicine. https://pmc.ncbi.nlm.nih.gov/articles/PMC3776518/
 - [3] Incident Reporting Agent — design doc: `design-docs/incident-reporting.md`
 - [4] Future Considerations — design doc: `design-docs/future-considerations.md`
 - [5] Agentic Workflow Ideas — design doc: `design-docs/agentic-workflow-ideas.md`
