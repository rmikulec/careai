"""Content definitions for the hospital policy corpus.

Each ``build_*`` function returns one :class:`PolicyDoc`. ``build_corpus``
assembles them all. Content is fictional-facility prose anchored to real
regulatory frameworks so the Incident Reporting Agent has realistic material to
retrieve, cite, and ground severity/notification decisions against.

Design intent (so the corpus is useful as a test fixture):
  * A single facility-wide severity scheme (SEV-1 / SEV-2 / SEV-3 / Near Miss)
    is defined in the master Incident Reporting policy (POL-RM-013) and
    referenced by the topic policies — the agent should be able to resolve a
    severity consistently across documents.
  * Every policy states concrete, time-bound notification deadlines in prose
    (e.g. "notify Employee Health within 2 hours") because the agent extracts
    those at submission time.
  * Topic policies restate the specific immediate actions the agent must surface
    to a reporter before intake is complete.
"""

from __future__ import annotations

from reportlab.lib.units import inch

from _policy_model import (
    Bullets,
    Note,
    Para,
    PolicyDoc,
    Section,
    Steps,
    TableBlock,
    _SEV1,
    _SEV2,
    _SEV3,
)

_APPROVER = "Patient Safety & Quality Committee"


def build_incident_reporting() -> PolicyDoc:
    """Master incident reporting + facility-wide severity classification."""
    return PolicyDoc(
        number="POL-RM-013",
        title="Incident Reporting and Event Severity Classification",
        owner="Risk Management / Patient Safety",
        effective="2024-01-15",
        revised="2026-02-10",
        review="2028-02-10",
        version="4.2",
        approved_by=_APPROVER,
        applies_to="All staff, licensed providers, students, and contractors, "
        "all departments and units",
        keywords=[
            "incident report",
            "event report",
            "severity",
            "escalation",
            "near miss",
            "notification",
            "sentinel event",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "This policy establishes a single, facility-wide process for "
                        "reporting patient-safety events, staff-safety events, and "
                        "near misses, and a common severity scale used to triage, "
                        "escalate, and notify. It is the governing reference for "
                        "event severity and notification timing; topic-specific "
                        "policies restate these rules for their domain and must not "
                        "conflict with this document."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to any event or unsafe condition that reached a "
                        "patient, visitor, or staff member, as well as near misses "
                        "(events intercepted before reaching a patient) and unsafe "
                        "conditions. Reporting is non-punitive; the facility "
                        "maintains a just-culture framework and does not discipline "
                        "staff for good-faith reporting of errors or near misses."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Event</b> — any happening not consistent with the "
                            "routine operation of the facility or routine care of a "
                            "patient.",
                            "<b>Near miss (close call)</b> — an event that did not "
                            "reach the patient, whether by chance or active "
                            "interception.",
                            "<b>Harm</b> — physical, psychological, or functional "
                            "injury. Graded as none, mild/temporary, "
                            "moderate/temporary, severe/temporary, permanent, or "
                            "death.",
                            "<b>Sentinel event</b> — a patient-safety event that "
                            "reaches a patient and results in death, permanent harm, "
                            "or severe temporary harm (The Joint Commission). All "
                            "sentinel events are SEV-1.",
                            "<b>Serious Reportable Event (SRE / &ldquo;never "
                            "event&rdquo;)</b> — one of the 29 NQF events in 7 "
                            "categories (e.g., wrong-site surgery, retained foreign "
                            "object, air embolism, Stage 3/4 hospital-acquired "
                            "pressure injury).",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy — Severity Classification",
                [
                    Para(
                        "Every reported event is assigned one severity level. When "
                        "the facts could support two levels, assign the higher level "
                        "and let review adjust it. Severity drives the notification "
                        "and review requirements in Section 6."
                    ),
                    TableBlock(
                        headers=["Level", "Definition", "Typical examples"],
                        rows=[
                            [
                                "<b>SEV-1</b><br/>Catastrophic / Sentinel",
                                "Death, permanent harm, or severe temporary harm; any "
                                "sentinel event or Serious Reportable Event; any event "
                                "requiring a life-sustaining intervention.",
                                "Wrong-site surgery; hemolytic transfusion reaction; "
                                "fall with intracranial hemorrhage; suicide of an "
                                "inpatient; infant abduction.",
                            ],
                            [
                                "<b>SEV-2</b><br/>Major",
                                "Temporary harm requiring intervention, treatment, or "
                                "an increased level of care, or a prolonged length of "
                                "stay.",
                                "Medication error reaching the patient and requiring "
                                "treatment; fall with fracture; Stage 2 "
                                "hospital-acquired pressure injury.",
                            ],
                            [
                                "<b>SEV-3</b><br/>Minor",
                                "Event reached the patient but caused no harm or only "
                                "minimal harm not requiring treatment beyond "
                                "monitoring.",
                                "Medication given one hour late without consequence; "
                                "unwitnessed fall with no injury; mislabeled "
                                "non-critical specimen caught before resulting.",
                            ],
                            [
                                "<b>Near&nbsp;Miss</b>",
                                "Error or unsafe condition intercepted before reaching "
                                "the patient.",
                                "Wrong medication caught at the bedside scan; "
                                "incorrect blood unit caught during the two-person "
                                "check.",
                            ],
                        ],
                        col_widths=[1.25 * inch, 2.35 * inch, 2.2 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3, None],
                    ),
                ],
            ),
            Section(
                "Procedure — Filing a Report",
                [
                    Steps(
                        [
                            "Ensure the patient and the area are safe; render "
                            "immediate clinical care before documenting.",
                            "File an event report in the electronic reporting system "
                            "as soon as the situation is stable, and no later than "
                            "the end of the shift on which the event occurred or was "
                            "discovered.",
                            "Describe the facts objectively — what happened, when, "
                            "where, who was involved, and what was done. Do not record "
                            "blame, opinion, or speculation.",
                            "Record the patient's condition and any monitoring or "
                            "treatment initiated in response.",
                            "Notify per the matrix in Section 6 based on the assigned "
                            "severity. When in doubt about severity, escalate.",
                        ]
                    ),
                    Note(
                        "The event report is a confidential quality-improvement "
                        "document. Do not file it in or reference it from the "
                        "patient's medical record. Clinical facts belong in the "
                        "medical record; the event report does not."
                    ),
                ],
            ),
            Section(
                "Reporting & Notification Requirements",
                [
                    TableBlock(
                        headers=[
                            "Severity",
                            "Who must be notified",
                            "By when",
                            "Review",
                        ],
                        rows=[
                            [
                                "SEV-1",
                                "Attending provider, Charge Nurse, Nursing "
                                "Supervisor, Risk Management, and the "
                                "Administrator-on-Call.",
                                "Immediately, and never later than 1 hour from "
                                "discovery.",
                                "Mandatory human review. Comprehensive systematic "
                                "analysis (RCA²) and action plan within 45 business "
                                "days for sentinel events.",
                            ],
                            [
                                "SEV-2",
                                "Attending provider, Charge Nurse, and Risk "
                                "Management.",
                                "Within 4 hours.",
                                "Human review within 3 business days.",
                            ],
                            [
                                "SEV-3",
                                "Charge Nurse; Risk Management via the event report.",
                                "Within 24 hours.",
                                "Quality review in aggregate.",
                            ],
                            [
                                "Near Miss",
                                "Charge Nurse; Risk Management via the event report.",
                                "Within 24 hours.",
                                "Aggregate trend review.",
                            ],
                        ],
                        col_widths=[0.85 * inch, 2.4 * inch, 1.5 * inch, 1.6 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3, None],
                    ),
                    Para(
                        "External reporting (State Department of Health, CMS, FDA "
                        "MedWatch, or accrediting bodies) is coordinated solely by "
                        "Risk Management and is not initiated at the unit level."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Reporter name, role, and contact; date/time of the event "
                            "and of discovery.",
                            "Location (unit/room) and persons involved (patient MRN, "
                            "staff, witnesses).",
                            "Objective description of the event and immediate actions "
                            "taken.",
                            "Patient condition before and after; monitoring and "
                            "treatment initiated.",
                            "Assigned severity and every notification made (who, "
                            "when, by what method).",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission, Sentinel Event Policy (CAMH), "
                            "comprehensive systematic analysis within 45 business "
                            "days.",
                            "National Quality Forum, Serious Reportable Events (2011) "
                            "— 29 events in 7 categories.",
                            "AHRQ Common Formats for Event Reporting.",
                            "Related: POL-EH-001, POL-PS-002, POL-PS-003, POL-RM-004, "
                            "POL-LAB-006, POL-SURG-007, POL-PS-008, POL-NUR-009.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_bloodborne() -> PolicyDoc:
    """Needlestick / sharps / bloodborne pathogen exposure."""
    return PolicyDoc(
        number="POL-EH-001",
        title="Bloodborne Pathogen Exposure and Needlestick / Sharps Injury",
        owner="Employee / Occupational Health · Environmental Health & Safety",
        effective="2023-07-01",
        revised="2026-01-20",
        review="2028-01-20",
        version="5.1",
        approved_by="Environmental Health & Safety Committee",
        applies_to="All employees, licensed providers, students, volunteers, and "
        "contract staff with potential occupational exposure",
        keywords=[
            "needlestick",
            "sharps",
            "bloodborne pathogen",
            "exposure",
            "post-exposure prophylaxis",
            "PEP",
            "employee health",
            "source patient",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To protect staff from occupational exposure to blood and "
                        "other potentially infectious materials (OPIM) and to ensure "
                        "a prompt, confidential post-exposure evaluation consistent "
                        "with the OSHA Bloodborne Pathogens Standard (29 CFR "
                        "1910.1030)."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to any percutaneous injury (needlestick, cut with a "
                        "contaminated sharp) or mucous-membrane / non-intact-skin "
                        "contact with blood or OPIM occurring in the course of work."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Exposure incident</b> — specific eye, mouth, other "
                            "mucous membrane, non-intact skin, or parenteral contact "
                            "with blood or OPIM.",
                            "<b>Source individual</b> — the person whose blood or OPIM "
                            "was involved in the exposure.",
                            "<b>PEP</b> — post-exposure prophylaxis, medication "
                            "started after a possible HIV exposure.",
                        ]
                    ),
                ],
            ),
            Section(
                "Immediate Actions (Employee)",
                [
                    Note(
                        "Time-critical. HIV post-exposure prophylaxis is most "
                        "effective when started as soon as possible — ideally within "
                        "2 hours — and is not recommended beyond 72 hours. The "
                        "exposed employee must be evaluated by Employee Health "
                        "within 2 hours of the exposure (go to the Emergency "
                        "Department if Employee Health is closed)."
                    ),
                    Steps(
                        [
                            "Immediately wash the site with soap and water; flush "
                            "mucous membranes and eyes with water or saline for "
                            "15 minutes.",
                            "Report the exposure to your charge nurse or supervisor "
                            "right away — do not wait until the end of shift.",
                            "Present to Employee Health (or the ED after hours) within "
                            "2 hours for evaluation and, if indicated, PEP.",
                            "File an event report per POL-RM-013 before the end of the "
                            "shift.",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy — Source Testing and Evaluation",
                [
                    Bullets(
                        [
                            "Source-individual blood is tested for HBV, HCV, and HIV "
                            "as soon as feasible after consent is obtained. Testing "
                            "requires documented consent where required by state law; "
                            "the exposed employee's need to know does not waive "
                            "consent requirements.",
                            "The exposed employee's baseline blood is collected with "
                            "consent; if the employee declines testing, the sample is "
                            "preserved for at least 90 days.",
                            "Post-exposure evaluation, follow-up, and any prophylaxis "
                            "are provided confidentially and at no cost to the "
                            "employee.",
                            "Hepatitis B vaccination is offered to all at-risk staff "
                            "within 10 working days of initial assignment.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Escalation",
                [
                    Para(
                        "A sharps/exposure incident is classified under POL-RM-013. "
                        "A confirmed high-risk source (known HIV/HCV positive) or any "
                        "exposure requiring PEP is escalated as SEV-2; routine "
                        "low-risk exposures are SEV-3. Escalate immediately if the "
                        "employee is symptomatic or the source is high-risk."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Route and depth of exposure; device type and brand, and "
                            "whether a safety feature was engaged.",
                            "Body fluid involved and estimated volume/duration of "
                            "contact.",
                            "Source identity and infectious status (if known); "
                            "consent for source testing.",
                            "Department/work area and a description of how the "
                            "incident occurred — recorded on the OSHA Sharps Injury "
                            "Log, kept confidentially for 5 years.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "OSHA Bloodborne Pathogens Standard, 29 CFR 1910.1030 "
                            "(post-exposure evaluation §(f); sharps injury log "
                            "§(h)(5)).",
                            "CDC, Updated U.S. Public Health Service Guidelines for "
                            "Management of Occupational Exposures to HIV and "
                            "Recommendations for PEP.",
                            "Related: POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_falls() -> PolicyDoc:
    """Patient fall prevention and post-fall response."""
    return PolicyDoc(
        number="POL-PS-002",
        title="Patient Fall Prevention and Post-Fall Response",
        owner="Nursing / Patient Safety",
        effective="2023-09-01",
        revised="2026-03-05",
        review="2028-03-05",
        version="3.4",
        approved_by=_APPROVER,
        applies_to="All inpatient and observation units, the ED, and procedural areas",
        keywords=[
            "fall",
            "patient safety",
            "post-fall",
            "head strike",
            "anticoagulant",
            "neuro checks",
            "fall risk",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To reduce patient falls through risk assessment and "
                        "prevention, and to standardize the clinical response, "
                        "monitoring, and reporting after a fall."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to all patients in inpatient, observation, "
                        "emergency, and procedural settings. Fall-risk assessment is "
                        "completed on admission, every shift, after any fall, and on "
                        "change in condition."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Fall</b> — an unplanned descent to the floor or other "
                            "lower surface, with or without injury.",
                            "<b>Witnessed / unwitnessed fall</b> — whether a staff "
                            "member directly observed the descent.",
                            "<b>Head strike</b> — any impact to the head, or an "
                            "unwitnessed fall in which head impact cannot be excluded.",
                        ]
                    ),
                ],
            ),
            Section(
                "Post-Fall Immediate Response",
                [
                    Note(
                        "Do not move the patient until injury has been assessed. A "
                        "fall with head strike, or any fall in a patient on "
                        "anticoagulant or antiplatelet therapy, is SEV-1 and requires "
                        "physician notification within 1 hour and immediate "
                        "consideration of head CT."
                    ),
                    Steps(
                        [
                            "Stay with the patient; call for help. Assess airway, "
                            "breathing, circulation, and level of consciousness.",
                            "Assess for injury head-to-toe before moving — pain, "
                            "deformity, bleeding, and signs of fracture or spinal "
                            "injury.",
                            "Obtain vital signs and a neurological assessment; "
                            "determine whether head strike occurred or cannot be "
                            "excluded.",
                            "Notify the attending provider — within 1 hour for any "
                            "head strike, anticoagulated patient, or suspected "
                            "injury; promptly for all other falls.",
                            "Initiate neuro checks when indicated (see Section 6) and "
                            "notify the patient's family per the patient's wishes.",
                            "Conduct a post-fall huddle and file an event report per "
                            "POL-RM-013.",
                        ]
                    ),
                ],
            ),
            Section(
                "Neurological Monitoring After Head Strike",
                [
                    Para(
                        "For any head strike, unwitnessed fall where head impact "
                        "cannot be excluded, or anticoagulated patient, initiate "
                        "neurological checks and vital signs on the following minimum "
                        "schedule (increase frequency for any deterioration):"
                    ),
                    Bullets(
                        [
                            "Every 15 minutes &times; 4 (first hour),",
                            "then every 1 hour &times; 4,",
                            "then every 4 hours to complete 24 hours of monitoring.",
                        ]
                    ),
                    Para(
                        "Anticoagulated and antiplatelet patients carry elevated risk "
                        "of delayed intracranial hemorrhage; maintain a low threshold "
                        "for head CT even without external signs of trauma, and "
                        "re-notify the provider for any new neurological change."
                    ),
                ],
            ),
            Section(
                "Severity Classification",
                [
                    TableBlock(
                        headers=["Finding", "Severity"],
                        rows=[
                            [
                                "Head strike, anticoagulated patient, or intracranial "
                                "hemorrhage / fracture / major injury",
                                "SEV-1",
                            ],
                            [
                                "Fall with injury requiring treatment (e.g., "
                                "laceration requiring sutures, minor fracture)",
                                "SEV-2",
                            ],
                            ["Fall with no injury", "SEV-3"],
                        ],
                        col_widths=[4.6 * inch, 1.2 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Whether the fall was witnessed; activity and location at "
                            "time of fall.",
                            "Whether head strike occurred or cannot be excluded; "
                            "anticoagulant/antiplatelet status.",
                            "Assessment findings, vital signs, and neuro-check "
                            "results with times.",
                            "Provider and family notification (who, when); "
                            "interventions and imaging ordered.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "AHRQ, Preventing Falls in Hospitals: A Toolkit for "
                            "Improving Quality of Care.",
                            "The Joint Commission, National Patient Safety Goals — "
                            "falls.",
                            "Related: POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_medication() -> PolicyDoc:
    """Medication error and adverse drug event reporting."""
    return PolicyDoc(
        number="POL-PS-003",
        title="Medication Error and Adverse Drug Event Reporting",
        owner="Pharmacy / Patient Safety",
        effective="2023-05-15",
        revised="2026-02-28",
        review="2028-02-28",
        version="4.0",
        approved_by=_APPROVER,
        applies_to="All staff who prescribe, transcribe, dispense, administer, or "
        "monitor medications",
        keywords=[
            "medication error",
            "adverse drug event",
            "ADE",
            "NCC MERP",
            "wrong dose",
            "high-alert medication",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To standardize detection, response, and reporting of "
                        "medication errors and adverse drug events (ADEs), and to "
                        "classify events by harm using the NCC MERP index."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Medication error</b> — any preventable event that may "
                            "cause or lead to inappropriate medication use or patient "
                            "harm.",
                            "<b>Adverse drug event (ADE)</b> — harm resulting from the "
                            "use of a medication.",
                            "<b>High-alert medication</b> — a drug bearing heightened "
                            "risk of significant harm when used in error (e.g., "
                            "insulin, heparin, opioids, concentrated electrolytes, "
                            "chemotherapy).",
                        ]
                    ),
                ],
            ),
            Section(
                "Harm Classification (NCC MERP Index)",
                [
                    Para(
                        "Classify every medication error by the NCC MERP category, "
                        "which maps to the facility severity scale."
                    ),
                    TableBlock(
                        headers=["Category", "Meaning", "Facility severity"],
                        rows=[
                            [
                                "A",
                                "Circumstances capable of causing error.",
                                "Near Miss",
                            ],
                            [
                                "B",
                                "Error occurred but did not reach the patient.",
                                "Near Miss",
                            ],
                            ["C", "Reached the patient; no harm.", "SEV-3"],
                            [
                                "D",
                                "Reached the patient; required monitoring to "
                                "confirm no harm.",
                                "SEV-3",
                            ],
                            ["E", "Temporary harm requiring intervention.", "SEV-2"],
                            [
                                "F",
                                "Temporary harm requiring or prolonging "
                                "hospitalization.",
                                "SEV-2",
                            ],
                            ["G", "Permanent harm.", "SEV-1"],
                            ["H", "Intervention required to sustain life.", "SEV-1"],
                            ["I", "Contributed to or resulted in death.", "SEV-1"],
                        ],
                        col_widths=[0.9 * inch, 3.5 * inch, 1.4 * inch],
                        row_shades=[
                            None,
                            None,
                            _SEV3,
                            _SEV3,
                            _SEV2,
                            _SEV2,
                            _SEV1,
                            _SEV1,
                            _SEV1,
                        ],
                    ),
                ],
            ),
            Section(
                "Immediate Response",
                [
                    Note(
                        "If an error reaches the patient, assess and stabilize the "
                        "patient first, notify the ordering provider immediately, and "
                        "follow any ordered monitoring or reversal. For a "
                        "high-alert-medication error reaching the patient, notify the "
                        "provider and Pharmacy without delay and classify at least "
                        "SEV-2."
                    ),
                    Steps(
                        [
                            "Assess the patient and provide clinically indicated care.",
                            "Notify the ordering/attending provider; obtain orders "
                            "for monitoring, antidote, or reversal as needed.",
                            "Notify Pharmacy for guidance and to quarantine any "
                            "implicated product.",
                            "File an event report per POL-RM-013; classify by NCC "
                            "MERP category.",
                        ]
                    ),
                ],
            ),
            Section(
                "Notification Timing",
                [
                    Bullets(
                        [
                            "SEV-1 (NCC MERP G–I): notify provider, Nursing "
                            "Supervisor, and Risk Management immediately and within "
                            "1 hour.",
                            "SEV-2 (NCC MERP E–F): notify provider and Risk "
                            "Management within 4 hours.",
                            "SEV-3 / Near Miss (NCC MERP A–D): event report within "
                            "24 hours.",
                        ]
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Medication, dose, route, and the node where the error "
                            "occurred (prescribing, transcribing, dispensing, "
                            "administering, monitoring).",
                            "Whether the drug is a high-alert medication.",
                            "Whether the error reached the patient and the NCC MERP "
                            "category.",
                            "Provider notification and any treatment, monitoring, or "
                            "reversal provided.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "NCC MERP Index for Categorizing Medication Errors.",
                            "ISMP List of High-Alert Medications in Acute Care "
                            "Settings.",
                            "Related: POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_sentinel() -> PolicyDoc:
    """Sentinel event management and root cause analysis."""
    return PolicyDoc(
        number="POL-RM-004",
        title="Sentinel Event Management and Root Cause Analysis",
        owner="Risk Management / Patient Safety",
        effective="2023-02-01",
        revised="2026-01-10",
        review="2028-01-10",
        version="3.1",
        approved_by=_APPROVER,
        applies_to="All departments; coordinated by Risk Management and the Patient "
        "Safety Officer",
        keywords=[
            "sentinel event",
            "root cause analysis",
            "RCA2",
            "serious reportable event",
            "never event",
            "action plan",
            "45 business days",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To define the facility's response to sentinel events and "
                        "Serious Reportable Events, including immediate stabilization, "
                        "a comprehensive systematic analysis (RCA²), and a measurable "
                        "corrective action plan."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Sentinel event</b> — a patient-safety event not "
                            "primarily related to the natural course of the patient's "
                            "illness that reaches the patient and results in death, "
                            "permanent harm, or severe temporary harm.",
                            "<b>Severe temporary harm</b> — critical, potentially "
                            "life-threatening harm lasting a limited time with no "
                            "permanent residual, but requiring transfer to a higher "
                            "level of care, additional major surgery/procedure, or "
                            "life-sustaining intervention.",
                            "<b>Serious Reportable Event</b> — an NQF &ldquo;never "
                            "event&rdquo;; always managed as a sentinel-level event.",
                        ]
                    ),
                ],
            ),
            Section(
                "Immediate Response",
                [
                    Note(
                        "A sentinel event is always SEV-1. Notify the "
                        "Administrator-on-Call, Risk Management, and the Patient "
                        "Safety Officer immediately. Secure and sequester any "
                        "involved equipment, devices, medications, and packaging — do "
                        "not discard, clean, or return to service — and preserve "
                        "them for analysis."
                    ),
                    Steps(
                        [
                            "Stabilize the patient and meet immediate care needs.",
                            "Notify Risk Management and the Administrator-on-Call "
                            "immediately (within 1 hour).",
                            "Sequester devices, medications, and records; document "
                            "chain of custody.",
                            "Begin disclosure to the patient/family per the "
                            "disclosure policy.",
                            "Provide support to involved staff (second-victim "
                            "resources).",
                        ]
                    ),
                ],
            ),
            Section(
                "Comprehensive Systematic Analysis (RCA²)",
                [
                    Bullets(
                        [
                            "Risk Management convenes an interdisciplinary RCA² team "
                            "within 72 hours of the event.",
                            "The analysis must be thorough and credible: identify "
                            "root causes and contributing factors, focusing on "
                            "systems and processes rather than individual blame.",
                            "A corrective action plan — specific, measurable, "
                            "time-limited, with assigned owners — and the completed "
                            "analysis are finalized within 45 business days of the "
                            "event or of becoming aware of it.",
                            "Action items are tracked to closure with effectiveness "
                            "measures.",
                        ]
                    ),
                ],
            ),
            Section(
                "External Reporting",
                [
                    Para(
                        "Risk Management determines and coordinates any external "
                        "reporting (The Joint Commission self-report, State "
                        "Department of Health, CMS). Self-reporting to The Joint "
                        "Commission is voluntary; the comprehensive systematic "
                        "analysis is completed regardless of whether the event is "
                        "reported externally."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission, Sentinel Event Policy and "
                            "Procedures.",
                            "National Patient Safety Foundation, RCA² — Improving "
                            "Root Cause Analyses and Actions to Prevent Harm.",
                            "National Quality Forum, Serious Reportable Events.",
                            "Related: POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_restraint() -> PolicyDoc:
    """Restraint and seclusion."""
    return PolicyDoc(
        number="POL-NUR-005",
        title="Restraint and Seclusion",
        owner="Nursing / Patient Care Services",
        effective="2023-04-01",
        revised="2026-02-15",
        review="2028-02-15",
        version="4.3",
        approved_by=_APPROVER,
        applies_to="All inpatient units, the ED, and behavioral-health areas",
        keywords=[
            "restraint",
            "seclusion",
            "violent self-destructive",
            "one-hour face-to-face",
            "CMS 482.13",
            "patient rights",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To ensure restraint and seclusion are used only when less "
                        "restrictive interventions have failed, for the minimum "
                        "necessary time, consistent with patient rights under CMS "
                        "Conditions of Participation (42 CFR 482.13)."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Restraint</b> — any manual method, physical or "
                            "mechanical device, or drug used to restrict movement "
                            "that is not a standard treatment for the patient's "
                            "condition.",
                            "<b>Seclusion</b> — involuntary confinement of a patient "
                            "alone in a room from which they are prevented from "
                            "leaving.",
                            "<b>Violent/self-destructive behavior</b> — behavior that "
                            "jeopardizes the immediate physical safety of the patient "
                            "or others.",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy — Orders",
                [
                    Note(
                        "Restraint or seclusion requires an order from a physician or "
                        "licensed practitioner responsible for the patient's care. "
                        "PRN (as-needed) and standing orders are prohibited. For "
                        "violent/self-destructive behavior, the patient must be seen "
                        "face-to-face within 1 hour of initiation."
                    ),
                    Bullets(
                        [
                            "The 1-hour face-to-face evaluation may be performed by a "
                            "physician/LP or by a trained registered nurse or "
                            "physician assistant, who then consults the attending.",
                            "Orders for violent/self-destructive behavior are "
                            "time-limited and may be renewed within the maximum "
                            "durations below, up to a total of 24 hours; after 24 "
                            "hours a new in-person evaluation is required before any "
                            "further order.",
                        ]
                    ),
                ],
            ),
            Section(
                "Maximum Order Durations (Violent / Self-Destructive Behavior)",
                [
                    TableBlock(
                        headers=["Patient age", "Maximum per order"],
                        rows=[
                            ["Adults (18 and older)", "4 hours"],
                            ["Children / adolescents ages 9–17", "2 hours"],
                            ["Children under age 9", "1 hour"],
                        ],
                        col_widths=[3.6 * inch, 2.2 * inch],
                    ),
                    Para(
                        "Restraint used for non-violent, non-self-destructive reasons "
                        "(e.g., to protect a medical device) follows separate order "
                        "and renewal rules and is reassessed at least every "
                        "24 hours by the provider."
                    ),
                ],
            ),
            Section(
                "Monitoring and Documentation",
                [
                    Bullets(
                        [
                            "Continuous monitoring appropriate to the type of "
                            "restraint/seclusion and the patient's condition; "
                            "assessment of circulation, nutrition, hydration, "
                            "toileting, and comfort.",
                            "Document the less-restrictive measures attempted, the "
                            "order, the 1-hour face-to-face findings, monitoring, and "
                            "the clinical justification for continuation.",
                            "Any death that occurs while a patient is in restraint or "
                            "seclusion, or within 24 hours after removal, is a SEV-1 "
                            "event and is reported to CMS as required.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CMS Conditions of Participation, 42 CFR 482.13(e)–(g) — "
                            "Patients' Rights.",
                            "The Joint Commission, Provision of Care standards on "
                            "restraint and seclusion.",
                            "Related: POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_transfusion() -> PolicyDoc:
    """Blood transfusion administration and reaction management."""
    return PolicyDoc(
        number="POL-LAB-006",
        title="Blood Transfusion Administration and Reaction Management",
        owner="Laboratory / Blood Bank (Transfusion Service) · Nursing",
        effective="2023-06-01",
        revised="2026-03-01",
        review="2028-03-01",
        version="3.2",
        approved_by=_APPROVER,
        applies_to="All staff who order, collect for, or administer blood components",
        keywords=[
            "transfusion",
            "blood",
            "transfusion reaction",
            "hemolytic",
            "blood bank",
            "two-person check",
            "FDA fatality",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To ensure safe administration of blood components and a "
                        "prompt, standardized response to suspected transfusion "
                        "reactions, consistent with AABB Standards and FDA "
                        "requirements."
                    ),
                ],
            ),
            Section(
                "Policy — Pre-Transfusion Verification",
                [
                    Bullets(
                        [
                            "Two qualified staff perform an independent bedside check "
                            "matching the patient's two identifiers, the blood bank "
                            "record, and the unit label/component before starting.",
                            "Obtain baseline vital signs immediately before "
                            "transfusion; remain with the patient for the first 15 "
                            "minutes, the period of highest risk.",
                        ]
                    ),
                ],
            ),
            Section(
                "Suspected Transfusion Reaction — Immediate Actions",
                [
                    Note(
                        "Stop the transfusion immediately at the first sign of a "
                        "reaction (fever, chills, hypotension, dyspnea, back/flank "
                        "pain, hemoglobinuria, or sudden deterioration). Keep the IV "
                        "line open with normal saline using new tubing, and notify "
                        "the ordering provider and the Blood Bank at once. An acute "
                        "hemolytic reaction is a SEV-1 event."
                    ),
                    Steps(
                        [
                            "Stop the transfusion; disconnect the unit but keep the "
                            "IV line patent with 0.9% normal saline via new tubing.",
                            "Recheck the patient's identifiers against the unit label "
                            "and paperwork at the bedside.",
                            "Assess and monitor vital signs; treat symptoms as "
                            "ordered.",
                            "Notify the ordering provider and the Blood Bank "
                            "immediately.",
                            "Return the blood unit and attached administration set to "
                            "the Blood Bank; collect post-reaction blood and urine "
                            "specimens per protocol.",
                            "Complete the transfusion reaction report form and file "
                            "an event report per POL-RM-013.",
                        ]
                    ),
                ],
            ),
            Section(
                "Reporting Requirements",
                [
                    Bullets(
                        [
                            "The Blood Bank investigates every suspected reaction and "
                            "notifies the component supplier(s) of implicated units.",
                            "Any transfusion- or collection-related fatality is "
                            "reported by the Blood Bank Medical Director to the FDA "
                            "Center for Biologics Evaluation and Research (CBER) as "
                            "soon as possible, with a written report within 7 days "
                            "of the fatality.",
                            "Participation in the CDC NHSN Hemovigilance Module is "
                            "maintained for trended surveillance.",
                        ]
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Component type and unit number; start/stop times and "
                            "volume infused.",
                            "Symptoms, onset time, vital-sign trend, and treatment.",
                            "Bedside re-verification result; specimens collected and "
                            "returned to the Blood Bank.",
                            "Provider and Blood Bank notification times.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "AABB, Standards for Blood Banks and Transfusion "
                            "Services.",
                            "FDA, 21 CFR 606.170 — fatality reporting to CBER.",
                            "Related: POL-PS-008 (patient identification), POL-RM-013 "
                            "(severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_universal_protocol() -> PolicyDoc:
    """Universal Protocol — wrong-site/procedure/person surgery prevention."""
    return PolicyDoc(
        number="POL-SURG-007",
        title="Universal Protocol: Prevention of Wrong-Site, Wrong-Procedure, "
        "and Wrong-Person Surgery",
        owner="Perioperative Services / Patient Safety",
        effective="2023-03-15",
        revised="2026-02-20",
        review="2028-02-20",
        version="3.0",
        approved_by=_APPROVER,
        applies_to="All operative and invasive procedures, in any setting "
        "(OR, procedural, bedside)",
        keywords=[
            "universal protocol",
            "wrong site",
            "wrong procedure",
            "time-out",
            "site marking",
            "pre-procedure verification",
            "surgery",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To prevent wrong-site, wrong-procedure, and wrong-person "
                        "events through the three components of The Joint Commission "
                        "Universal Protocol: pre-procedure verification, site "
                        "marking, and a time-out."
                    ),
                ],
            ),
            Section(
                "Policy — Three Required Components",
                [
                    Steps(
                        [
                            "<b>Pre-procedure verification.</b> Confirm the correct "
                            "patient (two identifiers), correct procedure, and "
                            "correct site, and that all relevant documents, consent, "
                            "images, and required equipment/implants are present and "
                            "matched.",
                            "<b>Site marking.</b> The licensed provider performing "
                            "the procedure marks the site, involving the patient when "
                            "possible, for any procedure with laterality, multiple "
                            "structures, or multiple levels. The mark must be "
                            "unambiguous and remain visible after prep and draping.",
                            "<b>Time-out.</b> Immediately before incision/start, the "
                            "entire team pauses and actively verbally confirms, at a "
                            "minimum, correct patient identity, correct site, and "
                            "correct procedure. The time-out is documented.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Note(
                        "A wrong-site, wrong-procedure, or wrong-person event is a "
                        "Serious Reportable Event and a sentinel event — always "
                        "SEV-1. If recognized at any point, stop immediately, "
                        "stabilize the patient, and notify the surgeon of record, the "
                        "Administrator-on-Call, and Risk Management at once. Manage "
                        "per POL-RM-004 (RCA² within 45 business days)."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Completed pre-procedure verification checklist and "
                            "consent.",
                            "Site mark and the name of the provider who marked it.",
                            "Time-out performed, participants, and confirmation of "
                            "patient/site/procedure.",
                            "Any discrepancy identified and how it was resolved "
                            "before proceeding.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission, Universal Protocol (UP.01.01.01, "
                            "UP.01.02.01, UP.01.03.01).",
                            "The Joint Commission, NPSG.01.01.01 — two patient "
                            "identifiers.",
                            "Related: POL-PS-008, POL-RM-004, POL-RM-013.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_patient_id() -> PolicyDoc:
    """Patient identification (two-identifier) policy."""
    return PolicyDoc(
        number="POL-PS-008",
        title="Patient Identification",
        owner="Patient Safety / Nursing",
        effective="2023-01-10",
        revised="2026-01-30",
        review="2028-01-30",
        version="2.6",
        approved_by=_APPROVER,
        applies_to="All staff at every point of care, treatment, and service",
        keywords=[
            "patient identification",
            "two identifiers",
            "wristband",
            "misidentification",
            "NPSG",
            "specimen labeling",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To reliably identify the individual as the person for whom "
                        "a service or treatment is intended and to match the service "
                        "or treatment to that individual, per The Joint Commission "
                        "NPSG.01.01.01."
                    ),
                ],
            ),
            Section(
                "Policy",
                [
                    Bullets(
                        [
                            "Use at least two patient identifiers — typically full "
                            "name and date of birth, or name and medical record "
                            "number — before any care, treatment, medication, blood, "
                            "specimen collection, or procedure.",
                            "A room or bed number is never an acceptable identifier.",
                            "Actively confirm identifiers with the patient when "
                            "possible (ask them to state name and date of birth) "
                            "rather than reading them aloud for confirmation.",
                            "Label specimens in the presence of the patient, at the "
                            "point of collection.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "A misidentification that reaches the patient (wrong patient "
                        "treated, wrong specimen resulted, wrong blood administered) "
                        "is at least SEV-2 and, where it causes serious harm or "
                        "involves blood, SEV-1. An identification error caught before "
                        "reaching the patient is a Near Miss and is still reported "
                        "under POL-RM-013."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission, NPSG.01.01.01 — Identify Patients "
                            "Correctly.",
                            "Related: POL-SURG-007, POL-LAB-006, POL-RM-013.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_pressure_injury() -> PolicyDoc:
    """Hospital-acquired pressure injury prevention and staging."""
    return PolicyDoc(
        number="POL-NUR-009",
        title="Hospital-Acquired Pressure Injury Prevention and Staging",
        owner="Nursing / Wound, Ostomy & Continence (WOCN)",
        effective="2023-08-01",
        revised="2026-03-10",
        review="2028-03-10",
        version="3.3",
        approved_by=_APPROVER,
        applies_to="All inpatient and observation units",
        keywords=[
            "pressure injury",
            "pressure ulcer",
            "HAPI",
            "staging",
            "NPIAP",
            "Braden",
            "skin assessment",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To prevent hospital-acquired pressure injuries (HAPIs) "
                        "through risk assessment and skin care, and to stage injuries "
                        "consistently using the NPIAP staging system."
                    ),
                ],
            ),
            Section(
                "Policy — Assessment and Prevention",
                [
                    Bullets(
                        [
                            "Complete a head-to-toe skin assessment and a Braden Scale "
                            "risk assessment on admission, every shift, and on change "
                            "in condition.",
                            "Implement a prevention bundle for at-risk patients: "
                            "repositioning schedule, pressure-redistribution surface, "
                            "moisture management, and nutrition review.",
                            "A pressure injury present on admission is documented as "
                            "such; one that develops after admission is "
                            "hospital-acquired.",
                        ]
                    ),
                ],
            ),
            Section(
                "NPIAP Staging",
                [
                    TableBlock(
                        headers=["Stage", "Description"],
                        rows=[
                            [
                                "Stage 1",
                                "Intact skin with localized non-blanchable "
                                "erythema.",
                            ],
                            [
                                "Stage 2",
                                "Partial-thickness skin loss with exposed "
                                "dermis; may present as an intact or ruptured "
                                "serum-filled blister.",
                            ],
                            [
                                "Stage 3",
                                "Full-thickness skin loss; adipose (fat) "
                                "visible; no exposed fascia, muscle, tendon, or bone.",
                            ],
                            [
                                "Stage 4",
                                "Full-thickness skin and tissue loss with "
                                "exposed or palpable fascia, muscle, tendon, ligament, "
                                "cartilage, or bone.",
                            ],
                            [
                                "Unstageable",
                                "Full-thickness loss obscured by slough "
                                "or eschar so depth cannot be confirmed.",
                            ],
                            [
                                "Deep Tissue Pressure Injury",
                                "Persistent "
                                "non-blanchable deep red, maroon, or purple "
                                "discoloration, or a blood-filled blister.",
                            ],
                        ],
                        col_widths=[1.5 * inch, 4.3 * inch],
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Note(
                        "A hospital-acquired Stage 3, Stage 4, or unstageable "
                        "pressure injury is a Serious Reportable Event and is "
                        "classified SEV-1. Stage 2 HAPIs are SEV-2. Notify the "
                        "attending provider and the WOCN nurse, and file an event "
                        "report per POL-RM-013."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "NPIAP, Pressure Injury Staging System (2016 revision).",
                            "National Quality Forum, Serious Reportable Events — "
                            "Stage 3/4 and unstageable HAPI.",
                            "Related: POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_elopement() -> PolicyDoc:
    """Patient elopement / missing patient response."""
    return PolicyDoc(
        number="POL-SEC-010",
        title="Patient Elopement and Missing Patient Response",
        owner="Security / Nursing / Emergency Management",
        effective="2023-10-01",
        revised="2026-02-05",
        review="2028-02-05",
        version="2.4",
        approved_by=_APPROVER,
        applies_to="All units; coordinated with Security and the "
        "Administrator-on-Call",
        keywords=[
            "elopement",
            "missing patient",
            "code green",
            "wander",
            "AWOL",
            "search",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To standardize the response when a patient who lacks the "
                        "capacity to make a safe decision to leave, or who is at risk "
                        "to self or others, is missing from the care area."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Elopement</b> — a patient who is unsafe to be left "
                            "unsupervised leaves the unit or facility without staff "
                            "knowledge.",
                            "<b>Missing patient</b> — a patient cannot be located "
                            "within the care area.",
                            "<b>Code Green</b> — the facility overhead alert for an "
                            "elopement / missing at-risk patient.",
                        ]
                    ),
                ],
            ),
            Section(
                "Immediate Response",
                [
                    Steps(
                        [
                            "Perform a rapid search of the immediate area (room, "
                            "bathroom, unit).",
                            "Notify the charge nurse and Security immediately with "
                            "the patient's name, description, last-known location, "
                            "and time last seen.",
                            "Initiate an overhead Code Green and notify the "
                            "Administrator-on-Call; Security coordinates a facility "
                            "and grounds search.",
                            "Notify the attending provider and, as appropriate, the "
                            "patient's family and law enforcement.",
                            "File an event report per POL-RM-013; a missing at-risk "
                            "patient is at least SEV-2 and is SEV-1 if the patient is "
                            "harmed or is a danger to self/others.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission, Environment of Care and Emergency "
                            "Management standards.",
                            "Facility Emergency Operations Plan — overhead code "
                            "standards.",
                            "Related: POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_workplace_violence() -> PolicyDoc:
    """Workplace violence prevention and reporting."""
    return PolicyDoc(
        number="POL-EH-011",
        title="Workplace Violence Prevention and Reporting",
        owner="Environmental Health & Safety · Employee Health · Security",
        effective="2023-11-01",
        revised="2026-03-12",
        review="2028-03-12",
        version="2.2",
        approved_by="Environmental Health & Safety Committee",
        applies_to="All staff, in all areas, including violence from patients, "
        "visitors, and coworkers",
        keywords=[
            "workplace violence",
            "staff safety",
            "assault",
            "OSHA general duty",
            "code gray",
            "security",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To protect staff from workplace violence (WPV) through "
                        "prevention, de-escalation, response, and consistent "
                        "reporting, consistent with the OSHA General Duty Clause and "
                        "OSHA's healthcare WPV guidelines (Publication 3148)."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Workplace violence</b> — any act or threat of "
                            "physical violence, harassment, intimidation, or "
                            "threatening behavior occurring at the worksite.",
                            "<b>Code Gray</b> — the facility alert for a combative or "
                            "threatening person requiring a team response.",
                        ]
                    ),
                ],
            ),
            Section(
                "Response and Reporting",
                [
                    Steps(
                        [
                            "Ensure personal safety and the safety of others; call a "
                            "Code Gray and Security for any imminent threat.",
                            "Use approved de-escalation techniques; restraint is a "
                            "last resort governed by POL-NUR-005.",
                            "Obtain medical evaluation for any injured staff through "
                            "Employee Health or the ED.",
                            "File an event report per POL-RM-013 for every WPV event, "
                            "including verbal threats and near misses — "
                            "non-punitive and expected.",
                        ]
                    ),
                    Note(
                        "An assault causing injury is at least SEV-2. OSHA severe-"
                        "injury reporting applies to the facility: a work-related "
                        "fatality is reported to OSHA within 8 hours, and any "
                        "in-patient hospitalization, amputation, or loss of an eye "
                        "within 24 hours — coordinated by EH&S."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "OSH Act, Section 5(a)(1) — General Duty Clause.",
                            "OSHA Publication 3148 — Guidelines for Preventing "
                            "Workplace Violence for Healthcare and Social Service "
                            "Workers.",
                            "OSHA 29 CFR 1904 — recording and reporting of "
                            "occupational injuries.",
                            "Related: POL-NUR-005, POL-RM-013.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_emtala() -> PolicyDoc:
    """EMTALA compliance — medical screening and transfer."""
    return PolicyDoc(
        number="POL-ED-012",
        title="EMTALA Compliance: Medical Screening and Transfer",
        owner="Emergency Department / Medical Staff / Compliance",
        effective="2023-01-20",
        revised="2026-01-25",
        review="2028-01-25",
        version="3.5",
        approved_by="Medical Executive Committee",
        applies_to="The Emergency Department, on-call medical staff, and any "
        "dedicated emergency service",
        keywords=[
            "EMTALA",
            "medical screening exam",
            "emergency medical condition",
            "stabilize",
            "transfer",
            "anti-dumping",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To ensure compliance with the Emergency Medical Treatment "
                        "and Active Labor Act (42 USC 1395dd) so that any individual "
                        "who comes to the ED receives an appropriate medical "
                        "screening examination and stabilizing treatment regardless "
                        "of ability to pay."
                    ),
                ],
            ),
            Section(
                "Policy",
                [
                    Bullets(
                        [
                            "Any individual who comes to the ED and requests "
                            "examination or treatment receives a medical screening "
                            "examination (MSE) within the hospital's capability to "
                            "determine whether an emergency medical condition (EMC) "
                            "exists — including active labor.",
                            "If an EMC exists, provide treatment to stabilize within "
                            "the hospital's capability, or arrange an appropriate "
                            "transfer.",
                            "Registration and the MSE must not be delayed to inquire "
                            "about insurance or payment.",
                        ]
                    ),
                ],
            ),
            Section(
                "Appropriate Transfer",
                [
                    Para(
                        "An individual with an unstabilized EMC may be transferred "
                        "only when the patient requests transfer after being informed "
                        "of the risks, or a physician certifies that the medical "
                        "benefits outweigh the risks; the receiving facility has "
                        "space, qualified personnel, and has accepted the patient; "
                        "and records, qualified personnel, and equipment accompany "
                        "the patient."
                    ),
                    Note(
                        "An EMTALA violation (e.g., failure to provide an MSE, or an "
                        "inappropriate transfer) is a SEV-1 compliance event. Notify "
                        "the ED Medical Director, Risk Management, and Compliance "
                        "immediately; Compliance coordinates any required reporting to "
                        "CMS."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "EMTALA, 42 USC 1395dd; 42 CFR 489.24.",
                            "CMS State Operations Manual, Appendix V — "
                            "Responsibilities of Medicare-Participating Hospitals in "
                            "Emergency Cases.",
                            "Related: POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_hazmat() -> PolicyDoc:
    """Hazardous material spill and chemical exposure."""
    return PolicyDoc(
        number="POL-EH-014",
        title="Hazardous Material Spill and Chemical Exposure",
        owner="Environmental Health & Safety",
        effective="2023-12-01",
        revised="2026-02-18",
        review="2028-02-18",
        version="2.1",
        approved_by="Environmental Health & Safety Committee",
        applies_to="All staff handling hazardous drugs, chemicals, or compressed "
        "gases",
        keywords=[
            "hazardous material",
            "spill",
            "chemical exposure",
            "hazardous drug",
            "SDS",
            "code orange",
            "decontamination",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To protect staff, patients, and the environment during "
                        "hazardous material spills and chemical exposures, consistent "
                        "with the OSHA Hazard Communication Standard (29 CFR 1910.1200) "
                        "and USP <800> for hazardous drugs."
                    ),
                ],
            ),
            Section(
                "Immediate Response",
                [
                    Steps(
                        [
                            "Protect yourself and others; evacuate the immediate area "
                            "if the spill is large, volatile, or unknown.",
                            "For a large or hazardous spill, call a Code Orange and "
                            "notify EH&S; do not attempt cleanup beyond your training "
                            "or without the correct PPE.",
                            "Consult the Safety Data Sheet (SDS) for the specific "
                            "agent before cleanup; use the spill kit appropriate to "
                            "the hazard class.",
                            "For skin/eye exposure, flush the affected area with water "
                            "for at least 15 minutes and report to Employee Health or "
                            "the ED.",
                            "File an event report per POL-RM-013.",
                        ]
                    ),
                    Note(
                        "A chemical exposure causing injury, or any hazardous-drug "
                        "spill reaching a patient, is at least SEV-2. Escalate "
                        "immediately for respiratory symptoms, large volatile spills, "
                        "or unknown agents."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "OSHA Hazard Communication Standard, 29 CFR 1910.1200.",
                            "USP General Chapter <800> — Hazardous Drugs Handling in "
                            "Healthcare Settings.",
                            "Related: POL-EH-001, POL-RM-013.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_corpus() -> list[PolicyDoc]:
    """Return the full policy corpus.

    The core policies defined in this module are concatenated with the themed
    batches (infection prevention, medication safety, clinical deterioration,
    emergency management, patient care, safety/workforce, compliance), each of
    which exposes a ``build_batch()`` returning its own list.

    Returns:
        list[PolicyDoc]: Every policy document to render.

    Raises:
        ValueError: If any two policies share a policy number.
    """
    # Imported here (not at module top) to keep the batch modules optional and
    # avoid any import ordering concerns with the shared model.
    import policy_content_clinical
    import policy_content_compliance
    import policy_content_emergency
    import policy_content_infection
    import policy_content_medication
    import policy_content_patientcare
    import policy_content_safety

    core = [
        build_incident_reporting(),
        build_bloodborne(),
        build_falls(),
        build_medication(),
        build_sentinel(),
        build_restraint(),
        build_transfusion(),
        build_universal_protocol(),
        build_patient_id(),
        build_pressure_injury(),
        build_elopement(),
        build_workplace_violence(),
        build_emtala(),
        build_hazmat(),
    ]

    batches = [
        policy_content_infection.build_batch(),
        policy_content_medication.build_batch(),
        policy_content_clinical.build_batch(),
        policy_content_emergency.build_batch(),
        policy_content_patientcare.build_batch(),
        policy_content_safety.build_batch(),
        policy_content_compliance.build_batch(),
    ]

    corpus = core + [doc for batch in batches for doc in batch]

    seen: dict[str, str] = {}
    for doc in corpus:
        if doc.number in seen:
            raise ValueError(
                f"Duplicate policy number {doc.number}: "
                f"{seen[doc.number]!r} and {doc.title!r}"
            )
        seen[doc.number] = doc.title

    return corpus
