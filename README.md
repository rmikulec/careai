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

  
### Architecture

This will be a multi-agent workflow engine, deployed in the cloud, and working alongside a managed
vector database that stays synced with the facility's policies. 

 - Agents: `Langchain`
 - VectorDB: `postgres` with `pgvector`