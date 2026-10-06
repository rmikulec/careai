# Florence Heathcare Take-Home Assignment

**Chose Use Case** Incident Reporting and Escalation

### Problem

Incident Reporting is an inconsistent process defined and implemented thousands of ways
across all hospitals / facilities. Reporting relies. soley on the expectation that nurses, doctors,
and other practicioners will self report incidents in full and accurate detail. 

One of the biggest problems facing Incident Reporting is underreporting, caused by many factors such
as `time-consuming paper forms`, `not knowing *what* to report`, `fear of repurcussions`, and many more.


### Solution
 A friendly, data-driven AI Agent, that has complete access to a facility's policies and
previous incidents, allowing it to know **what** to ask, and **when** to ask it.

   - `time-consuming paper forms`: A easy to use chatbot, where reporters now just "talk" to an
   agent rather than filling out mundane forms
   - `not knowing *what* to report`: Agent can structure all incidents, with linkage to specific
   policies, allowing it to prompt the practiciter about incidents proactively, rather than
   reactionary
   - `fear of repurcussions`: Asking specific questions in a friendly, easy to approach way, can
   lead to a higher response rate, and gathering the correct data when needed. Rather than relying
   on blank text blocks and the practioner's judgement on what is relevant.

[Source](https://www.quasrplus.com/blog/incident-reporting-in-healthcare/)  

### Architecture

This will be a multi-agent workflow engine, deployed in the cloud, and working alongside a managed
vector database that stays synced with the facility's policies. 

 - Agents: `Langgraph`
 - VectorDB: `postgres` with `pgvector`
 - Backend: FastAPI
 - Frontend Demo: Streamlit


### Agent Workflow
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

The finalized report is then sent to an Escalation Agent, which is a seperate process to ensure no bias from the
reporeting agent's conversation. It is given the finalized report as well as relevant policies,
and determines what severity level the incident is, grounded in multi-step reasoning, linked to
specific policy sections. Based on this severity level, the escalation agent can then draft
notifications to be sent.

In order to ensure the best results. Both agents are grounding in guidelines defined as "Just Culture"
The goal of that framework is to create an open space for reporting, in order to gain the most accurate
and complete report to prevent future incidents.
[source](https://pmc.ncbi.nlm.nih.gov/articles/PMC3776518/)




#### Implementation Strategies
Due to time contraints, different part's of this app will recieve different levels of care.
The main focus is on the actual agents, and the backend systems around them, rather than the
frontend delivery or strict product goals.

