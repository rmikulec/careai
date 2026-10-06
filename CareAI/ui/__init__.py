"""Streamlit front-end for the CareAI reporting agent.

A thin HTTP client over the ``/api/v1/reporting`` endpoints — it holds no agent
or database logic of its own; conversation state lives server-side keyed by
``thread_id``. The entrypoint is ``streamlit_app.py``.
"""
