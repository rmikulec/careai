"""Clinical-deterioration and acute-response batch of the policy corpus.

This module holds seven interlocking clinical policies for the fictional
Riverside Regional Medical Center that govern the recognition of and response to
acutely unwell patients: rapid response / code blue resuscitation, early-warning
scoring, critical-value reporting, massive transfusion, VTE prophylaxis, contrast
reaction management, and latex allergy management. Each is anchored to the real
standard it operationalizes (AHA ACLS/BLS, Royal College NEWS2, The Joint
Commission NPSG critical-results reporting, AABB massive-transfusion literature,
CHEST/ACCP VTE prophylaxis with Caprini/Padua scoring, the ACR Manual on Contrast
Media, and CDC/ASA latex guidance) and routes severity and notification through
the facility-wide scheme defined in POL-RM-013 so the Incident Reporting Agent can
ground its decisions consistently across the corpus.
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

_APPROVER_RESUS = "Code Blue / Resuscitation Committee"
_APPROVER_SAFETY = "Patient Safety & Quality Committee"


def build_code_blue() -> PolicyDoc:
    """Rapid response and code blue (CPR) activation and resuscitation."""
    return PolicyDoc(
        number="POL-CLN-040",
        title="Rapid Response and Code Blue (Cardiopulmonary Resuscitation)",
        owner="Resuscitation Committee / Nursing",
        effective="2024-02-01",
        revised="2026-03-12",
        review="2028-03-12",
        version="3.1",
        approved_by=_APPROVER_RESUS,
        applies_to="All clinical staff and first responders in all inpatient and "
        "outpatient areas of the facility",
        keywords=[
            "code blue",
            "cardiac arrest",
            "rapid response",
            "cpr",
            "acls",
            "bls",
            "resuscitation",
            "defibrillation",
            "crash cart",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To establish a standardized, time-critical response to "
                        "cardiopulmonary arrest (Code Blue) and to clinical "
                        "deterioration that has not yet progressed to arrest (Rapid "
                        "Response), so that high-quality basic and advanced life "
                        "support reaches the patient without delay. This policy "
                        "operationalizes the current American Heart Association (AHA) "
                        "BLS and ACLS guidelines."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to any patient, visitor, or staff member found "
                        "pulseless and/or apneic (Code Blue) or showing signs of "
                        "acute deterioration short of arrest (Rapid Response Team, "
                        "RRT). Any staff member may activate either response; "
                        "activation is never to be delayed for supervisory approval."
                    ),
                ],
            ),
            Section(
                "Activation Criteria",
                [
                    Para(
                        "Call a <b>Code Blue</b> (dial 55) for unresponsiveness with "
                        "absent or abnormal breathing and no definite pulse within 10 "
                        "seconds. Call the <b>Rapid Response Team</b> (dial 66) for "
                        "any of the following, or for any staff member who is simply "
                        "&ldquo;worried&rdquo; about the patient:"
                    ),
                    Bullets(
                        [
                            "Acute change in heart rate &lt; 40 or &gt; 130 bpm.",
                            "Systolic blood pressure &lt; 90 mmHg.",
                            "Respiratory rate &lt; 8 or &gt; 28 breaths/min.",
                            "SpO2 &lt; 90% despite supplemental oxygen.",
                            "Acute change in level of consciousness or new seizure.",
                            "A NEWS2 aggregate score &ge; 7, or any single parameter "
                            "scoring 3 (see POL-CLN-041).",
                        ]
                    ),
                    Note(
                        "If the patient is pulseless and/or not breathing normally, do "
                        "not wait for the team: call Code Blue (dial 55), start chest "
                        "compressions immediately at 100&ndash;120/min and a depth of "
                        "2&ndash;2.4 inches (5&ndash;6 cm), and attach the AED / "
                        "defibrillator as soon as it arrives. Every minute without CPR "
                        "and defibrillation reduces survival by roughly 7&ndash;10%."
                    ),
                ],
            ),
            Section(
                "Procedure — First Responder",
                [
                    Steps(
                        [
                            "Confirm unresponsiveness and shout for help; activate "
                            "Code Blue (dial 55) and note the time.",
                            "Begin high-quality CPR: compressions 100&ndash;120/min, "
                            "depth 5&ndash;6 cm, full chest recoil, minimize "
                            "interruptions (&lt; 10 seconds).",
                            "Open the airway and deliver ventilations at a 30:2 "
                            "compression-to-ventilation ratio until an advanced airway "
                            "is placed; thereafter ventilate once every 6 seconds.",
                            "Attach pads and analyze rhythm as soon as the "
                            "defibrillator arrives; defibrillate a shockable rhythm "
                            "(VF/pulseless VT) without delay, then resume compressions "
                            "immediately.",
                            "Rotate the compressor every 2 minutes (every rhythm "
                            "check) to limit fatigue.",
                            "Follow the ACLS cardiac-arrest algorithm: epinephrine 1 "
                            "mg IV/IO every 3&ndash;5 minutes; amiodarone 300 mg (then "
                            "150 mg) for refractory VF/pVT; and treat reversible "
                            "causes (the Hs and Ts).",
                        ]
                    ),
                ],
            ),
            Section(
                "Crash Cart and Equipment",
                [
                    Bullets(
                        [
                            "Crash carts are checked and lock-sealed every shift; a "
                            "broken seal mandates a full inventory and reseal.",
                            "Defibrillator self-test and battery are verified each "
                            "shift and logged.",
                            "A backboard, bag-valve-mask, and oxygen source are "
                            "immediately available at every care location.",
                        ]
                    ),
                ],
            ),
            Section(
                "Post-Event Documentation and Debrief",
                [
                    Bullets(
                        [
                            "Complete the code record / resuscitation flowsheet in "
                            "real time, including times of arrest, CPR start, first "
                            "shock, drugs, and return of spontaneous circulation "
                            "(ROSC) or termination.",
                            "Conduct a hot debrief with the team immediately after the "
                            "event.",
                            "Restock and reseal the crash cart before it returns to "
                            "service.",
                            "Submit an event report in the safety system per POL-RM-"
                            "013.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Classify and report every resuscitation event per the "
                        "facility-wide severity scale in POL-RM-013 (SEV-1 "
                        "catastrophic/sentinel; SEV-2 major; SEV-3 minor/no harm; Near "
                        "Miss)."
                    ),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "Unrecognized deterioration or failure to rescue "
                                "leading to death or permanent harm (sentinel event); "
                                "delayed CPR or missing/failed defibrillator.",
                                "Attending, Administrator-on-Call, and Risk "
                                "Management within 1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Resuscitation with delayed response or equipment gap "
                                "but patient recovered with major temporary harm.",
                                "Unit manager and Risk Management within 4 hours.",
                            ],
                            [
                                "SEV-3",
                                "Minor process deviation (e.g. late cart restock) with "
                                "no patient harm.",
                                "Unit manager within 24 hours via event report.",
                            ],
                            [
                                "Near Miss",
                                "Crash cart seal/equipment failure caught before a "
                                "code; deterioration intercepted in time.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[0.85 * inch, 3.05 * inch, 1.9 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3, None],
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "American Heart Association, Guidelines for CPR and "
                            "Emergency Cardiovascular Care (BLS and ACLS).",
                            "AHA Chain of Survival and cardiac-arrest algorithms.",
                            "Related: POL-CLN-041, POL-RM-013.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_early_warning() -> PolicyDoc:
    """Early warning score (NEWS2) and deteriorating-patient escalation."""
    return PolicyDoc(
        number="POL-CLN-041",
        title="Early Warning Score and Deteriorating Patient Escalation",
        owner="Nursing / Patient Safety",
        effective="2023-11-06",
        revised="2026-02-18",
        review="2028-02-18",
        version="2.3",
        approved_by=_APPROVER_SAFETY,
        applies_to="All nursing and medical staff caring for adult inpatients on "
        "general wards and in step-down units",
        keywords=[
            "early warning score",
            "news2",
            "mews",
            "deterioration",
            "escalation",
            "track and trigger",
            "rapid response",
            "vital signs",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To detect clinical deterioration early and trigger a timely, "
                        "graded clinical response using a standardized aggregate "
                        "track-and-trigger early-warning score. Riverside uses the "
                        "Royal College of Physicians National Early Warning Score "
                        "(NEWS2) for adult inpatients."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to all adult inpatients except those on an agreed "
                        "palliative/comfort-care pathway. NEWS2 is calculated at every "
                        "set of vital signs and whenever clinical concern arises; it "
                        "does not replace clinical judgment, and a worried clinician "
                        "may escalate regardless of score."
                    ),
                ],
            ),
            Section(
                "The NEWS2 Score",
                [
                    Para(
                        "NEWS2 aggregates seven physiological parameters: respiratory "
                        "rate, oxygen saturation (with a separate scale for patients "
                        "with target range 88&ndash;92%), supplemental oxygen, "
                        "temperature, systolic blood pressure, pulse, and level of "
                        "consciousness (ACVPU). Each parameter scores 0&ndash;3; a "
                        "score of 3 in any single parameter is itself a trigger."
                    ),
                ],
            ),
            Section(
                "Escalation Triggers and Response",
                [
                    Note(
                        "A NEWS2 aggregate score of 7 or more, or new confusion / "
                        "ACVPU other than Alert, is an emergency: immediately call the "
                        "Rapid Response Team (dial 66), begin continuous monitoring, "
                        "and do not leave the patient unattended. A patient scoring "
                        "&ge; 5 requires urgent clinical review within 30 minutes."
                    ),
                    TableBlock(
                        headers=[
                            "NEWS2 score",
                            "Risk / frequency",
                            "Response",
                        ],
                        rows=[
                            [
                                "0",
                                "Low; minimum 12-hourly.",
                                "Continue routine monitoring.",
                            ],
                            [
                                "1&ndash;4",
                                "Low; minimum 4&ndash;6-hourly.",
                                "Registered nurse assesses; decide whether to increase "
                                "frequency or escalate.",
                            ],
                            [
                                "3 in any one parameter",
                                "Low&ndash;medium; minimum hourly.",
                                "Urgent review by the ward doctor; consider escalation.",
                            ],
                            [
                                "5&ndash;6",
                                "Medium; minimum hourly.",
                                "Urgent review by a clinician within 30 min; consider "
                                "Rapid Response Team.",
                            ],
                            [
                                "7 or more",
                                "High; continuous monitoring.",
                                "Emergency: activate Rapid Response Team (dial 66); "
                                "critical-care assessment.",
                            ],
                        ],
                        col_widths=[1.4 * inch, 1.9 * inch, 2.5 * inch],
                        row_shades=[None, _SEV3, _SEV3, _SEV2, _SEV1],
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Record all seven parameters, the aggregate score, and "
                            "the monitoring frequency on the observation chart.",
                            "Document the time of each escalation, who was contacted, "
                            "and the response/plan.",
                            "Note any clinician decision to vary monitoring frequency "
                            "from the protocol, with the rationale.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Report escalation failures per POL-RM-013. A failure to "
                        "recognize or act on a rising score that leads to death or "
                        "permanent harm is a failure-to-rescue sentinel event."
                    ),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "Documented high score not escalated; unrecognized "
                                "deterioration leading to death or permanent harm "
                                "(sentinel event).",
                                "Attending, Administrator-on-Call, and Risk "
                                "Management within 1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Escalation delayed beyond protocol with major "
                                "temporary harm.",
                                "Unit manager and Risk Management within 4 hours.",
                            ],
                            [
                                "SEV-3",
                                "Missed or late observation set with no harm.",
                                "Unit manager within 24 hours via event report.",
                            ],
                            [
                                "Near Miss",
                                "High score caught and escalated promptly; no harm "
                                "reached the patient.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[0.85 * inch, 3.05 * inch, 1.9 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3, None],
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "Royal College of Physicians, National Early Warning "
                            "Score (NEWS2), updated report of a working party.",
                            "Related early-warning scoring literature (MEWS).",
                            "Related: POL-CLN-040, POL-RM-013.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_critical_values() -> PolicyDoc:
    """Critical value and critical test result reporting."""
    return PolicyDoc(
        number="POL-CLN-042",
        title="Critical Value and Critical Test Result Reporting",
        owner="Laboratory / Medical Staff",
        effective="2023-09-18",
        revised="2026-01-22",
        review="2028-01-22",
        version="3.0",
        approved_by=_APPROVER_SAFETY,
        applies_to="Laboratory, radiology, cardiodiagnostics staff and all "
        "licensed providers and nurses receiving results",
        keywords=[
            "critical value",
            "critical result",
            "panic value",
            "read-back",
            "npsg",
            "result reporting",
            "closed loop",
            "notification",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To ensure that critical results of tests and diagnostic "
                        "procedures are reported to the responsible licensed caregiver "
                        "on a timely basis so that the patient can be treated "
                        "promptly, satisfying The Joint Commission National Patient "
                        "Safety Goal on reporting critical results (NPSG.02.03.01)."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to all critical (life-threatening) values and "
                        "critical findings from the clinical laboratory, blood bank, "
                        "radiology, and cardiodiagnostics, whether the result is a "
                        "first occurrence or a repeat. Each discipline maintains a "
                        "defined critical-value list approved by the Medical Staff."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Critical value</b> &mdash; a result so far outside the "
                            "normal range that it represents a life-threatening "
                            "situation unless action is taken promptly.",
                            "<b>Read-back</b> &mdash; the receiver repeats the "
                            "verbally reported result and patient identifiers back to "
                            "the reporter, who confirms accuracy (closed-loop "
                            "communication).",
                            "<b>Responsible licensed caregiver</b> &mdash; the "
                            "ordering provider or a licensed designee able to act on "
                            "the result.",
                        ]
                    ),
                ],
            ),
            Section(
                "Procedure — Reporting a Critical Value",
                [
                    Steps(
                        [
                            "Verify the result and patient identity before calling.",
                            "Notify the responsible licensed caregiver by direct "
                            "verbal contact (in person or by phone) &mdash; never by "
                            "voicemail, text, or an unmonitored queue alone.",
                            "Use two patient identifiers and state the test, value, "
                            "and units.",
                            "Obtain a read-back of the result and identifiers and "
                            "confirm accuracy.",
                            "Document the result, date/time of the call, the names of "
                            "the reporter and receiver, and that read-back occurred.",
                            "If the caregiver cannot be reached, follow the escalation "
                            "call list until a licensed caregiver is reached.",
                        ]
                    ),
                    Note(
                        "A critical value must reach a licensed caregiver who can act "
                        "on it within the timeframe in the table below &mdash; "
                        "measured from result verification. If the first contact is "
                        "not reached, immediately move down the escalation list; a "
                        "critical value that is not communicated and acted upon is a "
                        "serious reporting failure under POL-RM-013."
                    ),
                ],
            ),
            Section(
                "Critical-Value Call List and Timeframes",
                [
                    TableBlock(
                        headers=[
                            "Tier",
                            "Contact",
                            "Target timeframe",
                        ],
                        rows=[
                            [
                                "1",
                                "Ordering provider (or covering provider).",
                                "Within 30 min of verification.",
                            ],
                            [
                                "2",
                                "Attending / responsible service if Tier 1 not "
                                "reached in 15 min.",
                                "Within 45 min of verification.",
                            ],
                            [
                                "3",
                                "Rapid Response Team or hospitalist on call if no "
                                "licensed caregiver reached.",
                                "Within 60 min of verification.",
                            ],
                        ],
                        col_widths=[0.6 * inch, 3.3 * inch, 1.9 * inch],
                        row_shades=[None, None, None],
                    ),
                    Para(
                        "Representative critical values include potassium &lt; 2.8 or "
                        "&gt; 6.0 mmol/L, glucose &lt; 40 or &gt; 500 mg/dL, "
                        "hemoglobin &lt; 7 g/dL, platelets &lt; 20 &times; 10<super>9</super>/L, "
                        "INR &gt; 5.0, troponin above the facility threshold, and "
                        "radiology findings such as new intracranial hemorrhage or "
                        "pulmonary embolism."
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Report breakdowns in critical-result communication per "
                        "POL-RM-013."
                    ),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "Critical value not communicated or not acted upon, "
                                "contributing to death or permanent harm (sentinel "
                                "event).",
                                "Attending, Administrator-on-Call, and Risk "
                                "Management within 1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Critical value reported late / to the wrong patient "
                                "record with major temporary harm or required rescue "
                                "treatment.",
                                "Lab director and Risk Management within 4 hours.",
                            ],
                            [
                                "SEV-3",
                                "Read-back omitted or late report with no patient "
                                "harm.",
                                "Supervisor within 24 hours via event report.",
                            ],
                            [
                                "Near Miss",
                                "Result flagged and corrected before reaching the "
                                "chart; no action taken on erroneous value.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[0.85 * inch, 3.05 * inch, 1.9 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3, None],
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission, National Patient Safety Goal "
                            "NPSG.02.03.01 &mdash; report critical results of tests "
                            "and diagnostic procedures on a timely basis.",
                            "Related: POL-CLN-043, POL-RM-013.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_massive_transfusion() -> PolicyDoc:
    """Massive transfusion protocol (MTP) activation and management."""
    return PolicyDoc(
        number="POL-CLN-043",
        title="Massive Transfusion Protocol",
        owner="Blood Bank / Trauma Services",
        effective="2024-03-04",
        revised="2026-04-09",
        review="2028-04-09",
        version="2.2",
        approved_by=_APPROVER_SAFETY,
        applies_to="Emergency department, operating rooms, obstetrics, ICU, blood "
        "bank, and trauma team staff",
        keywords=[
            "massive transfusion",
            "mtp",
            "hemorrhage",
            "trauma",
            "blood bank",
            "prbc",
            "ffp",
            "platelets",
            "1:1:1",
            "tranexamic acid",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To provide rapid, balanced delivery of blood components for "
                        "patients with life-threatening hemorrhage, minimizing the "
                        "coagulopathy of trauma and shock. This protocol reflects "
                        "current AABB and massive-transfusion literature favoring a "
                        "balanced 1:1:1 ratio of plasma, platelets, and red cells."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to adult patients with, or at high risk of, massive "
                        "hemorrhage &mdash; defined as transfusion of &ge; 10 units of "
                        "red cells in 24 hours, &ge; 4 units in 1 hour with ongoing "
                        "bleeding, or an Assessment of Blood Consumption (ABC) score "
                        "&ge; 2. Pediatric and obstetric variants are addressed in "
                        "unit-specific appendices."
                    ),
                ],
            ),
            Section(
                "Activation",
                [
                    Steps(
                        [
                            "Any physician or the trauma team leader may activate the "
                            "MTP by calling the Blood Bank (dial 44) and stating "
                            "&ldquo;Activate MTP&rdquo; with the patient location and "
                            "two identifiers.",
                            "Send a type-and-crossmatch sample immediately if not "
                            "already on file; emergency-release group O red cells are "
                            "issued until the sample resolves.",
                            "Assign a runner to shuttle coolers between the bedside "
                            "and the Blood Bank.",
                            "Draw a baseline CBC, coagulation panel, fibrinogen, "
                            "ionized calcium, and arterial blood gas.",
                        ]
                    ),
                    Note(
                        "Give tranexamic acid (TXA) 1 g IV over 10 minutes as early as "
                        "possible &mdash; ideally within 3 hours of injury &mdash; "
                        "followed by 1 g over 8 hours. Benefit falls sharply with "
                        "delay, and TXA given beyond 3 hours after injury may increase "
                        "mortality."
                    ),
                ],
            ),
            Section(
                "Component Ratios and Pack Contents",
                [
                    Para(
                        "The Blood Bank issues components in pre-defined packs to "
                        "maintain an approximately 1:1:1 ratio of plasma to platelets "
                        "to red cells. Transfuse through a warmer with a rapid "
                        "infuser; monitor for citrate-induced hypocalcemia."
                    ),
                    TableBlock(
                        headers=[
                            "MTP pack",
                            "Red cells",
                            "Plasma",
                            "Platelets",
                        ],
                        rows=[
                            ["Pack 1", "6 units", "6 units", "1 apheresis dose"],
                            ["Pack 2", "6 units", "6 units", "1 apheresis dose"],
                            [
                                "Adjuncts",
                                "Cryoprecipitate if fibrinogen &lt; 150 mg/dL",
                                "Calcium for ionized Ca<super>2+</super> &lt; 1.1 mmol/L",
                                "TXA per above",
                            ],
                        ],
                        col_widths=[1.0 * inch, 1.6 * inch, 1.6 * inch, 1.6 * inch],
                        row_shades=[None, None, _SEV3],
                    ),
                ],
            ),
            Section(
                "Targets and Termination",
                [
                    Bullets(
                        [
                            "Target fibrinogen &ge; 150 mg/dL, platelets &ge; 50 "
                            "&times; 10<super>9</super>/L, INR &lt; 1.5, ionized calcium &ge; "
                            "1.1 mmol/L, temperature &ge; 36&deg;C, and pH &ge; 7.2.",
                            "Reassess with repeat labs after every pack or every "
                            "30&ndash;60 minutes.",
                            "The treating physician deactivates the MTP by notifying "
                            "the Blood Bank once hemostasis is achieved; return unused "
                            "components promptly.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Report MTP events and transfusion reactions per POL-RM-013; "
                        "transfusion reactions also follow the facility hemovigilance "
                        "process."
                    ),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "ABO-incompatible transfusion or MTP delay/failure "
                                "contributing to death or permanent harm (sentinel "
                                "event).",
                                "Attending, Administrator-on-Call, and Risk "
                                "Management within 1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Acute transfusion reaction or component-delivery delay "
                                "with major temporary harm.",
                                "Blood Bank medical director and Risk Management "
                                "within 4 hours.",
                            ],
                            [
                                "SEV-3",
                                "Protocol deviation (e.g. ratio error) with no patient "
                                "harm.",
                                "Blood Bank supervisor within 24 hours via event "
                                "report.",
                            ],
                            [
                                "Near Miss",
                                "Mislabeled sample or wrong unit intercepted before "
                                "transfusion.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[0.85 * inch, 3.05 * inch, 1.9 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3, None],
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "AABB (Association for the Advancement of Blood & "
                            "Biotherapies) standards and massive-transfusion guidance.",
                            "Balanced-resuscitation (1:1:1) trial literature and "
                            "CRASH-2 (tranexamic acid) evidence.",
                            "Related: POL-CLN-042, POL-RM-013.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_vte_prophylaxis() -> PolicyDoc:
    """Venous thromboembolism (VTE) prophylaxis and risk assessment."""
    return PolicyDoc(
        number="POL-CLN-044",
        title="Venous Thromboembolism (VTE) Prophylaxis",
        owner="Medical Staff / Pharmacy",
        effective="2023-07-11",
        revised="2026-03-27",
        review="2028-03-27",
        version="2.1",
        approved_by=_APPROVER_SAFETY,
        applies_to="All licensed providers, pharmacists, and nurses caring for "
        "admitted adult medical and surgical patients",
        keywords=[
            "vte prophylaxis",
            "dvt",
            "pulmonary embolism",
            "caprini",
            "padua",
            "anticoagulation",
            "heparin",
            "enoxaparin",
            "mechanical prophylaxis",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To reduce hospital-associated venous thromboembolism (deep "
                        "vein thrombosis and pulmonary embolism) through structured "
                        "risk assessment and appropriate pharmacologic and/or "
                        "mechanical prophylaxis, consistent with CHEST/ACCP "
                        "antithrombotic guidelines."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to every admitted adult patient. A VTE risk "
                        "assessment and a bleeding-risk assessment are completed on "
                        "admission, on transfer between levels of care, and at least "
                        "every 24 hours thereafter or when clinical status changes."
                    ),
                ],
            ),
            Section(
                "Risk Assessment",
                [
                    Para(
                        "Use the <b>Padua Prediction Score</b> for medical patients "
                        "and the <b>Caprini Risk Assessment Model</b> for surgical "
                        "patients. A Padua score &ge; 4 indicates high VTE risk; "
                        "Caprini risk rises in steps with the cumulative score. Always "
                        "pair the VTE risk score with a bleeding-risk assessment "
                        "before prescribing pharmacologic prophylaxis."
                    ),
                    TableBlock(
                        headers=[
                            "Model / score",
                            "Risk tier",
                            "Recommended prophylaxis",
                        ],
                        rows=[
                            [
                                "Padua &lt; 4 / Caprini 0&ndash;2",
                                "Low",
                                "Early ambulation; reassess daily.",
                            ],
                            [
                                "Caprini 3&ndash;4",
                                "Moderate",
                                "Pharmacologic or mechanical prophylaxis per bleeding "
                                "risk.",
                            ],
                            [
                                "Padua &ge; 4 / Caprini &ge; 5",
                                "High",
                                "Pharmacologic prophylaxis unless contraindicated; add "
                                "mechanical if high bleeding risk.",
                            ],
                        ],
                        col_widths=[2.0 * inch, 1.0 * inch, 2.8 * inch],
                        row_shades=[_SEV3, _SEV2, _SEV1],
                    ),
                ],
            ),
            Section(
                "Prophylaxis Options",
                [
                    Bullets(
                        [
                            "<b>Pharmacologic</b>: enoxaparin 40 mg subcutaneously "
                            "once daily (adjust for weight and renal function), or "
                            "unfractionated heparin 5,000 units subcutaneously every "
                            "8&ndash;12 hours.",
                            "<b>Mechanical</b>: intermittent pneumatic compression "
                            "devices and/or graduated compression stockings when "
                            "pharmacologic prophylaxis is contraindicated.",
                            "Reassess renal function, platelet count (for heparin-"
                            "induced thrombocytopenia), and bleeding daily.",
                        ]
                    ),
                    Note(
                        "Do not start or continue pharmacologic prophylaxis in a "
                        "patient with active major bleeding, platelets &lt; 50 &times; "
                        "10<super>9</super>/L, or another hard contraindication; use mechanical "
                        "prophylaxis instead and document the reason. Every high-risk "
                        "patient must have prophylaxis ordered or an explicit, "
                        "documented reason for omission within 24 hours of admission."
                    ),
                ],
            ),
            Section(
                "Monitoring and Reassessment",
                [
                    Bullets(
                        [
                            "Reassess VTE and bleeding risk at least every 24 hours "
                            "and at every transition of care.",
                            "Investigate new unilateral limb swelling, pleuritic chest "
                            "pain, dyspnea, or hypoxia for VTE promptly.",
                            "Provide VTE prophylaxis education and address at-discharge "
                            "extended prophylaxis where indicated.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Report prophylaxis omissions and hospital-associated VTE per "
                        "POL-RM-013."
                    ),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "Fatal or permanently disabling hospital-associated "
                                "PE/DVT after prophylaxis was indicated but not "
                                "ordered (sentinel-level event).",
                                "Attending, Administrator-on-Call, and Risk "
                                "Management within 1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Hospital-associated VTE with major temporary harm, or "
                                "bleeding from inappropriate prophylaxis.",
                                "Attending and Risk Management within 4 hours.",
                            ],
                            [
                                "SEV-3",
                                "Missed or late risk assessment with no patient harm.",
                                "Unit manager within 24 hours via event report.",
                            ],
                            [
                                "Near Miss",
                                "Omitted order caught by pharmacy/nursing and corrected "
                                "before any harm.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[0.85 * inch, 3.05 * inch, 1.9 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3, None],
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CHEST / ACCP, Antithrombotic Therapy for VTE Disease and "
                            "Prevention of VTE in Nonsurgical and Surgical Patients.",
                            "Padua Prediction Score (medical) and Caprini Risk "
                            "Assessment Model (surgical).",
                            "Related: POL-RM-013.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_contrast_reaction() -> PolicyDoc:
    """Contrast media reaction recognition and management."""
    return PolicyDoc(
        number="POL-CLN-045",
        title="Contrast Media Reaction Management",
        owner="Radiology / Nursing",
        effective="2023-10-02",
        revised="2026-02-05",
        review="2028-02-05",
        version="2.4",
        approved_by=_APPROVER_SAFETY,
        applies_to="Radiology technologists, nurses, and physicians involved in "
        "contrast-enhanced imaging",
        keywords=[
            "contrast reaction",
            "iodinated contrast",
            "gadolinium",
            "anaphylaxis",
            "epinephrine",
            "acr",
            "premedication",
            "extravasation",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To standardize the recognition and treatment of acute adverse "
                        "reactions to iodinated and gadolinium-based contrast media, "
                        "following the American College of Radiology (ACR) Manual on "
                        "Contrast Media."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to all areas where intravascular contrast is "
                        "administered. A provider able to manage an acute reaction and "
                        "an emergency cart with epinephrine must be immediately "
                        "available whenever contrast is injected."
                    ),
                ],
            ),
            Section(
                "Screening and Prevention",
                [
                    Bullets(
                        [
                            "Screen for prior contrast reaction, asthma, and renal "
                            "impairment (eGFR) before injection.",
                            "A prior moderate or severe allergic-like reaction is the "
                            "strongest predictor of a future reaction; consider a "
                            "premedication regimen (corticosteroid plus "
                            "antihistamine) and/or an alternative study.",
                            "Confirm two patient identifiers, agent, dose, and IV "
                            "patency before injection.",
                        ]
                    ),
                ],
            ),
            Section(
                "Reaction Severity and Treatment",
                [
                    Note(
                        "For any severe allergic-like reaction &mdash; laryngeal edema "
                        "with stridor, bronchospasm with hypoxia, or anaphylactic "
                        "shock &mdash; give intramuscular epinephrine 0.3 mg (0.3 mL "
                        "of 1 mg/mL) in the mid-outer thigh immediately, call a Code "
                        "Blue (dial 55), give high-flow oxygen, and run IV fluids. Do "
                        "not delay epinephrine to try antihistamines first."
                    ),
                    TableBlock(
                        headers=[
                            "Severity",
                            "Signs",
                            "First-line treatment",
                        ],
                        rows=[
                            [
                                "Mild",
                                "Limited urticaria/pruritus, nasal congestion, "
                                "sneezing, limited scratchy throat; self-limited.",
                                "Observe and reassure; oral/IV antihistamine if "
                                "bothersome.",
                            ],
                            [
                                "Moderate",
                                "Diffuse urticaria, facial edema without dyspnea, "
                                "wheezing/bronchospasm with mild or no hypoxia, stable "
                                "vitals.",
                                "Oxygen, IV fluids, antihistamine, inhaled "
                                "beta-agonist; monitor closely for progression.",
                            ],
                            [
                                "Severe",
                                "Laryngeal edema with stridor, bronchospasm with "
                                "hypoxia, diffuse erythema with hypotension, "
                                "anaphylactic shock.",
                                "IM epinephrine 0.3 mg, high-flow oxygen, rapid IV "
                                "fluids; call Code Blue.",
                            ],
                        ],
                        col_widths=[0.9 * inch, 2.55 * inch, 2.35 * inch],
                        row_shades=[_SEV3, _SEV2, _SEV1],
                    ),
                    Para(
                        "Treat contrast extravasation by stopping the injection, "
                        "elevating the limb, and applying cold compresses; escalate to "
                        "surgical consult for compartment syndrome, skin ulceration, "
                        "or a large-volume extravasation."
                    ),
                ],
            ),
            Section(
                "Post-Event Observation",
                [
                    Bullets(
                        [
                            "Observe patients who received epinephrine for a protracted "
                            "period and arrange appropriate monitoring for biphasic "
                            "reactions.",
                            "Document the agent, dose, reaction, treatment, times, and "
                            "outcome.",
                            "Flag the reaction prominently in the allergy record.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para("Report contrast reactions and management per POL-RM-013."),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "Severe reaction / anaphylaxis with cardiac arrest, "
                                "death, or permanent harm; contrast given despite a "
                                "documented severe prior reaction (sentinel event).",
                                "Attending, Administrator-on-Call, and Risk "
                                "Management within 1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Moderate/severe reaction requiring rescue treatment "
                                "with major temporary harm, or significant "
                                "extravasation.",
                                "Radiologist and Risk Management within 4 hours.",
                            ],
                            [
                                "SEV-3",
                                "Mild self-limited reaction; minor extravasation with "
                                "no harm.",
                                "Radiology supervisor within 24 hours via event "
                                "report.",
                            ],
                            [
                                "Near Miss",
                                "High-risk allergy history caught before injection; "
                                "wrong agent intercepted.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[0.85 * inch, 3.05 * inch, 1.9 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3, None],
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "American College of Radiology, ACR Manual on Contrast "
                            "Media (acute reaction classification and treatment).",
                            "Related: POL-CLN-040, POL-CLN-046, POL-RM-013.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_latex_allergy() -> PolicyDoc:
    """Latex allergy identification and management."""
    return PolicyDoc(
        number="POL-CLN-046",
        title="Latex Allergy Management",
        owner="Nursing / Perioperative Services",
        effective="2023-08-21",
        revised="2026-01-15",
        review="2028-01-15",
        version="2.0",
        approved_by=_APPROVER_SAFETY,
        applies_to="All clinical and support staff, with emphasis on perioperative, "
        "procedural, and emergency areas",
        keywords=[
            "latex allergy",
            "natural rubber latex",
            "anaphylaxis",
            "latex-safe",
            "perioperative",
            "sensitization",
            "cross-reactivity",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To prevent and manage reactions to natural rubber latex (NRL) "
                        "by identifying at-risk patients and staff and providing a "
                        "latex-safe environment, consistent with CDC/NIOSH and "
                        "American Society of Anesthesiologists (ASA) latex-allergy "
                        "guidance."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies throughout the facility and to all patient-care "
                        "products that may contain natural rubber latex. The facility "
                        "maintains a low-latex environment and a list of latex-"
                        "containing and latex-free alternative products."
                    ),
                ],
            ),
            Section(
                "Risk Identification",
                [
                    Bullets(
                        [
                            "Screen every patient for latex allergy at registration "
                            "and on admission.",
                            "Higher-risk groups: patients with spina bifida or "
                            "urogenital anomalies, those with multiple prior surgeries, "
                            "health-care workers, and people with known fruit cross-"
                            "reactivity (banana, avocado, kiwi, chestnut).",
                            "Distinguish true IgE-mediated latex allergy (Type I) from "
                            "irritant or allergic contact dermatitis (Type IV).",
                        ]
                    ),
                ],
            ),
            Section(
                "Latex-Safe Management",
                [
                    Steps(
                        [
                            "Flag the allergy in the medical record, wristband, and "
                            "door/room signage.",
                            "Remove latex-containing items from the patient&rsquo;s "
                            "environment and substitute latex-free alternatives.",
                            "Schedule procedures for a latex-allergic patient as the "
                            "first case of the day to minimize airborne latex-protein "
                            "exposure.",
                            "Use latex-free gloves, tourniquets, IV ports, and "
                            "medication vials/stoppers; stage a latex-free cart.",
                            "Communicate latex precautions at every handoff and to all "
                            "team members before the procedure.",
                        ]
                    ),
                    Note(
                        "A latex-allergic patient presenting with an acute Type I "
                        "reaction &mdash; urticaria progressing to wheeze, stridor, or "
                        "hypotension &mdash; is a medical emergency: remove all latex "
                        "source items immediately, give intramuscular epinephrine 0.3 "
                        "mg, call a Code Blue (dial 55), and provide oxygen and IV "
                        "fluids."
                    ),
                ],
            ),
            Section(
                "Staff Protection",
                [
                    Bullets(
                        [
                            "Provide powder-free, low-protein or non-latex gloves to "
                            "reduce sensitization.",
                            "Refer staff with suspected latex allergy to Employee "
                            "Health for evaluation and accommodation.",
                            "Report occupational latex reactions through the staff-"
                            "safety process in POL-RM-013.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para("Report latex exposures and reactions per POL-RM-013."),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "Latex-induced anaphylaxis with cardiac arrest, death, "
                                "or permanent harm; latex exposure of a documented "
                                "latex-allergic patient causing severe reaction "
                                "(sentinel event).",
                                "Attending, Administrator-on-Call, and Risk "
                                "Management within 1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Latex reaction requiring rescue treatment with major "
                                "temporary harm.",
                                "Attending and Risk Management within 4 hours.",
                            ],
                            [
                                "SEV-3",
                                "Minor localized reaction (e.g. contact dermatitis) "
                                "with no systemic harm.",
                                "Unit manager within 24 hours via event report.",
                            ],
                            [
                                "Near Miss",
                                "Latex item staged for an allergic patient but caught "
                                "and removed before use.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[0.85 * inch, 3.05 * inch, 1.9 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3, None],
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CDC / NIOSH, Preventing Allergic Reactions to Natural "
                            "Rubber Latex in the Workplace.",
                            "American Society of Anesthesiologists (ASA) guidance on "
                            "latex allergy.",
                            "Related: POL-CLN-045, POL-RM-013.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_batch() -> list[PolicyDoc]:
    """Return this batch's policies, in listed order."""
    return [
        build_code_blue(),
        build_early_warning(),
        build_critical_values(),
        build_massive_transfusion(),
        build_vte_prophylaxis(),
        build_contrast_reaction(),
        build_latex_allergy(),
    ]
