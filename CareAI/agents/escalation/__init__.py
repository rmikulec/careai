"""Escalation agent: policy-grounded severity assessment of finalized reports."""

from CareAI.agents.escalation.agent import assess_severity, build_escalation_agent
from CareAI.agents.escalation.state import EscalationState

__all__ = ["build_escalation_agent", "assess_severity", "EscalationState"]
