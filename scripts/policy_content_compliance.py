"""Compliance, privacy, and patient-rights batch of the hospital policy corpus.

Holds seven fictional-facility policy documents (POL-HIM-080 through
POL-CMP-086) covering HIPAA privacy and PHI, breach notification, patient
grievance/complaint management, patient rights, language access and interpreter
services, verbal/telephone order read-back, and primary source verification /
credentialing. Each document is anchored to a real regulatory framework (HIPAA
Privacy and Breach Notification Rules, CMS Conditions of Participation, Title VI
/ Section 1557, CLAS standards, and The Joint Commission standards) and reuses
the facility-wide severity scale defined in POL-RM-013 so the Incident Reporting
Agent can resolve severity and notification timing consistently across the
corpus.
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


def build_hipaa_privacy() -> PolicyDoc:
    """HIPAA privacy and protected health information handling."""
    return PolicyDoc(
        number="POL-HIM-080",
        title="HIPAA Privacy and Protected Health Information",
        owner="Compliance / Health Information Management",
        effective="2023-04-01",
        revised="2026-03-12",
        review="2028-03-12",
        version="3.1",
        approved_by="Compliance & Privacy Committee",
        applies_to="All workforce members, licensed providers, students, "
        "volunteers, and business associates with access to protected health "
        "information",
        keywords=[
            "hipaa",
            "privacy",
            "phi",
            "minimum necessary",
            "disclosure",
            "authorization",
            "confidentiality",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "This policy establishes how Riverside Regional Medical "
                        "Center protects the privacy of protected health "
                        "information (PHI) and limits its use and disclosure, "
                        "consistent with the HIPAA Privacy Rule (45 CFR Part 164 "
                        "Subpart E). It defines permitted uses, the "
                        "minimum-necessary standard, individual rights, and the "
                        "duty to report suspected privacy violations."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Protected health information (PHI)</b> — "
                            "individually identifiable health information held or "
                            "transmitted in any form (electronic, paper, or oral).",
                            "<b>Treatment, payment, and health care operations "
                            "(TPO)</b> — the core activities for which PHI may be "
                            "used or disclosed without a separate authorization.",
                            "<b>Minimum necessary</b> — the requirement to limit "
                            "PHI to the least amount needed to accomplish the "
                            "intended purpose; does not apply to disclosures to "
                            "the provider for treatment.",
                            "<b>Authorization</b> — a signed, HIPAA-compliant "
                            "permission required for uses and disclosures not "
                            "otherwise permitted (e.g., most marketing, sale of "
                            "PHI, psychotherapy notes).",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy — Permitted Uses and Disclosures",
                [
                    Para(
                        "PHI may be used or disclosed for treatment, payment, and "
                        "health care operations without individual authorization. "
                        "All other uses and disclosures require a valid "
                        "authorization unless specifically permitted or required "
                        "by law (for example, public-health reporting, abuse "
                        "reporting, or a valid court order). Workforce members "
                        "access only the PHI required for their role."
                    ),
                    Bullets(
                        [
                            "Apply the minimum-necessary standard to every use, "
                            "disclosure, and request except treatment.",
                            "Verify the identity and authority of any person "
                            "requesting PHI before disclosing.",
                            "Never access your own record, a family member&rsquo;s "
                            "record, or a co-worker&rsquo;s record through "
                            "treatment systems; use the formal records-request "
                            "process.",
                            "Route media, law-enforcement, and attorney requests "
                            "to the Privacy Office before responding.",
                        ]
                    ),
                ],
            ),
            Section(
                "Individual Rights",
                [
                    TableBlock(
                        headers=["Right", "What the patient may do", "Owner"],
                        rows=[
                            [
                                "Access / copy",
                                "Inspect and obtain a copy of their designated "
                                "record set",
                                "HIM",
                            ],
                            [
                                "Amendment",
                                "Request correction of inaccurate or incomplete " "PHI",
                                "HIM",
                            ],
                            [
                                "Accounting of disclosures",
                                "Request a list of certain disclosures",
                                "Privacy Office",
                            ],
                            [
                                "Restriction / confidential communication",
                                "Request limits or alternative contact methods",
                                "Privacy Office",
                            ],
                        ],
                        col_widths=[1.8 * inch, 2.8 * inch, 1.0 * inch],
                    ),
                    Para(
                        "Requests are logged and acted on within the timeframes "
                        "in the Notice of Privacy Practices. Denials must cite a "
                        "permitted ground and inform the individual of review "
                        "rights."
                    ),
                ],
            ),
            Section(
                "Safeguards",
                [
                    Bullets(
                        [
                            "Position screens away from public view; lock "
                            "workstations when unattended; never share login "
                            "credentials.",
                            "Discuss PHI only where it cannot be overheard; avoid "
                            "patient identifiers in hallways and elevators.",
                            "Encrypt PHI in transit and at rest; do not store PHI "
                            "on unencrypted or personal devices.",
                            "Shred paper PHI in designated bins; do not place PHI "
                            "in regular trash or recycling.",
                        ]
                    ),
                    Note(
                        "If you suspect any unauthorized access, use, or "
                        "disclosure of PHI, report it to the Privacy Office "
                        "<b>immediately and no later than the end of your shift</b>. "
                        "Do not attempt to investigate, delete, or &ldquo;undo&rdquo; "
                        "the disclosure yourself &mdash; preserve the record and "
                        "escalate. A potential breach affecting 500 or more "
                        "individuals is a SEV-1 compliance event."
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Privacy events are classified on the facility-wide "
                        "severity scale defined in POL-RM-013 (SEV-1 catastrophic "
                        "/ sentinel, SEV-2 major, SEV-3 minor, Near Miss) and are "
                        "co-managed with the Privacy Office under POL-HIM-081 "
                        "(Breach Notification)."
                    ),
                    TableBlock(
                        headers=[
                            "Severity",
                            "Example privacy event",
                            "Notify",
                            "By when",
                        ],
                        rows=[
                            [
                                "SEV-1",
                                "Breach of 500+ individuals; large-scale PHI "
                                "loss/theft",
                                "Privacy Officer & Compliance (immediately)",
                                "Within 1 hour",
                            ],
                            [
                                "SEV-2",
                                "Misdirected records; snooping in a record",
                                "Privacy Office, manager",
                                "Within 4 hours",
                            ],
                            [
                                "SEV-3 / Near Miss",
                                "Single mis-faxed page intercepted; verbal "
                                "overshare",
                                "Privacy Office via event report",
                                "Within 24 hours",
                            ],
                        ],
                        col_widths=[1.0 * inch, 2.2 * inch, 1.6 * inch, 1.0 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "HIPAA Privacy Rule, 45 CFR Part 164 Subpart E.",
                            "HIPAA Security Rule, 45 CFR Part 164 Subpart C "
                            "(electronic PHI safeguards).",
                            "Related: POL-HIM-081 (Breach Notification), "
                            "POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_breach_notification() -> PolicyDoc:
    """HIPAA breach notification recipients, deadlines, and process."""
    return PolicyDoc(
        number="POL-HIM-081",
        title="Breach Notification",
        owner="Compliance / Privacy Office",
        effective="2023-04-01",
        revised="2026-03-12",
        review="2028-03-12",
        version="2.4",
        approved_by="Compliance & Privacy Committee",
        applies_to="All workforce members and business associates; executed by "
        "the Privacy Office and Compliance",
        keywords=[
            "breach",
            "breach notification",
            "phi",
            "ocr",
            "60 days",
            "risk assessment",
            "media notice",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "This policy governs how Riverside Regional Medical "
                        "Center responds to a breach of unsecured protected "
                        "health information, consistent with the HIPAA Breach "
                        "Notification Rule (45 CFR 164.400&ndash;414). It defines "
                        "how a potential breach is assessed, who must be notified, "
                        "and the deadlines for each notice."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Breach</b> — the acquisition, access, use, or "
                            "disclosure of unsecured PHI in a manner not permitted "
                            "by the Privacy Rule that compromises the security or "
                            "privacy of the PHI.",
                            "<b>Discovery</b> — the first day the breach is known, "
                            "or by reasonable diligence would have been known, to "
                            "the facility. All notification clocks run from "
                            "discovery.",
                            "<b>Unsecured PHI</b> — PHI not rendered unusable, "
                            "unreadable, or indecipherable through encryption or "
                            "destruction per HHS guidance.",
                        ]
                    ),
                ],
            ),
            Section(
                "Four-Factor Risk Assessment",
                [
                    Para(
                        "Unless an exception applies, an impermissible use or "
                        "disclosure is presumed to be a breach unless the facility "
                        "demonstrates a low probability that PHI was compromised, "
                        "based on at least these four factors:"
                    ),
                    Steps(
                        [
                            "The nature and extent of the PHI involved, including "
                            "identifiers and likelihood of re-identification.",
                            "The unauthorized person who used the PHI or to whom "
                            "the disclosure was made.",
                            "Whether the PHI was actually acquired or viewed.",
                            "The extent to which the risk to the PHI has been "
                            "mitigated.",
                        ]
                    ),
                ],
            ),
            Section(
                "Notification Recipients and Deadlines",
                [
                    TableBlock(
                        headers=["Recipient", "When required", "Deadline"],
                        rows=[
                            [
                                "Affected individuals",
                                "Every breach of unsecured PHI",
                                "Without unreasonable delay; no later than 60 "
                                "calendar days from discovery",
                            ],
                            [
                                "HHS / OCR",
                                "Breach affecting 500+ individuals",
                                "Concurrently; no later than 60 days from "
                                "discovery, via the OCR portal",
                            ],
                            [
                                "HHS / OCR (small breach log)",
                                "Breach affecting fewer than 500 individuals",
                                "Logged and submitted annually, within 60 days "
                                "after year-end",
                            ],
                            [
                                "Prominent media",
                                "Breach affecting 500+ residents of a State or "
                                "jurisdiction",
                                "Without unreasonable delay; no later than 60 days "
                                "from discovery",
                            ],
                        ],
                        col_widths=[1.5 * inch, 1.9 * inch, 2.4 * inch],
                        row_shades=[None, _SEV1, None, _SEV1],
                    ),
                    Para(
                        "Individual notice is written and sent by first-class mail "
                        "(or email if the individual agreed) and describes what "
                        "happened, the PHI involved, steps individuals should "
                        "take, what the facility is doing, and contact "
                        "information."
                    ),
                    Note(
                        "The 60-day period is an <b>outer limit, not a target</b>. "
                        "Begin individual notification as soon as the breach is "
                        "confirmed. For any breach affecting <b>500 or more "
                        "individuals</b>, notify the Privacy Officer and Compliance "
                        "immediately &mdash; this is a SEV-1 event &mdash; and "
                        "submit the HHS/OCR and media notices concurrently with "
                        "individual notice, no later than 60 days from discovery."
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Breaches are classified on the facility-wide scale in "
                        "POL-RM-013. A breach of 500 or more individuals, or any "
                        "large-scale PHI loss, is a SEV-1-level compliance event "
                        "escalated to the Privacy Officer and Compliance "
                        "immediately (within 1 hour). A confirmed breach under 500 "
                        "individuals is typically SEV-2 (notify the Privacy Office "
                        "within 4 hours). A suspected impermissible disclosure "
                        "intercepted before PHI was acquired is a Near Miss "
                        "(report within 24 hours)."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "HIPAA Breach Notification Rule, 45 CFR "
                            "164.400&ndash;414 (individual notice 164.404, media "
                            "notice 164.406, HHS notice 164.408).",
                            "HHS guidance on securing PHI (encryption / "
                            "destruction).",
                            "Related: POL-HIM-080 (HIPAA Privacy), POL-RM-013 "
                            "(severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_grievance() -> PolicyDoc:
    """Patient grievance versus complaint handling and timeframes."""
    return PolicyDoc(
        number="POL-CMP-082",
        title="Patient Grievance and Complaint Management",
        owner="Patient Experience / Risk Management",
        effective="2023-06-15",
        revised="2026-04-20",
        review="2028-04-20",
        version="3.0",
        approved_by="Patient Experience Committee",
        applies_to="All staff who receive patient or representative concerns; "
        "coordinated by Patient Experience",
        keywords=[
            "grievance",
            "complaint",
            "patient rights",
            "resolution",
            "written notice",
            "patient experience",
            "cms",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "This policy establishes a prompt, fair process for "
                        "resolving patient complaints and grievances consistent "
                        "with the CMS Condition of Participation on patient rights "
                        "(42 CFR 482.13). It distinguishes a complaint from a "
                        "grievance and sets response timeframes and written-notice "
                        "requirements."
                    ),
                ],
            ),
            Section(
                "Definitions — Complaint vs. Grievance",
                [
                    TableBlock(
                        headers=[
                            "Type",
                            "What it is",
                            "Target timeframe",
                        ],
                        rows=[
                            [
                                "Complaint",
                                "A concern resolved promptly by staff present, "
                                "about care or service that can be addressed at "
                                "the point of contact",
                                "Resolve during the encounter; no written notice "
                                "required",
                            ],
                            [
                                "Grievance",
                                "A formal written or verbal concern about care, "
                                "safety, Medicare rights, or abuse that is not "
                                "resolved at once, or any written/emailed concern",
                                "Written notice of resolution; ~7-day average per "
                                "CMS",
                            ],
                        ],
                        col_widths=[1.0 * inch, 2.9 * inch, 1.9 * inch],
                    ),
                    Para(
                        "A concern becomes a grievance when it cannot be resolved "
                        "at the time by staff present, is postponed for later "
                        "follow-up, is submitted in writing (including email), or "
                        "alleges abuse, neglect, or a patient-safety or Medicare "
                        "rights issue."
                    ),
                ],
            ),
            Section(
                "Process",
                [
                    Steps(
                        [
                            "Acknowledge the concern and attempt immediate "
                            "resolution; de-escalate and address what can be fixed "
                            "now.",
                            "If it meets the grievance definition, enter it in the "
                            "grievance log and notify Patient Experience the same "
                            "day.",
                            "Investigate: gather facts from the care team and the "
                            "record; involve the manager and, as needed, Risk "
                            "Management.",
                            "Determine resolution and document the steps taken and "
                            "the outcome.",
                            "Send the patient or representative written notice of "
                            "the decision.",
                        ]
                    ),
                ],
            ),
            Section(
                "Written Notice and Timeframes",
                [
                    Bullets(
                        [
                            "The grievance process targets a <b>7-day average</b> "
                            "resolution; most grievances receive written notice "
                            "within 7 calendar days.",
                            "If resolution will take longer, send the patient an "
                            "interim update stating that review is ongoing and a "
                            "follow-up date.",
                            "The written notice must name a hospital contact "
                            "person, the steps taken to investigate, the results "
                            "of the process, and the date of completion.",
                        ]
                    ),
                    Note(
                        "Any grievance alleging <b>abuse, neglect, or an event "
                        "that caused patient harm</b> must be reported to Risk "
                        "Management and, where applicable, filed as an event "
                        "report per POL-RM-013 at the same time the grievance is "
                        "logged &mdash; do not wait for the grievance process to "
                        "conclude."
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "A grievance is classified on the facility-wide scale in "
                        "POL-RM-013 based on any underlying event. A grievance "
                        "alleging serious harm or a sentinel event is SEV-1 "
                        "(notify the Administrator-on-Call and Risk Management "
                        "within 1 hour). A grievance alleging a major care issue "
                        "without current harm is SEV-2 (notify Patient Experience "
                        "and the manager within 4 hours). A routine service "
                        "grievance is SEV-3 (report within 24 hours)."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CMS Conditions of Participation, 42 CFR 482.13 "
                            "(patient&rsquo;s rights; grievance process and "
                            "timeframes).",
                            "CMS State Operations Manual, Appendix A "
                            "(interpretive guidance on grievances).",
                            "Related: POL-CMP-083 (Patient Rights), POL-RM-013 "
                            "(severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_patient_rights() -> PolicyDoc:
    """Patient rights and responsibilities under the CMS CoP."""
    return PolicyDoc(
        number="POL-CMP-083",
        title="Patient Rights and Responsibilities",
        owner="Administration / Patient Experience",
        effective="2023-06-15",
        revised="2026-04-20",
        review="2028-04-20",
        version="2.2",
        approved_by="Patient Experience Committee",
        applies_to="All patients and their representatives; all staff and "
        "licensed providers",
        keywords=[
            "patient rights",
            "responsibilities",
            "informed consent",
            "restraints",
            "privacy",
            "advance directive",
            "cms",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "This policy affirms the rights of every patient at "
                        "Riverside Regional Medical Center and the "
                        "responsibilities of staff to honor them, consistent with "
                        "the CMS Condition of Participation on patient rights "
                        "(42 CFR 482.13). Patients are informed of their rights in "
                        "advance of furnishing or discontinuing care wherever "
                        "possible."
                    ),
                ],
            ),
            Section(
                "Patient Rights",
                [
                    Bullets(
                        [
                            "To be informed of their rights and to exercise them "
                            "without coercion, discrimination, or reprisal.",
                            "To participate in care decisions, give or withhold "
                            "informed consent, and formulate advance directives.",
                            "To personal privacy, confidentiality of records, and "
                            "care in a safe setting.",
                            "To be free from restraint or seclusion imposed for "
                            "coercion, discipline, convenience, or retaliation.",
                            "To access their medical records and to voice "
                            "grievances about care without fear of reprisal.",
                        ]
                    ),
                ],
            ),
            Section(
                "Patient Responsibilities",
                [
                    Bullets(
                        [
                            "Provide accurate and complete health information.",
                            "Ask questions when instructions or the plan of care "
                            "are not understood.",
                            "Treat staff and other patients with respect and "
                            "follow facility conduct and safety rules.",
                            "Meet financial obligations as arranged with the "
                            "facility.",
                        ]
                    ),
                ],
            ),
            Section(
                "Informing Patients of Rights",
                [
                    Para(
                        "Patients receive a written statement of rights and the "
                        "Notice of Privacy Practices at or before admission, in a "
                        "language and format they understand. Staff direct "
                        "patients to language-access services per POL-CMP-084 when "
                        "needed, and to the grievance process per POL-CMP-082."
                    ),
                    Note(
                        "A patient&rsquo;s refusal of care, request to leave "
                        "against medical advice, or withdrawal of consent must be "
                        "honored and <b>documented immediately</b>, with the "
                        "attending provider notified at once. Never use restraint "
                        "to prevent a competent patient from leaving."
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Violations of patient rights are classified on the "
                        "facility-wide scale in POL-RM-013. An event involving "
                        "abuse, neglect, or inappropriate restraint resulting in "
                        "serious harm or death is SEV-1 (notify the "
                        "Administrator-on-Call and Risk Management within 1 hour). "
                        "A major rights violation without serious harm is SEV-2 "
                        "(notify the manager and Risk Management within 4 hours). "
                        "A minor lapse is SEV-3 (report within 24 hours)."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CMS Conditions of Participation, 42 CFR 482.13 "
                            "(patient&rsquo;s rights).",
                            "Related: POL-CMP-082 (Grievance), POL-CMP-084 "
                            "(Language Access), POL-HIM-080 (HIPAA Privacy), "
                            "POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_language_access() -> PolicyDoc:
    """Language access and interpreter services."""
    return PolicyDoc(
        number="POL-CMP-084",
        title="Language Access and Interpreter Services",
        owner="Patient Experience / Compliance",
        effective="2024-02-01",
        revised="2026-04-20",
        review="2028-04-20",
        version="2.1",
        approved_by="Patient Experience Committee",
        applies_to="All staff and providers serving patients and representatives "
        "with limited English proficiency or who are deaf or hard of hearing",
        keywords=[
            "language access",
            "interpreter",
            "limited english proficiency",
            "lep",
            "section 1557",
            "clas",
            "title vi",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "This policy ensures meaningful access to care for "
                        "patients with limited English proficiency (LEP) and for "
                        "patients who are deaf or hard of hearing, consistent with "
                        "Title VI of the Civil Rights Act, Section 1557 of the "
                        "Affordable Care Act, and the national CLAS standards. "
                        "Qualified interpreter services are provided free of "
                        "charge."
                    ),
                ],
            ),
            Section(
                "Policy",
                [
                    Bullets(
                        [
                            "Offer and provide a qualified interpreter at no cost "
                            "for all significant clinical encounters.",
                            "Do not require or rely on family members, friends, or "
                            "minors to interpret; a minor may interpret only in a "
                            "genuine emergency until a qualified interpreter is "
                            "available.",
                            "Do not rely on bilingual staff to interpret unless "
                            "they are assessed and qualified to do so.",
                            "Document the patient&rsquo;s preferred language and "
                            "the interpreter modality used in the record.",
                        ]
                    ),
                ],
            ),
            Section(
                "Interpreter Access Modalities",
                [
                    TableBlock(
                        headers=["Modality", "Best for", "How to access"],
                        rows=[
                            [
                                "In-person interpreter",
                                "Complex, sensitive, or high-stakes encounters "
                                "(consent, end-of-life)",
                                "Schedule via Patient Experience; on-call roster "
                                "after hours",
                            ],
                            [
                                "Video remote interpreting (VRI)",
                                "Most encounters, including American Sign Language "
                                "when in-person is unavailable",
                                "Use the unit VRI tablet; dial the language",
                            ],
                            [
                                "Telephonic interpreting",
                                "Brief or urgent exchanges; less common languages",
                                "Dual-handset phone; call the vendor line and give "
                                "the account code",
                            ],
                        ],
                        col_widths=[1.5 * inch, 2.4 * inch, 1.9 * inch],
                    ),
                    Note(
                        "For any <b>informed consent, procedure, discharge "
                        "instruction, or end-of-life discussion</b>, a qualified "
                        "interpreter must be used before the encounter proceeds. "
                        "Do not proceed with a family member interpreting. If no "
                        "interpreter can be reached, pause non-emergent care and "
                        "escalate to the house supervisor."
                    ),
                ],
            ),
            Section(
                "Auxiliary Aids and Written Materials",
                [
                    Bullets(
                        [
                            "Provide auxiliary aids (ASL interpreters, "
                            "captioning, assistive listening) for patients who are "
                            "deaf or hard of hearing.",
                            "Post the facility&rsquo;s notice of nondiscrimination "
                            "and taglines in the top languages of the service "
                            "area.",
                            "Translate vital documents (consent, rights, "
                            "discharge instructions) into the most frequently "
                            "encountered languages.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Failures of language access are classified on the "
                        "facility-wide scale in POL-RM-013. A communication "
                        "failure that contributed to serious harm (for example, an "
                        "invalid consent for a procedure) is SEV-1 (notify the "
                        "Administrator-on-Call and Risk Management within 1 hour). "
                        "A major access failure without harm is SEV-2 (notify "
                        "Patient Experience within 4 hours). A minor lapse or a "
                        "Near Miss is SEV-3 / Near Miss (report within 24 hours)."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "Title VI of the Civil Rights Act of 1964; Section "
                            "1557 of the Affordable Care Act (45 CFR Part 92).",
                            "National CLAS Standards (HHS Office of Minority "
                            "Health).",
                            "Related: POL-CMP-083 (Patient Rights), POL-RM-013 "
                            "(severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_verbal_order_readback() -> PolicyDoc:
    """Verbal and telephone order read-back and critical-result read-back."""
    return PolicyDoc(
        number="POL-CMP-085",
        title="Verbal and Telephone Order Read-Back",
        owner="Medical Staff / Nursing",
        effective="2023-09-01",
        revised="2026-05-05",
        review="2028-05-05",
        version="2.3",
        approved_by="Medical Executive Committee",
        applies_to="All licensed staff who receive verbal or telephone orders or "
        "critical test results",
        keywords=[
            "verbal order",
            "telephone order",
            "read-back",
            "critical result",
            "npsg",
            "order entry",
            "closed loop",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "This policy defines the read-back process for verbal and "
                        "telephone orders and for reporting critical test results, "
                        "consistent with The Joint Commission National Patient "
                        "Safety Goal NPSG.02.03.01, to reduce communication errors "
                        "at points of hand-off."
                    ),
                ],
            ),
            Section(
                "Policy",
                [
                    Bullets(
                        [
                            "Verbal orders are limited to situations where "
                            "electronic or written entry is not feasible (for "
                            "example, during a sterile procedure or a true "
                            "emergency).",
                            "Every verbal/telephone order and every critical "
                            "result communicated verbally must be written down (or "
                            "entered) and read back verbatim.",
                            "The ordering or reporting individual must confirm the "
                            "read-back is correct before the exchange ends.",
                            "The receiver enters the order and the ordering "
                            "provider authenticates (signs) it within the "
                            "medical-staff timeframe.",
                        ]
                    ),
                ],
            ),
            Section(
                "Read-Back Procedure",
                [
                    Steps(
                        [
                            "<b>Write (or enter) down</b> the complete order or "
                            "critical result as it is given.",
                            "<b>Read back</b> what you wrote, verbatim, including "
                            "drug name, dose, route, and frequency; spell "
                            "look-alike/sound-alike drug names.",
                            "<b>Receive confirmation</b> &mdash; the ordering or "
                            "reporting person explicitly confirms "
                            "&ldquo;that is correct&rdquo;.",
                            "Document the order with the time, the provider, and "
                            "that read-back was performed.",
                        ]
                    ),
                    Note(
                        "A <b>critical test result</b> must be read back to the "
                        "reporter and communicated to the responsible licensed "
                        "caregiver within the timeframe in the critical-values "
                        "protocol so that the patient can be treated promptly. If "
                        "you cannot reach the responsible provider, escalate up "
                        "the chain without delay."
                    ),
                ],
            ),
            Section(
                "Prohibited and Restricted Orders",
                [
                    Bullets(
                        [
                            "Chemotherapy and other high-alert verbal orders are "
                            "prohibited except in defined emergencies.",
                            "Do not use prohibited abbreviations from the facility "
                            "&ldquo;Do Not Use&rdquo; list in any order.",
                            "Texting of orders is not permitted; orders are "
                            "entered through the approved order-entry system.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Read-back failures and resulting events are classified on "
                        "the facility-wide scale in POL-RM-013. A verbal-order or "
                        "critical-result failure that reached a patient and caused "
                        "serious harm or death is SEV-1 (notify the "
                        "Administrator-on-Call and Risk Management within 1 hour). "
                        "A failure that reached the patient without serious harm "
                        "is SEV-2 (notify the manager and the provider within 4 "
                        "hours). An error caught before reaching the patient is a "
                        "Near Miss (report within 24 hours)."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission NPSG.02.03.01 (critical results "
                            "of tests and diagnostic procedures; read-back).",
                            "The Joint Commission &ldquo;Do Not Use&rdquo; list of "
                            "abbreviations.",
                            "Related: POL-PS-008 (Patient Identification), "
                            "POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_credentialing() -> PolicyDoc:
    """Primary source verification and provider credentialing."""
    return PolicyDoc(
        number="POL-CMP-086",
        title="Primary Source Verification and Credentialing",
        owner="Medical Staff Office / Human Resources",
        effective="2024-03-01",
        revised="2026-05-05",
        review="2028-05-05",
        version="2.0",
        approved_by="Medical Executive Committee",
        applies_to="All licensed independent practitioners, advanced practice "
        "providers, and licensed/certified staff requiring verification",
        keywords=[
            "credentialing",
            "primary source verification",
            "psv",
            "privileging",
            "license",
            "certification",
            "expiration tracking",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "This policy establishes how Riverside Regional Medical "
                        "Center verifies the qualifications of practitioners and "
                        "licensed/certified staff through primary source "
                        "verification (PSV) before they provide care, consistent "
                        "with The Joint Commission MS/HR standards and the CMS "
                        "Condition of Participation for the medical staff (42 CFR "
                        "482.22). It also defines ongoing expiration tracking so "
                        "no one practices on a lapsed credential."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Primary source verification (PSV)</b> — "
                            "confirmation of a credential directly from the "
                            "issuing source or an approved designated-agent "
                            "equivalent, not from a copy supplied by the "
                            "applicant.",
                            "<b>Credentialing</b> — collecting and verifying "
                            "qualifications (education, training, licensure, "
                            "competence).",
                            "<b>Privileging</b> — granting a practitioner specific "
                            "clinical privileges based on verified competence.",
                        ]
                    ),
                ],
            ),
            Section(
                "Verification Sources",
                [
                    TableBlock(
                        headers=["Credential", "Primary source"],
                        rows=[
                            [
                                "State license",
                                "State licensing board (online verification or "
                                "direct confirmation)",
                            ],
                            [
                                "Board certification",
                                "The certifying board (e.g., ABMS member board)",
                            ],
                            [
                                "Education / training",
                                "The medical/professional school and residency "
                                "program",
                            ],
                            [
                                "DEA registration",
                                "DEA registration verification",
                            ],
                            [
                                "Sanctions / exclusions",
                                "NPDB query and OIG/SAM exclusion lists",
                            ],
                        ],
                        col_widths=[1.8 * inch, 4.0 * inch],
                    ),
                ],
            ),
            Section(
                "Expiration Tracking",
                [
                    Para(
                        "The Medical Staff Office and Human Resources maintain a "
                        "tracked record of every time-limited credential. This "
                        "directly supports the facility Employee Certification "
                        "workflow, which tracks each certification by "
                        "<b>hospital</b>, <b>certification type</b>, and "
                        "<b>expiration date</b> so that upcoming lapses are "
                        "surfaced before they occur."
                    ),
                    Bullets(
                        [
                            "Reverify time-limited credentials (license, board "
                            "certification, DEA, BLS/ACLS, and similar) at or "
                            "before expiration.",
                            "Generate expiration alerts well in advance so renewal "
                            "is completed before the lapse date.",
                            "Suspend privileges or assignment automatically when a "
                            "required credential lapses.",
                        ]
                    ),
                    Note(
                        "No practitioner or certified staff member may provide "
                        "care on an <b>expired or unverified credential</b>. If a "
                        "lapse is discovered, suspend the affected privileges or "
                        "assignment <b>immediately</b> and notify the Medical "
                        "Staff Office, the department chair, and Compliance before "
                        "the next scheduled shift."
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Credentialing failures are classified on the "
                        "facility-wide scale in POL-RM-013. A lapse that allowed "
                        "an unqualified or unverified provider to practice is a "
                        "serious event: if a patient was harmed it is SEV-1 "
                        "(notify the Administrator-on-Call, the Chief Medical "
                        "Officer, and Compliance within 1 hour); if a patient was "
                        "seen but not harmed it is SEV-2 (notify the Medical Staff "
                        "Office and Compliance within 4 hours). A lapse caught by "
                        "expiration tracking before any patient contact is a Near "
                        "Miss (report within 24 hours)."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission MS and HR standards "
                            "(credentialing and primary source verification).",
                            "CMS Conditions of Participation, 42 CFR 482.22 "
                            "(medical staff).",
                            "National Practitioner Data Bank (NPDB); OIG/SAM "
                            "exclusion databases.",
                            "Related: POL-RM-013 (severity & reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_batch() -> list[PolicyDoc]:
    """Return this batch's policies, in listed order."""
    return [
        build_hipaa_privacy(),
        build_breach_notification(),
        build_grievance(),
        build_patient_rights(),
        build_language_access(),
        build_verbal_order_readback(),
        build_credentialing(),
    ]
