"""Patient-care policy batch for the hospital policy corpus.

This module holds the patient-care cluster of policy documents (POL-PC-060
through POL-PC-067): suicide risk, behavioral emergencies, pain management,
code status / advance directives, death and postmortem care, against-medical-
advice discharge, informed consent, and disclosure of unanticipated outcomes.
Each policy is fictional-facility prose for Riverside Regional Medical Center,
anchored to a real regulatory or accreditation standard and cross-referenced to
the master severity/reporting policy POL-RM-013 so the Incident Reporting Agent
can resolve severity and notification timing consistently across documents.
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


def build_suicide_risk() -> PolicyDoc:
    """Suicide risk assessment and management (NPSG.15.01.01 / Zero Suicide)."""
    return PolicyDoc(
        number="POL-PC-060",
        title="Suicide Risk Assessment and Management",
        owner="Behavioral Health / Nursing",
        effective="2023-07-15",
        revised="2026-02-12",
        review="2028-02-12",
        version="2.1",
        approved_by="Patient Safety & Quality Committee",
        applies_to="All patients 12 years and older treated for behavioral-health "
        "conditions, and any patient who screens positive for suicide risk, in "
        "all inpatient units and the Emergency Department",
        keywords=[
            "suicide risk",
            "suicide screening",
            "C-SSAS",
            "columbia",
            "self-harm",
            "ligature",
            "1:1 observation",
            "zero suicide",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To identify patients at risk for suicide and to protect them "
                        "through standardized screening, environmental safety, and "
                        "level-based precautions, consistent with The Joint Commission "
                        "National Patient Safety Goal NPSG.15.01.01 and the Zero "
                        "Suicide framework."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to all patients being evaluated or treated for "
                        "behavioral-health conditions as their primary reason for "
                        "care, and to any patient in any setting who screens positive "
                        "for suicidal ideation. Screening is completed on admission, "
                        "on transfer, on any change in condition, and before "
                        "discharge."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Suicidal ideation</b> — thoughts of engaging in "
                            "behavior intended to end one&rsquo;s life, ranging from a "
                            "passive wish to die to active intent with a plan.",
                            "<b>Ligature risk</b> — anything that could be used to "
                            "attach a cord, rope, or other material for the purpose of "
                            "hanging or strangulation.",
                            "<b>1:1 observation</b> — continuous, uninterrupted "
                            "line-of-sight monitoring by an assigned staff member who "
                            "remains within arm&rsquo;s reach as clinically indicated.",
                            "<b>Validated screening tool</b> — an evidence-based "
                            "instrument such as the Columbia-Suicide Severity Rating "
                            "Scale (C-SSRS) or the Ask Suicide-Screening Questions "
                            "(ASQ).",
                        ]
                    ),
                ],
            ),
            Section(
                "Risk Levels, Required Precautions, and Observation",
                [
                    Para(
                        "Assign a risk level from the validated screen and the "
                        "clinician&rsquo;s assessment. When findings could support two "
                        "levels, assign the higher level. Precautions are initiated "
                        "immediately and are not reduced without a provider order "
                        "documenting reassessment."
                    ),
                    TableBlock(
                        headers=[
                            "Risk level",
                            "Typical findings",
                            "Required precautions",
                        ],
                        rows=[
                            [
                                "<b>High</b>",
                                "Active ideation with plan and/or intent; recent "
                                "attempt; command hallucinations to self-harm.",
                                "Continuous 1:1 observation within arm&rsquo;s reach; "
                                "ligature-resistant environment; remove belongings and "
                                "personal items; search for contraband; behavioral-"
                                "health consult same day.",
                            ],
                            [
                                "<b>Moderate</b>",
                                "Active ideation without specific plan or intent; "
                                "significant risk factors; ambivalence.",
                                "Continuous line-of-sight observation; safe-room "
                                "placement; remove hazardous items; reassess at least "
                                "every shift; behavioral-health consult.",
                            ],
                            [
                                "<b>Low</b>",
                                "Passive ideation only; no plan, intent, or recent "
                                "attempt; protective factors present.",
                                "Routine observation with documented check frequency; "
                                "environmental review; reassess each shift and on any "
                                "change in condition.",
                            ],
                        ],
                        col_widths=[0.95 * inch, 2.25 * inch, 2.6 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "Immediate Management",
                [
                    Note(
                        "A patient who screens at high risk must never be left alone. "
                        "Initiate continuous 1:1 observation immediately, remove "
                        "ligature and sharp hazards and all personal belongings from "
                        "reach, and notify the attending provider and behavioral-"
                        "health on-call without delay. Do not wait for the formal "
                        "consult to begin precautions."
                    ),
                    Steps(
                        [
                            "Complete the validated screen and clinician assessment; "
                            "assign a risk level.",
                            "Initiate the required precautions for that level "
                            "immediately, including observation and environmental "
                            "safety.",
                            "Notify the attending provider and request a behavioral-"
                            "health consultation on the required timeline.",
                            "Document the screen, risk level, precautions, and "
                            "notifications; hand off risk level and precautions at "
                            "every care transition.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Events are classified and reported under POL-RM-013. An "
                        "inpatient suicide, or a suicide attempt resulting in serious "
                        "harm, is a sentinel event and is always SEV-1: notify the "
                        "attending provider, Charge Nurse, Nursing Supervisor, Risk "
                        "Management, and the Administrator-on-Call immediately and "
                        "within 1 hour, and manage per POL-RM-004 (RCA&sup2; within "
                        "45 business days). The elopement of a suicidal patient is "
                        "managed as a Code Green under POL-SEC-010 in addition to the "
                        "notifications here. Use of restraint or seclusion for a "
                        "behavioral emergency follows POL-NUR-005. A near miss (e.g., "
                        "contraband or a ligature intercepted before harm) is reported "
                        "within 24 hours."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Screening tool used, score, and assigned risk level, with "
                            "date and time.",
                            "Precautions initiated, observation level, and the "
                            "environmental safety review performed.",
                            "Provider and behavioral-health notifications (who, when, "
                            "by what method).",
                            "Reassessments, any change in risk level, and the order "
                            "supporting any reduction in precautions.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission, NPSG.15.01.01 — Reduce the risk for "
                            "suicide.",
                            "Zero Suicide framework (Suicide Prevention Resource "
                            "Center / EDC).",
                            "The Joint Commission, environmental risk reduction for "
                            "ligature and self-harm hazards.",
                            "Related: POL-NUR-005 (restraint & seclusion), POL-SEC-010 "
                            "(elopement), POL-RM-004 (sentinel events), POL-RM-013 "
                            "(severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_behavioral_emergency() -> PolicyDoc:
    """Behavioral emergency response and de-escalation (Code Gray)."""
    return PolicyDoc(
        number="POL-PC-061",
        title="Behavioral Emergency and De-escalation (Code Gray)",
        owner="Nursing / Security",
        effective="2023-09-15",
        revised="2026-02-22",
        review="2028-02-22",
        version="2.1",
        approved_by="Patient Safety & Quality Committee",
        applies_to="All staff in all patient-care and public areas; coordinated "
        "with Security and the Administrator-on-Call",
        keywords=[
            "behavioral emergency",
            "code gray",
            "de-escalation",
            "agitation",
            "crisis",
            "verbal intervention",
            "security",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To provide a safe, coordinated response to behavioral "
                        "emergencies that emphasizes early recognition and verbal "
                        "de-escalation, reserving physical intervention for imminent "
                        "danger, consistent with patient rights under CMS Conditions "
                        "of Participation (42 CFR 482.13)."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to any patient, visitor, or situation involving "
                        "escalating agitation or threatening behavior that risks the "
                        "safety of the patient, staff, or others, in any area of the "
                        "facility."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Behavioral emergency</b> — an acute disturbance of "
                            "behavior, thought, or mood that poses an imminent risk of "
                            "harm and requires an immediate response.",
                            "<b>Code Gray</b> — the facility overhead alert summoning "
                            "a trained behavioral-response team and Security for a "
                            "combative or threatening person.",
                            "<b>De-escalation</b> — verbal and nonverbal techniques "
                            "used to reduce agitation and restore the person&rsquo;s "
                            "ability to engage, without physical force.",
                        ]
                    ),
                ],
            ),
            Section(
                "De-escalation Approach",
                [
                    Bullets(
                        [
                            "Maintain a calm demeanor and a safe distance; keep an "
                            "unobstructed exit for yourself and the patient.",
                            "Use a single spokesperson, simple language, and a "
                            "respectful tone; acknowledge feelings and offer realistic "
                            "choices.",
                            "Reduce environmental stimulation; remove potential "
                            "weapons and bystanders from the area.",
                            "Set clear, non-threatening limits and allow time for the "
                            "person to respond.",
                        ]
                    ),
                ],
            ),
            Section(
                "Code Gray Response",
                [
                    Note(
                        "For any imminent threat of harm, call a Code Gray and "
                        "Security immediately and ensure staff and bystander safety "
                        "first. De-escalation is always attempted first; physical "
                        "intervention is a last resort. Restraint or seclusion for a "
                        "behavioral emergency is governed by POL-NUR-005 and requires "
                        "an order and a 1-hour face-to-face evaluation."
                    ),
                    Steps(
                        [
                            "Call a Code Gray; summon Security and the behavioral-"
                            "response team.",
                            "Clear the immediate area of other patients and visitors; "
                            "assign a single spokesperson to lead verbal "
                            "de-escalation.",
                            "Attempt de-escalation; offer voluntary medication and "
                            "support as clinically appropriate.",
                            "If imminent danger persists despite de-escalation, apply "
                            "restraint or seclusion only per POL-NUR-005.",
                            "After the event, provide medical evaluation for anyone "
                            "injured, debrief the team and patient, and file an event "
                            "report per POL-RM-013.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Events are classified and reported under POL-RM-013. A "
                        "behavioral emergency causing serious injury to a patient, "
                        "staff member, or visitor, or any death associated with "
                        "restraint or seclusion, is SEV-1 — notify the attending "
                        "provider, Charge Nurse, Nursing Supervisor, Risk Management, "
                        "and the Administrator-on-Call immediately and within 1 hour. "
                        "An assault or injury requiring treatment is SEV-2, reported "
                        "within 4 hours. A contained episode with no injury is SEV-3 "
                        "or a near miss, reported within 24 hours. Staff injury from "
                        "patient or visitor violence is additionally handled under "
                        "the workplace-violence policy."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Trigger and behavior observed; de-escalation techniques "
                            "attempted and the response.",
                            "Whether a Code Gray was called and who responded.",
                            "Any medication offered or given, and any restraint or "
                            "seclusion applied (cross-reference POL-NUR-005).",
                            "Injuries, notifications, and the post-event debrief.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CMS Conditions of Participation, 42 CFR 482.13 — "
                            "Patients&rsquo; Rights.",
                            "The Joint Commission, Provision of Care standards on "
                            "behavioral management and de-escalation.",
                            "Related: POL-NUR-005 (restraint & seclusion), POL-PC-060 "
                            "(suicide risk), POL-EH-011 (workplace violence), "
                            "POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_pain_management() -> PolicyDoc:
    """Pain assessment and management (Joint Commission pain standards)."""
    return PolicyDoc(
        number="POL-PC-062",
        title="Pain Assessment and Management",
        owner="Nursing / Pharmacy",
        effective="2023-05-01",
        revised="2026-03-04",
        review="2028-03-04",
        version="2.1",
        approved_by="Patient Safety & Quality Committee",
        applies_to="All patients in all inpatient, observation, emergency, and "
        "procedural settings",
        keywords=[
            "pain",
            "pain assessment",
            "reassessment",
            "opioid",
            "naloxone",
            "sedation",
            "oversedation",
            "pasero",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To assess and manage pain safely and effectively through "
                        "individualized, multimodal treatment and timely "
                        "reassessment, while monitoring for opioid-induced sedation "
                        "and respiratory depression, consistent with The Joint "
                        "Commission pain-assessment and pain-management standards."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to all patients. Pain is screened on admission and "
                        "assessed with an age- and condition-appropriate validated "
                        "tool, reassessed after every intervention, and documented."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Multimodal analgesia</b> — combining non-opioid "
                            "medications, non-pharmacologic methods, and opioids when "
                            "indicated to control pain while minimizing opioid dose.",
                            "<b>Sedation scale</b> — a validated scale (e.g., the "
                            "Pasero Opioid-Induced Sedation Scale, POSS) used to "
                            "detect advancing sedation before respiratory "
                            "depression.",
                            "<b>Opioid-induced respiratory depression</b> — "
                            "hypoventilation and hypoxia resulting from opioid effect, "
                            "a potentially fatal adverse event.",
                        ]
                    ),
                ],
            ),
            Section(
                "Reassessment Timeframes by Route",
                [
                    Para(
                        "Reassess pain, sedation level, and respiratory status after "
                        "each intervention within the timeframe matched to the "
                        "expected onset of the route used. Reassess sooner for any "
                        "sign of oversedation."
                    ),
                    TableBlock(
                        headers=["Route / intervention", "Reassess within"],
                        rows=[
                            ["Intravenous (IV) push opioid", "15–30 minutes"],
                            ["Subcutaneous / intramuscular", "30 minutes"],
                            ["Oral / enteral analgesic", "60 minutes"],
                            [
                                "Epidural / patient-controlled analgesia (PCA)",
                                "Per protocol; sedation & respirations hourly &times; "
                                "the first 12 hours",
                            ],
                            [
                                "Non-pharmacologic measure",
                                "60 minutes, or per the intervention",
                            ],
                        ],
                        col_widths=[3.3 * inch, 2.5 * inch],
                    ),
                ],
            ),
            Section(
                "Opioid Safety Monitoring",
                [
                    Note(
                        "Advancing sedation precedes opioid-induced respiratory "
                        "depression. If a patient is difficult to arouse, has a "
                        "declining sedation score, or shows a respiratory rate below "
                        "8 or oxygen desaturation, hold further opioids, stimulate "
                        "and support ventilation, administer naloxone per protocol, "
                        "and call for rapid response immediately."
                    ),
                    Bullets(
                        [
                            "Monitor sedation level and respiratory rate (and "
                            "capnography/oximetry where indicated) with each opioid "
                            "dose and during peak effect, more intensively for "
                            "opioid-naive, post-operative, and sleep-apnea patients.",
                            "Naloxone and reversal supplies are immediately "
                            "available wherever opioids are administered.",
                            "Avoid stacking opioids and concurrent sedatives without "
                            "reassessment between doses.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Events are classified and reported under POL-RM-013. "
                        "Opioid-induced respiratory depression requiring naloxone, "
                        "rapid response, or rescue is at least SEV-2 (SEV-1 if it "
                        "results in severe harm, permanent harm, or death) — notify "
                        "the attending provider and Risk Management, and for SEV-1 "
                        "the Nursing Supervisor and Administrator-on-Call, within 1 "
                        "hour. An under-treated-pain complaint or a late reassessment "
                        "without harm is SEV-3 or a near miss, reported within 24 "
                        "hours. Medication errors are additionally reported under the "
                        "medication-error policy."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Pain score with the tool used; location, quality, and "
                            "acceptable comfort/function goal.",
                            "Intervention given (drug, dose, route) and non-"
                            "pharmacologic measures.",
                            "Reassessment time and result, including sedation score "
                            "and respiratory status.",
                            "Any adverse effect, reversal given, and provider "
                            "notification.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission, pain-assessment and pain-management "
                            "standards (Provision of Care).",
                            "Pasero Opioid-Induced Sedation Scale (POSS).",
                            "CDC Clinical Practice Guideline for Prescribing Opioids "
                            "for Pain.",
                            "Related: POL-PS-003 (medication errors), POL-RM-013 "
                            "(severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_code_status() -> PolicyDoc:
    """Code status, DNR, and advance directives (PSDA / CMS 482.13)."""
    return PolicyDoc(
        number="POL-PC-063",
        title="Code Status, Do-Not-Resuscitate, and Advance Directives",
        owner="Medical Staff / Nursing",
        effective="2023-02-15",
        revised="2026-01-18",
        review="2028-01-18",
        version="2.1",
        approved_by="Ethics Committee",
        applies_to="All inpatients and observation patients; all licensed "
        "providers and nursing staff",
        keywords=[
            "code status",
            "DNR",
            "do not resuscitate",
            "advance directive",
            "living will",
            "POLST",
            "healthcare proxy",
            "surrogate",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To honor patients&rsquo; rights to make decisions about "
                        "resuscitation and life-sustaining treatment, to document code "
                        "status clearly, and to recognize advance directives, "
                        "consistent with the Patient Self-Determination Act and CMS "
                        "Conditions of Participation (42 CFR 482.13)."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to all patients. On admission, every patient is asked "
                        "whether they have an advance directive and is informed of "
                        "their right to make one; existing directives are obtained and "
                        "placed in the record."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Advance directive</b> — a written instruction, such as "
                            "a living will or a durable power of attorney for health "
                            "care, recognized under state law, stating a "
                            "person&rsquo;s wishes or naming an agent.",
                            "<b>Healthcare agent / proxy</b> — the person authorized "
                            "to make medical decisions when the patient lacks "
                            "capacity.",
                            "<b>POLST</b> — Physician/Provider Orders for "
                            "Life-Sustaining Treatment: portable medical orders for "
                            "seriously ill patients.",
                            "<b>Decision-making capacity</b> — the ability to "
                            "understand, appreciate, reason about, and communicate a "
                            "choice regarding a specific decision.",
                        ]
                    ),
                ],
            ),
            Section(
                "Code Status Definitions",
                [
                    Para(
                        "Code status is a provider order based on a documented "
                        "goals-of-care conversation with the patient or their "
                        "surrogate. In the absence of a valid order or directive, the "
                        "default is Full Code."
                    ),
                    TableBlock(
                        headers=["Code status", "Meaning"],
                        rows=[
                            [
                                "<b>Full Code</b>",
                                "All resuscitative measures, including chest "
                                "compressions, defibrillation, intubation, and "
                                "advanced cardiac life support.",
                            ],
                            [
                                "<b>DNR / DNAR</b>",
                                "Do Not Resuscitate / Attempt Resuscitation: no CPR or "
                                "ACLS in the event of cardiac or respiratory arrest; "
                                "all other indicated treatment continues.",
                            ],
                            [
                                "<b>DNI</b>",
                                "Do Not Intubate: no endotracheal intubation or "
                                "mechanical ventilation; other measures per the order.",
                            ],
                            [
                                "<b>Limited / partial</b>",
                                "Specific interventions elected or declined per a "
                                "documented order (e.g., defibrillation yes, "
                                "intubation no).",
                            ],
                        ],
                        col_widths=[1.5 * inch, 4.3 * inch],
                    ),
                ],
            ),
            Section(
                "Advance Directive Levels",
                [
                    TableBlock(
                        headers=["Instrument", "What it does"],
                        rows=[
                            [
                                "Living will",
                                "States the patient&rsquo;s wishes about "
                                "life-sustaining treatment if they become unable to "
                                "decide.",
                            ],
                            [
                                "Durable power of attorney for health care",
                                "Names a healthcare agent to make decisions when the "
                                "patient lacks capacity.",
                            ],
                            [
                                "POLST",
                                "Portable provider orders that travel with a seriously "
                                "ill patient across settings; actionable immediately.",
                            ],
                        ],
                        col_widths=[2.3 * inch, 3.5 * inch],
                    ),
                ],
            ),
            Section(
                "Honoring and Changing Code Status",
                [
                    Note(
                        "A DNR/DNAR order must be a current, documented provider "
                        "order in the medical record before resuscitation is withheld. "
                        "In the absence of a valid DNR order or an actionable "
                        "directive, staff must initiate full resuscitation. A patient "
                        "with capacity may change their code status at any time; "
                        "update the order immediately and communicate it to the care "
                        "team."
                    ),
                    Bullets(
                        [
                            "Confirm the code-status order at every handoff and "
                            "transfer of care.",
                            "If a patient lacks capacity and no directive or agent "
                            "exists, follow the state surrogate hierarchy and involve "
                            "the attending; consult the Ethics Committee for conflict "
                            "or uncertainty.",
                            "Reconcile any conflict between a directive, a POLST, and "
                            "the current order before acting, favoring the "
                            "patient&rsquo;s known current wishes.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Events are classified and reported under POL-RM-013. "
                        "Resuscitation performed contrary to a valid DNR order, or "
                        "resuscitation withheld without a valid order, is a SEV-1 "
                        "event — notify the attending provider, Charge Nurse, Nursing "
                        "Supervisor, Risk Management, and the Administrator-on-Call "
                        "immediately and within 1 hour. A documentation discrepancy "
                        "caught before it affects care is a near miss, reported within "
                        "24 hours. Any outcome resulting from a code-status error is "
                        "disclosed to the patient/family under POL-PC-067."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "Patient Self-Determination Act (42 USC 1395cc(f)).",
                            "CMS Conditions of Participation, 42 CFR 482.13 — "
                            "Patients&rsquo; Rights.",
                            "The Joint Commission, Provision of Care and "
                            "Rights-and-Responsibilities standards.",
                            "Related: POL-PC-067 (disclosure of unanticipated "
                            "outcomes), POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_death_pronouncement() -> PolicyDoc:
    """Death pronouncement and postmortem care (CMS CoP on death & autopsy)."""
    return PolicyDoc(
        number="POL-PC-064",
        title="Death Pronouncement and Postmortem Care",
        owner="Medical Staff / Nursing",
        effective="2023-04-15",
        revised="2026-02-26",
        review="2028-02-26",
        version="2.1",
        approved_by="Medical Executive Committee",
        applies_to="All inpatient units, the Emergency Department, and procedural "
        "areas; all licensed providers and nursing staff",
        keywords=[
            "death",
            "pronouncement",
            "postmortem care",
            "autopsy",
            "organ donation",
            "medical examiner",
            "coroner",
            "OPO",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To ensure a respectful, legally sound process for "
                        "pronouncing death, caring for the body, honoring the "
                        "family&rsquo;s wishes, and meeting organ-donation and "
                        "death-reporting obligations, consistent with CMS Conditions "
                        "of Participation on patient rights, organ/tissue donation, "
                        "and autopsy."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to the death of any patient within the facility. "
                        "Pronouncement is performed by a provider authorized under "
                        "state law and medical-staff privileges."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Pronouncement of death</b> — the clinical "
                            "determination and documentation that death has occurred, "
                            "by an authorized provider.",
                            "<b>Medical examiner / coroner case</b> — a death that by "
                            "law must be reported (e.g., unexpected, unexplained, "
                            "violent, or within a defined period of admission or a "
                            "procedure).",
                            "<b>OPO</b> — the federally designated Organ Procurement "
                            "Organization that must be notified of every death and "
                            "imminent death to evaluate donation suitability.",
                        ]
                    ),
                ],
            ),
            Section(
                "Procedure — Pronouncement and Immediate Notifications",
                [
                    Note(
                        "Every death and imminent death must be reported to the "
                        "designated Organ Procurement Organization in a timely manner "
                        "as required by CMS, before any approach to the family about "
                        "donation. Do not initiate the donation conversation with the "
                        "family until the OPO has been notified and directs or "
                        "collaborates on the approach."
                    ),
                    Steps(
                        [
                            "An authorized provider assesses the patient and "
                            "pronounces death, recording the date, time, and absence "
                            "of vital signs.",
                            "Notify the attending provider (if not the pronouncing "
                            "provider), the Nursing Supervisor, and the family per the "
                            "patient&rsquo;s wishes.",
                            "Notify the OPO of the death/imminent death on the "
                            "required timeline; do not approach the family about "
                            "donation first.",
                            "Determine whether the death is a medical examiner / "
                            "coroner case; if so, preserve lines, tubes, and devices "
                            "and do not perform routine postmortem care until "
                            "released.",
                            "Offer the family the opportunity to request an autopsy "
                            "and provide information on how to do so.",
                        ]
                    ),
                ],
            ),
            Section(
                "Postmortem Care",
                [
                    Bullets(
                        [
                            "Provide culturally and religiously sensitive care of the "
                            "body and support to the family; allow time at the "
                            "bedside.",
                            "For a medical examiner case, leave all medical devices in "
                            "place and sequester the body as instructed until the "
                            "case is released.",
                            "Confirm identification of the body, complete required "
                            "tags and paperwork, and coordinate transfer to the "
                            "morgue or funeral home.",
                            "Complete the death certificate per state requirements "
                            "and within the required time.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Expected deaths consistent with the natural course of illness "
                        "are not reportable events. A death that is unexpected, or "
                        "that may be related to an error, device, restraint or "
                        "seclusion, or an unanticipated outcome, is a sentinel-level "
                        "SEV-1 event under POL-RM-013 — notify the attending provider, "
                        "Nursing Supervisor, Risk Management, and the "
                        "Administrator-on-Call immediately and within 1 hour, and "
                        "manage per POL-RM-004. Any death in or within 24 hours of "
                        "restraint or seclusion is SEV-1 and additionally handled "
                        "under POL-NUR-005. Unanticipated-outcome deaths are disclosed "
                        "to the family under POL-PC-067."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Pronouncement provider, date, and time; examination "
                            "findings supporting the determination.",
                            "OPO notification time and reference number; medical "
                            "examiner determination and release.",
                            "Family notification and any autopsy request or "
                            "declination.",
                            "Disposition of the body and devices; death-certificate "
                            "completion.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CMS Conditions of Participation, 42 CFR 482.13 "
                            "(patients&rsquo; rights), 42 CFR 482.45 (organ, tissue, "
                            "and eye procurement), and 42 CFR 482.22 (autopsy).",
                            "The Joint Commission, standards on organ/tissue donation "
                            "and care at the end of life.",
                            "Related: POL-NUR-005 (restraint & seclusion), POL-PC-067 "
                            "(disclosure), POL-RM-004 (sentinel events), POL-RM-013 "
                            "(severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_ama_discharge() -> PolicyDoc:
    """Against Medical Advice (AMA) discharge."""
    return PolicyDoc(
        number="POL-PC-065",
        title="Against Medical Advice (AMA) Discharge",
        owner="Medical Staff / Nursing",
        effective="2023-06-15",
        revised="2026-03-08",
        review="2028-03-08",
        version="2.1",
        approved_by="Medical Executive Committee",
        applies_to="All inpatient units and the Emergency Department; all licensed "
        "providers and nursing staff",
        keywords=[
            "AMA",
            "against medical advice",
            "refusal",
            "capacity",
            "discharge",
            "informed refusal",
            "elopement",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To respect a patient&rsquo;s right to refuse treatment and "
                        "leave the facility while ensuring the decision is informed "
                        "and made with capacity, and that the patient&rsquo;s safety "
                        "and continuity of care are protected, consistent with "
                        "patient-rights standards (42 CFR 482.13) and accepted "
                        "against-medical-advice practice."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies when a patient with decision-making capacity chooses "
                        "to leave or to decline recommended care before the provider "
                        "advises discharge. A patient who leaves without staff "
                        "knowledge and who is unsafe to be unsupervised is managed as "
                        "an elopement under POL-SEC-010, not as an AMA discharge."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Against Medical Advice (AMA)</b> — a patient leaves or "
                            "refuses recommended care against the provider&rsquo;s "
                            "advice.",
                            "<b>Decision-making capacity</b> — the ability to "
                            "understand the condition and the risks of leaving, "
                            "appreciate how they apply, reason about options, and "
                            "communicate a choice.",
                            "<b>Informed refusal</b> — the patient&rsquo;s documented "
                            "decision to decline care after being informed of the "
                            "risks, benefits, and alternatives.",
                        ]
                    ),
                ],
            ),
            Section(
                "Procedure",
                [
                    Note(
                        "Before a patient leaves AMA, a provider must assess "
                        "decision-making capacity. A patient who lacks capacity "
                        "cannot be discharged AMA; take steps to ensure safety, "
                        "involve the surrogate decision-maker, and consult the "
                        "attending (and Security/Risk Management as needed). Never "
                        "withhold stabilizing or emergency care because a patient "
                        "intends to leave."
                    ),
                    Steps(
                        [
                            "Assess and document decision-making capacity for the "
                            "specific decision to leave.",
                            "Explain, in understandable terms, the risks of leaving, "
                            "the expected benefits of staying, and the alternatives; "
                            "answer questions without coercion.",
                            "Offer continued care, follow-up, prescriptions, and a "
                            "clear invitation to return at any time.",
                            "Ask the patient to sign the AMA form; if they decline to "
                            "sign, document that the risks were explained and the "
                            "patient refused to sign — the discharge is still "
                            "documented as AMA.",
                            "Notify the attending provider; file an event report per "
                            "POL-RM-013.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Events are classified and reported under POL-RM-013. A "
                        "routine AMA departure by a patient with capacity after "
                        "informed refusal is a SEV-3 event, reported within 24 hours. "
                        "An AMA departure by a patient with a serious unstabilized "
                        "condition, or where capacity is in question, is SEV-2 and is "
                        "reported within 4 hours — notify the attending provider and "
                        "Risk Management. If the patient lacks capacity and is at risk "
                        "of harm, escalate as SEV-1 and treat a disappearance as an "
                        "elopement under POL-SEC-010."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Capacity assessment and its basis; who performed it.",
                            "Specific risks of leaving that were explained and the "
                            "patient&rsquo;s understanding.",
                            "Alternatives and follow-up offered (medications, return "
                            "precautions, appointments).",
                            "Whether the AMA form was signed or signing was declined; "
                            "provider notification.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CMS Conditions of Participation, 42 CFR 482.13 — "
                            "Patients&rsquo; Rights (right to refuse treatment).",
                            "The Joint Commission, Rights-and-Responsibilities "
                            "standards on informed refusal.",
                            "Related: POL-SEC-010 (elopement), POL-PC-066 (informed "
                            "consent), POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_informed_consent() -> PolicyDoc:
    """Informed consent (Joint Commission / CMS CoP)."""
    return PolicyDoc(
        number="POL-PC-066",
        title="Informed Consent",
        owner="Medical Staff / Risk Management",
        effective="2023-03-01",
        revised="2026-01-22",
        review="2028-01-22",
        version="2.1",
        approved_by="Medical Executive Committee",
        applies_to="All operative, invasive, and high-risk procedures and "
        "treatments requiring consent; all licensed providers and nursing staff",
        keywords=[
            "informed consent",
            "consent",
            "risks benefits alternatives",
            "capacity",
            "surrogate",
            "interpreter",
            "emergency exception",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To ensure that patients (or their authorized "
                        "representatives) make informed, voluntary decisions about "
                        "proposed treatments and procedures through a documented "
                        "informed-consent process, consistent with The Joint "
                        "Commission informed-consent standards and CMS Conditions of "
                        "Participation (42 CFR 482.13 and 482.51)."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to surgery, anesthesia, invasive procedures, blood "
                        "transfusion, and other treatments for which the facility or "
                        "law requires consent. Routine care covered by the general "
                        "consent to treatment is excluded."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Informed consent</b> — the process by which the "
                            "provider performing the procedure discloses the nature, "
                            "risks, benefits, and alternatives, and the patient "
                            "voluntarily agrees.",
                            "<b>Authorized representative / surrogate</b> — the person "
                            "who consents when the patient lacks capacity or is a "
                            "minor.",
                            "<b>Emergency exception</b> — treatment provided without "
                            "consent when delay to obtain it would seriously endanger "
                            "the patient and consent cannot be obtained.",
                        ]
                    ),
                ],
            ),
            Section(
                "Required Elements of Disclosure",
                [
                    Para(
                        "The provider who will perform the procedure is responsible "
                        "for the informed-consent discussion. At a minimum, it covers:"
                    ),
                    Bullets(
                        [
                            "The patient&rsquo;s diagnosis and the nature and purpose "
                            "of the proposed procedure or treatment.",
                            "The material risks and expected benefits.",
                            "Reasonable alternatives, including their risks and "
                            "benefits, and the option of no treatment.",
                            "Who will perform the procedure, and the likely result of "
                            "declining.",
                        ]
                    ),
                ],
            ),
            Section(
                "Capacity, Surrogates, and Language Access",
                [
                    Note(
                        "Consent must be voluntary and obtained before the procedure "
                        "and before sedation that impairs understanding. When the "
                        "patient does not speak English or has a communication "
                        "disability, use a qualified medical interpreter — never an "
                        "ad hoc interpreter such as a family member — and document "
                        "its use."
                    ),
                    Bullets(
                        [
                            "If the patient lacks capacity, obtain consent from the "
                            "authorized surrogate per the state hierarchy; for a "
                            "minor, from the parent or legal guardian except where law "
                            "allows the minor to consent.",
                            "Under the emergency exception, provide necessary care "
                            "and document why consent could not be obtained.",
                            "Confirm the signed consent is present, correct, and "
                            "matches the planned procedure and site during "
                            "pre-procedure verification (POL-SURG-007).",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Events are classified and reported under POL-RM-013. A "
                        "procedure performed without valid informed consent, or not "
                        "matching the consent (wrong procedure/site), is a SEV-1 "
                        "sentinel-level event — notify the provider of record, Nursing "
                        "Supervisor, Risk Management, and the Administrator-on-Call "
                        "immediately and within 1 hour, and manage per POL-RM-004. A "
                        "consent discrepancy caught during pre-procedure verification "
                        "before the procedure begins is a near miss, reported within "
                        "24 hours. Resulting harm is disclosed under POL-PC-067."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Signed, dated, and timed consent naming the specific "
                            "procedure, site/side, and provider.",
                            "That risks, benefits, and alternatives were discussed and "
                            "questions answered.",
                            "Capacity determination and the surrogate&rsquo;s "
                            "authority where applicable.",
                            "Interpreter used (name/ID and method) when language "
                            "access was needed.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission, informed-consent standards "
                            "(Record of Care / Rights).",
                            "CMS Conditions of Participation, 42 CFR 482.13 "
                            "(patients&rsquo; rights) and 42 CFR 482.51 (surgical "
                            "services — consent).",
                            "Related: POL-SURG-007 (universal protocol), POL-PC-065 "
                            "(AMA / informed refusal), POL-PC-067 (disclosure), "
                            "POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_disclosure() -> PolicyDoc:
    """Disclosure of unanticipated outcomes to patients and families."""
    return PolicyDoc(
        number="POL-PC-067",
        title="Disclosure of Unanticipated Outcomes",
        owner="Risk Management / Medical Staff",
        effective="2023-08-15",
        revised="2026-03-14",
        review="2028-03-14",
        version="2.1",
        approved_by="Patient Safety & Quality Committee",
        applies_to="All licensed providers and staff involved in a patient&rsquo;s "
        "care; coordinated by Risk Management",
        keywords=[
            "disclosure",
            "unanticipated outcome",
            "adverse event",
            "apology",
            "empathy",
            "transparency",
            "communication",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To ensure that patients and families are told, honestly and "
                        "compassionately, about unanticipated outcomes of care, "
                        "consistent with The Joint Commission standard requiring that "
                        "patients be informed of outcomes of care, including "
                        "unanticipated outcomes."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to any outcome that differs significantly from the "
                        "anticipated result and that affects the patient, whether or "
                        "not an error occurred. Disclosure is a clinical communication "
                        "with the patient/family; it is distinct from the confidential "
                        "event report filed under POL-RM-013."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Unanticipated outcome</b> — a result of care that "
                            "differs significantly and unexpectedly from the "
                            "anticipated outcome.",
                            "<b>Disclosure</b> — the communication to the "
                            "patient/family of the facts of what happened, with "
                            "empathy and ongoing care planning.",
                            "<b>Event report</b> — the confidential "
                            "quality-improvement record filed per POL-RM-013; it is "
                            "not part of the medical record and is not the disclosure.",
                        ]
                    ),
                ],
            ),
            Section(
                "Who Discloses and When",
                [
                    Note(
                        "Disclosure is made promptly — generally within 24 hours of "
                        "recognizing the outcome — once the patient is stable and the "
                        "immediate facts are known. The attending or responsible "
                        "provider leads the conversation; Risk Management is notified "
                        "first and helps coordinate, but disclosure is not delayed "
                        "pending a complete investigation."
                    ),
                    Bullets(
                        [
                            "The attending/responsible provider leads; a second "
                            "support person (e.g., nurse manager or Risk Management) "
                            "may attend.",
                            "Notify Risk Management before or as soon as the "
                            "disclosure occurs so it can coordinate and support.",
                            "Hold the conversation in a private setting, in language "
                            "the family understands, using a qualified interpreter "
                            "where needed.",
                        ]
                    ),
                ],
            ),
            Section(
                "What Is Said",
                [
                    Bullets(
                        [
                            "State the known facts of what happened and what it means "
                            "for the patient&rsquo;s care going forward.",
                            "Express genuine empathy and, where appropriate, an "
                            "apology for the harm or the experience.",
                            "Do not speculate about cause, assign or admit blame, or "
                            "point to other individuals before the facts are known.",
                            "Describe the next steps, who to contact, and that the "
                            "facility will follow up as more is learned.",
                        ]
                    ),
                ],
            ),
            Section(
                "Documentation and Distinction from the Event Report",
                [
                    Para(
                        "Document the disclosure conversation in the medical record: "
                        "who was present, the date and time, the facts communicated, "
                        "the patient/family response and questions, and the plan for "
                        "follow-up. Record only facts — not speculation, opinion, or "
                        "the contents of the confidential event report. The event "
                        "report itself is filed separately under POL-RM-013 and is "
                        "neither placed in nor referenced from the medical record."
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "The underlying event is classified and reported under "
                        "POL-RM-013 according to its harm. A SEV-1 (sentinel-level) "
                        "unanticipated outcome requires notification of the attending "
                        "provider, Nursing Supervisor, Risk Management, and the "
                        "Administrator-on-Call immediately and within 1 hour, and is "
                        "managed per POL-RM-004; SEV-2 within 4 hours; SEV-3 or near "
                        "miss within 24 hours. The disclosure obligation applies to "
                        "any significant unanticipated outcome regardless of severity, "
                        "and the disclosure is logged separately from the confidential "
                        "event report."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission, standard on informing patients of "
                            "unanticipated outcomes of care (Rights and "
                            "Responsibilities / Patient Rights).",
                            "CMS Conditions of Participation, 42 CFR 482.13 — "
                            "Patients&rsquo; Rights.",
                            "Related: POL-RM-004 (sentinel events), POL-PC-063 (code "
                            "status), POL-PC-066 (informed consent), POL-RM-013 "
                            "(severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_batch() -> list[PolicyDoc]:
    """Return this batch's policies, in listed order."""
    return [
        build_suicide_risk(),
        build_behavioral_emergency(),
        build_pain_management(),
        build_code_status(),
        build_death_pronouncement(),
        build_ama_discharge(),
        build_informed_consent(),
        build_disclosure(),
    ]
