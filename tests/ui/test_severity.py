"""The Streamlit severity banner: tone heuristic and when it stays hidden.

The severity *scale* belongs to the facility's policies, so the UI only applies a
best-effort visual tone and must never raise — nor show anything — when there is
no finalized assessment to render.
"""

import CareAI.ui.streamlit_app as ui


def test_severity_tone_maps_common_cues() -> None:
    """Recognized cues get an urgency tone; everything else degrades to info."""
    assert ui._severity_tone("SEV-1 catastrophic")[0] == "error"
    assert ui._severity_tone("Sentinel event")[0] == "error"
    assert ui._severity_tone("SEV-2 major")[0] == "warning"
    assert ui._severity_tone("Major harm")[0] == "warning"
    assert ui._severity_tone("SEV-3 minor")[0] == "info"
    assert ui._severity_tone("Near Miss")[0] == "info"


def test_undetermined_severity_is_flagged_for_attention() -> None:
    """A null severity (policies defined no criteria) reads as 'needs attention'."""
    tone, icon = ui._severity_tone(None)
    assert tone == "warning"
    assert icon


def test_banner_hidden_until_finalized_and_assessed() -> None:
    """No finalized report, or no escalation yet, renders nothing (and never raises)."""
    # Would raise if it tried to render anything via st.* in this guard path.
    ui._render_severity(None)
    ui._render_severity({})
    ui._render_severity({"severity": None, "escalation": None})
