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

- Give each `Person` a stable id and register them the way policies get added, so
  there's an authoritative set to link against.
- Add `related_people: list[str]` to `ActionTaken`, validated against that set in
  `record_action` — same rejection pattern as unknown policy ids.
- Mind the PHI split: patients are PHI, staff/witnesses are workforce data. The
  `role` field already distinguishes them; the de-identification layer should key
  off it.

I deferred this because nothing consumes the linkage yet — it pays off when the
manager view lands and wants to query the report as a graph.
