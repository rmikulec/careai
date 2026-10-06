# Notebooks

Prototyping and testing playground. These are where each piece of the system was
worked out interactively — against a live model and the real pgvector store —
before it was hardened into the `CareAI` package. They're scratch space, not part
of the app: handy for poking at the pipeline, but the committed code is the source
of truth.

| Notebook | What it is |
| --- | --- |
| `01_policy_vector_db.ipynb` | The policy RAG ingestion pipeline: hospital policy PDFs in `policy_corpus/documents/` → markdown + metadata → chunks → embeddings → the `policy_chunks` table in Postgres + pgvector. This is the retrieval layer `PolicyService` sits on. |
| `02_incident_reporting_agent.ipynb` | Building and testing the incident reporting agent end to end — collecting an incident from a practitioner, grounded in the retrieved policies and PII-scrubbed precedent. |

## Running them

Both expect the `pgvector` service from `docker-compose.yml`:

```bash
docker compose up -d db
```

Run `01` first — it populates the `policy_chunks` table that `02` retrieves from.
