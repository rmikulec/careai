"""Infection prevention & control batch of the hospital policy corpus.

Eight topic policies (POL-IC-020 through POL-IC-027) covering hand hygiene,
device-associated infection bundles (CLABSI, CAUTI, SSI), transmission-based
isolation precautions, multidrug-resistant organism management, tuberculosis
exposure control, and reusable medical device reprocessing. Each policy is
fictional-facility prose anchored to the governing real-world standard (CDC /
HICPAC, CMS Conditions of Participation, OSHA, The Joint Commission, APIC /
SHEA, AORN, AAMI) and ties its events back to the facility-wide severity and
notification scheme defined in POL-RM-013 so the Incident Reporting Agent can
resolve severity and notification timing consistently across documents.
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

_APPROVER = "Infection Prevention & Control Committee"


def build_hand_hygiene() -> PolicyDoc:
    """Hand hygiene indications, technique, and monitoring."""
    return PolicyDoc(
        number="POL-IC-020",
        title="Hand Hygiene",
        owner="Infection Prevention & Control",
        effective="2023-06-01",
        revised="2026-01-28",
        review="2028-01-28",
        version="4.0",
        approved_by=_APPROVER,
        applies_to="All employees, licensed providers, students, volunteers, and "
        "contract staff in every patient-care and patient-adjacent area",
        keywords=[
            "hand hygiene",
            "hand washing",
            "alcohol-based hand rub",
            "ABHR",
            "five moments",
            "WHO",
            "glove use",
            "compliance",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To prevent healthcare-associated infections by ensuring "
                        "consistent, correct hand hygiene by all personnel, "
                        "consistent with the CDC Guideline for Hand Hygiene in "
                        "Health-Care Settings and the WHO <i>My 5 Moments for Hand "
                        "Hygiene</i> framework."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to everyone who enters a patient-care area, "
                        "regardless of whether direct patient contact is anticipated. "
                        "Hand hygiene is the single most effective measure to reduce "
                        "transmission of pathogens and is non-negotiable at the "
                        "indications defined below."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Hand hygiene</b> — a general term for either washing "
                            "with soap and water or applying an alcohol-based hand "
                            "rub (ABHR).",
                            "<b>ABHR</b> — alcohol-based hand rub containing 60&ndash;"
                            "95% alcohol; the preferred method for routinely "
                            "decontaminating hands when they are not visibly soiled.",
                            "<b>Visibly soiled hands</b> — hands with visible dirt, "
                            "blood, or body fluids; these require soap and water, not "
                            "ABHR.",
                            "<b>Point of care</b> — the place where the patient, the "
                            "provider, and care involving contact come together; ABHR "
                            "must be available at the point of care.",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy and Procedure",
                [
                    Para(
                        "Perform hand hygiene at each of the WHO Five Moments: "
                        "(1)&nbsp;before touching a patient; (2)&nbsp;before a clean "
                        "or aseptic procedure; (3)&nbsp;after body-fluid exposure "
                        "risk; (4)&nbsp;after touching a patient; and (5)&nbsp;after "
                        "touching the patient&rsquo;s surroundings."
                    ),
                    Steps(
                        [
                            "Use soap and water when hands are visibly soiled, after "
                            "using the restroom, before eating, and after known or "
                            "suspected exposure to spore-forming organisms such as "
                            "<i>Clostridioides difficile</i> or <i>Bacillus "
                            "anthracis</i> (alcohol does not kill spores).",
                            "Otherwise, decontaminate hands with ABHR: apply a "
                            "palmful, cover all surfaces of both hands, and rub until "
                            "dry (about 20&ndash;30 seconds).",
                            "When washing, wet hands, apply soap, lather all "
                            "surfaces for at least 20 seconds, rinse, and dry with a "
                            "single-use towel; use the towel to turn off the faucet.",
                            "Perform hand hygiene before donning and after removing "
                            "gloves &mdash; gloves are not a substitute for hand "
                            "hygiene.",
                        ]
                    ),
                    Note(
                        "Hands must be decontaminated immediately before every "
                        "clean or aseptic procedure &mdash; including insertion of "
                        "any intravascular or urinary catheter &mdash; and "
                        "immediately after any contact with blood or body fluids, "
                        "even if gloves were worn. Do not proceed with an invasive "
                        "procedure if hand hygiene has not been performed."
                    ),
                    Bullets(
                        [
                            "Keep natural nail tips shorter than one-quarter inch. "
                            "Personnel with direct contact with high-risk patients "
                            "(e.g., ICU, OR) must not wear artificial nails or "
                            "extenders.",
                            "Do not wear rings or wrist jewelry during patient care "
                            "that impede effective hand hygiene.",
                            "Use facility-provided lotions only; petroleum-based "
                            "products can degrade latex gloves.",
                        ]
                    ),
                ],
            ),
            Section(
                "Monitoring and Compliance",
                [
                    TableBlock(
                        headers=["Program element", "Standard"],
                        rows=[
                            [
                                "Direct observation",
                                "Trained observers audit a sampled number of hand "
                                "hygiene opportunities per unit each month; the "
                                "facility goal is &ge;&nbsp;90% compliance.",
                            ],
                            [
                                "Product availability",
                                "ABHR dispensers at every point of care and room "
                                "entrance; sinks stocked with soap and single-use "
                                "towels at all times.",
                            ],
                            [
                                "Feedback",
                                "Unit-level compliance reported to staff and leaders "
                                "monthly; sustained shortfalls trigger a performance "
                                "improvement plan.",
                            ],
                        ],
                        col_widths=[1.8 * inch, 4.0 * inch],
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Hand hygiene lapses and related exposures are classified on "
                        "the facility-wide scale in POL-RM-013. A lapse that "
                        "contributes to a confirmed healthcare-associated infection "
                        "or an MDRO transmission is reviewed as SEV-2 (major / "
                        "temporary harm requiring intervention) and Risk Management "
                        "and Infection Prevention must be notified within 4 hours. "
                        "An observed breach in technique with no harm, or one "
                        "intercepted before patient contact, is logged as SEV-3 or a "
                        "Near Miss and reported to the Charge Nurse and Infection "
                        "Prevention within 24 hours via the event report. When facts "
                        "could support two levels, assign the higher level."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Monthly direct-observation audit results by unit, role, "
                            "and the specific moment missed.",
                            "Product-availability rounds and any stock-out "
                            "remediation.",
                            "For a lapse linked to an infection or transmission: the "
                            "event report, assigned severity, and every notification "
                            "made (who, when, by what method).",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CDC, Guideline for Hand Hygiene in Health-Care "
                            "Settings, MMWR 2002;51(RR-16); CDC Core Infection "
                            "Prevention and Control Practices.",
                            "WHO, Guidelines on Hand Hygiene in Health Care (2009); "
                            "<i>My 5 Moments for Hand Hygiene</i>.",
                            "The Joint Commission, NPSG.07.01.01 (comply with hand "
                            "hygiene guidelines); CMS Conditions of Participation, 42 "
                            "CFR 482.42 (infection prevention and control).",
                            "Related: POL-RM-013 (severity &amp; reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_clabsi() -> PolicyDoc:
    """Central line-associated bloodstream infection prevention bundle."""
    return PolicyDoc(
        number="POL-IC-021",
        title="Central Line-Associated Bloodstream Infection (CLABSI) Prevention",
        owner="Infection Prevention & Control / Nursing",
        effective="2023-08-15",
        revised="2026-02-18",
        review="2028-02-18",
        version="3.2",
        approved_by=_APPROVER,
        applies_to="All units and providers who insert, access, or maintain central "
        "venous catheters, including ICUs, procedural areas, and oncology",
        keywords=[
            "clabsi",
            "central line",
            "central venous catheter",
            "insertion bundle",
            "maintenance bundle",
            "chlorhexidine",
            "maximal barrier",
            "nhsn",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To eliminate central line-associated bloodstream infections "
                        "through standardized insertion and maintenance practices, "
                        "consistent with the CDC/HICPAC Guidelines for the Prevention "
                        "of Intravascular Catheter-Related Infections and the SHEA/"
                        "IDSA/APIC Compendium."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Central line</b> — an intravascular catheter that "
                            "terminates at or close to the heart or in a great "
                            "vessel and is used for infusion, withdrawal of blood, or "
                            "hemodynamic monitoring.",
                            "<b>CLABSI</b> — a laboratory-confirmed bloodstream "
                            "infection in a patient with a central line in place for "
                            "&gt;&nbsp;2 calendar days on the date of the event, not "
                            "related to an infection at another site, per the NHSN "
                            "surveillance definition.",
                            "<b>Maximal sterile barrier</b> — cap, mask, sterile "
                            "gown, sterile gloves, and a full-body sterile drape used "
                            "during insertion.",
                            "<b>Central line day</b> — the daily count of patients "
                            "with one or more central lines, the denominator for the "
                            "NHSN CLABSI rate.",
                        ]
                    ),
                ],
            ),
            Section(
                "Insertion and Maintenance Bundles",
                [
                    Para(
                        "Both bundles are all-or-nothing: every element is required "
                        "for every line. An independent observer completes the "
                        "insertion checklist and is empowered to halt a non-emergent "
                        "insertion if any element is breached."
                    ),
                    TableBlock(
                        headers=["Bundle", "Required elements"],
                        rows=[
                            [
                                "<b>Insertion</b>",
                                "Hand hygiene; maximal sterile barrier precautions; "
                                "chlorhexidine &gt;&nbsp;0.5% with alcohol skin prep "
                                "allowed to fully dry; avoid the femoral site in "
                                "adults; checklist completed by an observer.",
                            ],
                            [
                                "<b>Maintenance</b>",
                                "Daily review of line necessity with prompt removal; "
                                "scrub the hub for 15 seconds before every access; "
                                "sterile dressing change (gauze every 2 days, "
                                "transparent every 7 days or when soiled); CHG "
                                "bathing for ICU patients.",
                            ],
                        ],
                        col_widths=[1.3 * inch, 4.5 * inch],
                    ),
                    Note(
                        "Assess the need for every central line at least once daily "
                        "and remove it as soon as it is no longer essential &mdash; "
                        "an unnecessary catheter day is the single largest "
                        "modifiable CLABSI risk. Any line inserted under emergent, "
                        "non-sterile conditions must be replaced within 48 hours."
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Each confirmed CLABSI is an event under POL-RM-013. A CLABSI "
                        "resulting in sepsis, septic shock, ICU transfer, or death is "
                        "SEV-1; the attending provider, Charge Nurse, Nursing "
                        "Supervisor, Risk Management, Infection Prevention, and the "
                        "Administrator-on-Call must be notified immediately and never "
                        "later than 1 hour from discovery. A CLABSI requiring "
                        "antimicrobial therapy or line removal without those "
                        "complications is SEV-2 &mdash; notify the attending "
                        "provider, Charge Nurse, Risk Management, and Infection "
                        "Prevention within 4 hours. An insertion-bundle breach "
                        "caught before harm is a Near Miss, reported within 24 hours."
                    ),
                    TableBlock(
                        headers=["Severity", "CLABSI event", "Notify by"],
                        rows=[
                            [
                                "SEV-1",
                                "CLABSI with sepsis/septic shock, ICU transfer, or "
                                "death.",
                                "&le;&nbsp;1 hour from discovery.",
                            ],
                            [
                                "SEV-2",
                                "Confirmed CLABSI requiring treatment or line "
                                "removal, no life-threatening sequelae.",
                                "&le;&nbsp;4 hours.",
                            ],
                            [
                                "SEV-3 / Near Miss",
                                "Bundle breach or line issue intercepted before "
                                "infection.",
                                "&le;&nbsp;24 hours.",
                            ],
                        ],
                        col_widths=[1.2 * inch, 3.2 * inch, 1.4 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Completed insertion checklist with site, catheter type, "
                            "number of lumens, and observer name.",
                            "Daily line-necessity assessment and dressing/hub-care "
                            "records.",
                            "For a confirmed CLABSI: organism, date of positive "
                            "culture, central line days, assigned severity, and all "
                            "notifications; reported to NHSN by Infection Prevention.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CDC/HICPAC, Guidelines for the Prevention of "
                            "Intravascular Catheter-Related Infections (2011, with "
                            "updates).",
                            "SHEA/IDSA/APIC, Strategies to Prevent CLABSI in Acute "
                            "Care Hospitals (2022 Update).",
                            "CDC NHSN, Bloodstream Infection Event (CLABSI) "
                            "surveillance definition, Patient Safety Component "
                            "Manual.",
                            "Related: POL-RM-013 (severity &amp; reporting), "
                            "POL-IC-020 (hand hygiene).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_cauti() -> PolicyDoc:
    """Catheter-associated urinary tract infection prevention."""
    return PolicyDoc(
        number="POL-IC-022",
        title="Catheter-Associated Urinary Tract Infection (CAUTI) Prevention",
        owner="Infection Prevention & Control / Nursing",
        effective="2023-08-15",
        revised="2026-02-18",
        review="2028-02-18",
        version="3.1",
        approved_by=_APPROVER,
        applies_to="All units and providers who insert, maintain, or order indwelling "
        "urinary catheters",
        keywords=[
            "cauti",
            "urinary catheter",
            "foley",
            "indwelling catheter",
            "appropriate indications",
            "prompt removal",
            "nurse-driven protocol",
            "nhsn",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To reduce catheter-associated urinary tract infections by "
                        "limiting indwelling urinary catheter use to appropriate "
                        "indications, inserting aseptically, and removing promptly, "
                        "consistent with the CDC/HICPAC Guideline for Prevention of "
                        "Catheter-Associated Urinary Tract Infections."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Indwelling urinary catheter</b> — a drainage catheter "
                            "(Foley) left in place and retained by an inflated "
                            "balloon.",
                            "<b>CAUTI</b> — a urinary tract infection in a patient who "
                            "had an indwelling urinary catheter in place for "
                            "&gt;&nbsp;2 consecutive days on the date of the event, "
                            "per the NHSN surveillance definition.",
                            "<b>Nurse-driven removal protocol</b> — a standing order "
                            "allowing nursing to remove a catheter once no "
                            "appropriate indication remains, without an additional "
                            "provider order.",
                        ]
                    ),
                ],
            ),
            Section(
                "Appropriate Indications and Procedure",
                [
                    Para(
                        "Insert an indwelling urinary catheter only for an "
                        "appropriate indication and remove it as soon as the "
                        "indication resolves. Do not use indwelling catheters to "
                        "manage incontinence or for staff or patient convenience."
                    ),
                    TableBlock(
                        headers=["Appropriate", "Not appropriate"],
                        rows=[
                            [
                                "Acute retention or bladder outlet obstruction.",
                                "Management of incontinence in a continent or "
                                "cooperative patient.",
                            ],
                            [
                                "Accurate output measurement in the critically ill.",
                                "As a substitute for nursing care of an incontinent "
                                "patient.",
                            ],
                            [
                                "Selected peri-operative use; prolonged surgery; "
                                "large-volume infusion or diuresis.",
                                "Prolonged post-operative use without a continuing "
                                "indication.",
                            ],
                            [
                                "Healing of open sacral or perineal wounds in an "
                                "incontinent patient; required prolonged "
                                "immobilization; comfort at end of life.",
                                "Obtaining a urine culture or other diagnostic test "
                                "when the patient can void.",
                            ],
                        ],
                        col_widths=[2.9 * inch, 2.9 * inch],
                    ),
                    Steps(
                        [
                            "Perform hand hygiene and insert using aseptic technique "
                            "and sterile equipment, with the smallest effective "
                            "catheter.",
                            "Secure the catheter, maintain a sterile closed drainage "
                            "system, and keep the bag below the bladder and off the "
                            "floor at all times.",
                            "Assess necessity every shift and remove at the earliest "
                            "indication under the nurse-driven protocol.",
                            "Do not irrigate routinely; do not change catheters or "
                            "bags at fixed arbitrary intervals.",
                        ]
                    ),
                    Note(
                        "Review the necessity of every indwelling urinary catheter "
                        "every shift and remove it the moment no appropriate "
                        "indication remains. Duration of catheterization is the most "
                        "important modifiable risk factor for CAUTI; nursing may "
                        "remove under the standing protocol without a new order."
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Each CAUTI is classified under POL-RM-013. A CAUTI "
                        "progressing to urosepsis, bacteremia, ICU transfer, or death "
                        "is SEV-1 and requires notification of the attending "
                        "provider, Charge Nurse, Nursing Supervisor, Risk Management, "
                        "Infection Prevention, and the Administrator-on-Call "
                        "immediately and within 1 hour of discovery. An uncomplicated "
                        "CAUTI requiring antimicrobial treatment is SEV-2 &mdash; "
                        "notify the attending provider, Charge Nurse, Risk "
                        "Management, and Infection Prevention within 4 hours. A "
                        "catheter kept in without a valid indication but caught "
                        "before infection is a Near Miss, reported within 24 hours."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Documented indication at insertion; insertion date, "
                            "time, and aseptic technique.",
                            "Daily necessity review and date/time of removal.",
                            "For a confirmed CAUTI: organism, catheter days, assigned "
                            "severity, and all notifications; reported to NHSN by "
                            "Infection Prevention.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CDC/HICPAC, Guideline for Prevention of "
                            "Catheter-Associated Urinary Tract Infections (2009).",
                            "SHEA/IDSA/APIC, Strategies to Prevent CAUTI in Acute "
                            "Care Hospitals (2022 Update).",
                            "CDC NHSN, Urinary Tract Infection (CAUTI) surveillance "
                            "definition, Patient Safety Component Manual.",
                            "Related: POL-RM-013 (severity &amp; reporting), "
                            "POL-IC-020 (hand hygiene).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_ssi() -> PolicyDoc:
    """Surgical site infection prevention."""
    return PolicyDoc(
        number="POL-IC-023",
        title="Surgical Site Infection (SSI) Prevention",
        owner="Infection Prevention & Control / Perioperative Services",
        effective="2023-10-01",
        revised="2026-03-12",
        review="2028-03-12",
        version="2.3",
        approved_by=_APPROVER,
        applies_to="All operative and invasive-procedure areas, surgeons, "
        "anesthesia, and perioperative nursing",
        keywords=[
            "ssi",
            "surgical site infection",
            "antimicrobial prophylaxis",
            "normothermia",
            "glycemic control",
            "skin prep",
            "clippers",
            "nhsn",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To prevent surgical site infections through evidence-based "
                        "perioperative practices, consistent with the CDC Guideline "
                        "for the Prevention of Surgical Site Infection (2017), the "
                        "WHO Global Guidelines, and AORN perioperative standards."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Superficial incisional SSI</b> — infection within 30 "
                            "days involving only skin and subcutaneous tissue of the "
                            "incision (NHSN).",
                            "<b>Deep incisional SSI</b> — infection involving deep "
                            "soft tissues (fascia and muscle) of the incision.",
                            "<b>Organ/space SSI</b> — infection involving any part of "
                            "the anatomy opened or manipulated during the operation, "
                            "within the NHSN surveillance window (30 or 90 days by "
                            "procedure).",
                            "<b>Normothermia</b> — maintenance of perioperative core "
                            "temperature at or above 36&deg;C.",
                        ]
                    ),
                ],
            ),
            Section(
                "Perioperative Bundle",
                [
                    TableBlock(
                        headers=["Element", "Standard"],
                        rows=[
                            [
                                "Antimicrobial prophylaxis",
                                "Administer within 60 minutes before incision (within "
                                "120 minutes for vancomycin or a fluoroquinolone); "
                                "redose for long cases or major blood loss; "
                                "discontinue appropriately after closure.",
                            ],
                            [
                                "Hair removal",
                                "Do not remove hair unless it interferes with the "
                                "operation; if needed, use clippers &mdash; never a "
                                "razor.",
                            ],
                            [
                                "Skin antisepsis",
                                "Alcohol-based antiseptic skin prep unless "
                                "contraindicated; allow to dry fully before draping.",
                            ],
                            [
                                "Glycemic control",
                                "Maintain perioperative blood glucose below "
                                "200&nbsp;mg/dL in patients with and without "
                                "diabetes.",
                            ],
                            [
                                "Normothermia",
                                "Maintain perioperative normothermia (&ge;&nbsp;"
                                "36&deg;C).",
                            ],
                        ],
                        col_widths=[1.7 * inch, 4.1 * inch],
                    ),
                    Note(
                        "Prophylactic antimicrobials must be fully infused within 60 "
                        "minutes before incision &mdash; 120 minutes for vancomycin "
                        "or a fluoroquinolone. Do not proceed to incision for an "
                        "elective case until indicated prophylaxis has been given and "
                        "the surgical time-out is complete."
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "SSIs are classified under POL-RM-013. An organ/space SSI, or "
                        "any SSI causing sepsis, unplanned return to the OR, or death "
                        "is SEV-1 &mdash; notify the attending surgeon, Charge Nurse, "
                        "Nursing Supervisor, Risk Management, Infection Prevention, "
                        "and the Administrator-on-Call immediately and within 1 hour. "
                        "A deep or superficial incisional SSI requiring antibiotics "
                        "or bedside intervention is SEV-2, reported to the surgeon, "
                        "Charge Nurse, Risk Management, and Infection Prevention "
                        "within 4 hours. A bundle miss (e.g., late prophylaxis) "
                        "caught before harm is a Near Miss, reported within 24 hours. "
                        "A retained foreign object or wrong-site procedure is a "
                        "Serious Reportable Event and always SEV-1."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Antibiotic agent, dose, and infusion time relative to "
                            "incision; redosing.",
                            "Skin-prep agent, hair-removal method, and documented "
                            "perioperative temperature and glucose values.",
                            "For a confirmed SSI: depth classification, organism, "
                            "procedure and surveillance window, assigned severity, "
                            "and all notifications; reported to NHSN by Infection "
                            "Prevention.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CDC, Guideline for the Prevention of Surgical Site "
                            "Infection, 2017.",
                            "WHO, Global Guidelines for the Prevention of Surgical "
                            "Site Infection (2016/2018).",
                            "AORN, Guidelines for Perioperative Practice; SHEA/IDSA/"
                            "APIC, Strategies to Prevent SSI (2022 Update).",
                            "CDC NHSN, Surgical Site Infection Event surveillance "
                            "definitions. Related: POL-RM-013, POL-IC-020.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_isolation() -> PolicyDoc:
    """Transmission-based (isolation) precautions."""
    return PolicyDoc(
        number="POL-IC-024",
        title="Transmission-Based (Isolation) Precautions",
        owner="Infection Prevention & Control",
        effective="2023-05-01",
        revised="2026-01-15",
        review="2028-01-15",
        version="4.1",
        approved_by=_APPROVER,
        applies_to="All clinical staff, providers, environmental services, and "
        "visitors in every inpatient and outpatient area",
        keywords=[
            "isolation",
            "transmission-based precautions",
            "contact",
            "droplet",
            "airborne",
            "standard precautions",
            "ppn95",
            "aiir",
            "ppe",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To prevent transmission of infectious agents by applying "
                        "Standard Precautions to all patients and adding "
                        "Transmission-Based Precautions when a pathogen&rsquo;s route "
                        "of spread requires it, consistent with the CDC Guideline for "
                        "Isolation Precautions."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Standard Precautions</b> — the baseline practices "
                            "applied to all patients regardless of diagnosis: hand "
                            "hygiene, PPE based on anticipated exposure, respiratory "
                            "hygiene, and safe injection practices.",
                            "<b>Transmission-Based Precautions</b> — Contact, "
                            "Droplet, and Airborne precautions added when a pathogen "
                            "is known or suspected.",
                            "<b>AIIR</b> — airborne infection isolation room: a "
                            "single room at negative pressure with &ge;&nbsp;12 air "
                            "changes per hour, air exhausted outside or HEPA-"
                            "filtered.",
                            "<b>Fit-tested respirator</b> — an N95 or higher "
                            "respirator required for airborne precautions.",
                        ]
                    ),
                ],
            ),
            Section(
                "Precaution Types",
                [
                    Para(
                        "Initiate precautions empirically on clinical suspicion "
                        "&mdash; do not wait for confirmatory testing. Combine "
                        "precaution types when a pathogen spreads by more than one "
                        "route."
                    ),
                    TableBlock(
                        headers=["Type", "PPE / placement", "Example pathogens"],
                        rows=[
                            [
                                "<b>Contact</b>",
                                "Gown and gloves on room entry; single room "
                                "preferred; dedicated equipment.",
                                "MRSA, VRE, <i>C. difficile</i>, RSV, scabies.",
                            ],
                            [
                                "<b>Droplet</b>",
                                "Surgical mask within 6 feet; single room preferred; "
                                "patient masked for transport.",
                                "Influenza, pertussis, <i>N. meningitidis</i>, "
                                "mumps.",
                            ],
                            [
                                "<b>Airborne</b>",
                                "Fit-tested N95 or PAPR; AIIR with door closed; "
                                "patient masked for transport.",
                                "<i>M. tuberculosis</i>, measles, varicella, "
                                "disseminated zoster.",
                            ],
                        ],
                        col_widths=[1.0 * inch, 2.7 * inch, 2.1 * inch],
                    ),
                    Note(
                        "A patient with known or suspected airborne disease (e.g., "
                        "active TB, measles, or varicella) must be placed "
                        "immediately in an AIIR with the door closed, and staff must "
                        "wear a fit-tested N95 or PAPR before entry. If no AIIR is "
                        "available, mask the patient, move them to a private room, "
                        "and contact Infection Prevention at once."
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Isolation events are classified under POL-RM-013. A failure "
                        "to isolate that results in an exposure of staff or other "
                        "patients to a high-consequence airborne pathogen (e.g., "
                        "measles or active pulmonary TB) is escalated as SEV-1 and "
                        "requires notification of the Nursing Supervisor, Risk "
                        "Management, Infection Prevention, Employee Health, and the "
                        "Administrator-on-Call immediately and within 1 hour. A "
                        "precaution breach causing a lower-risk exposure needing "
                        "intervention is SEV-2 (notify within 4 hours). A breach with "
                        "no exposure, or one intercepted at the door, is SEV-3 or a "
                        "Near Miss, reported within 24 hours."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Precaution type initiated, the indication, and date/time "
                            "started and discontinued.",
                            "Room type used (single room, AIIR) and signage posted.",
                            "For any breach or exposure: persons exposed, the event "
                            "report, assigned severity, and all notifications; "
                            "exposure follow-up coordinated with Employee Health.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CDC/HICPAC, Guideline for Isolation Precautions: "
                            "Preventing Transmission of Infectious Agents in "
                            "Healthcare Settings (2007, with updates).",
                            "The Joint Commission, Infection Prevention and Control "
                            "(IC) standards; CMS Conditions of Participation, 42 CFR "
                            "482.42.",
                            "Related: POL-RM-013 (severity &amp; reporting), "
                            "POL-IC-020 (hand hygiene), POL-IC-026 (tuberculosis).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_mdro() -> PolicyDoc:
    """Multidrug-resistant organism management."""
    return PolicyDoc(
        number="POL-IC-025",
        title="Multidrug-Resistant Organism (MDRO) Management",
        owner="Infection Prevention & Control",
        effective="2024-01-10",
        revised="2026-02-25",
        review="2028-02-25",
        version="2.1",
        approved_by=_APPROVER,
        applies_to="All clinical units, the laboratory, antimicrobial stewardship, "
        "and environmental services",
        keywords=[
            "mdro",
            "multidrug-resistant organism",
            "mrsa",
            "vre",
            "cre",
            "carbapenem-resistant",
            "active surveillance",
            "antimicrobial stewardship",
            "cohorting",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To detect, contain, and prevent transmission of "
                        "multidrug-resistant organisms, consistent with the CDC/"
                        "HICPAC Management of Multidrug-Resistant Organisms in "
                        "Healthcare Settings and the CDC Containment Strategy for "
                        "novel or targeted resistance."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>MDRO</b> — a microorganism resistant to one or more "
                            "classes of antimicrobial agents, including MRSA, VRE, "
                            "ESBL-producing Enterobacterales, and carbapenem-"
                            "resistant organisms.",
                            "<b>CRE</b> — carbapenem-resistant Enterobacterales, a "
                            "high-consequence, often carbapenemase-producing MDRO.",
                            "<b>Active surveillance testing</b> — screening cultures "
                            "(e.g., nares, rectal) of at-risk patients to detect "
                            "asymptomatic colonization.",
                            "<b>Cohorting</b> — grouping colonized or infected "
                            "patients (and, where needed, dedicated staff) to limit "
                            "transmission.",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy and Procedure",
                [
                    Steps(
                        [
                            "Place any patient known or suspected to carry an MDRO on "
                            "Contact Precautions (gown and gloves) in a single room "
                            "when available; cohort when single rooms are scarce.",
                            "Perform active surveillance testing for targeted "
                            "organisms (e.g., CRE, <i>Candida auris</i>) on admission "
                            "for defined high-risk populations and on transfer from "
                            "high-prevalence facilities.",
                            "Dedicate noncritical equipment to the patient; clean and "
                            "disinfect shared equipment and the environment with an "
                            "EPA-registered agent effective against the organism.",
                            "Engage Antimicrobial Stewardship for appropriate therapy "
                            "and de-escalation; notify the laboratory to flag and "
                            "report targeted organisms promptly.",
                        ]
                    ),
                    Note(
                        "A single clinical or surveillance isolate of a "
                        "carbapenemase-producing organism or <i>Candida auris</i> "
                        "must be reported to Infection Prevention and the state "
                        "health department immediately, and the patient placed on "
                        "Contact Precautions at once &mdash; these novel/targeted "
                        "resistance findings trigger the CDC Containment Strategy, "
                        "including a point-prevalence survey of contacts."
                    ),
                ],
            ),
            Section(
                "MDRO Classification",
                [
                    TableBlock(
                        headers=["Tier", "Organisms", "Response"],
                        rows=[
                            [
                                "<b>Containment</b>",
                                "CRE/CP-CRE, <i>C. auris</i>, novel resistance "
                                "mechanisms.",
                                "Immediate isolation, public-health notification, "
                                "point-prevalence survey.",
                            ],
                            [
                                "<b>Endemic</b>",
                                "MRSA, VRE, ESBL producers.",
                                "Contact Precautions, surveillance, routine "
                                "reporting.",
                            ],
                            [
                                "<b>C. difficile</b>",
                                "Toxigenic <i>C. difficile</i>.",
                                "Contact Precautions, soap-and-water hand hygiene, "
                                "sporicidal cleaning.",
                            ],
                        ],
                        col_widths=[1.3 * inch, 2.3 * inch, 2.2 * inch],
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "MDRO events follow POL-RM-013. Identification of a "
                        "containment-tier organism (CP-CRE, <i>C. auris</i>), or any "
                        "MDRO infection progressing to sepsis or death, is SEV-1 "
                        "&mdash; notify the attending provider, Nursing Supervisor, "
                        "Risk Management, Infection Prevention, and the "
                        "Administrator-on-Call immediately and within 1 hour, and "
                        "Infection Prevention notifies the state health department. "
                        "A new healthcare-associated MDRO infection requiring "
                        "treatment is SEV-2 (notify within 4 hours). New "
                        "colonization without infection, or a lapse caught before "
                        "transmission, is SEV-3 or a Near Miss, reported within 24 "
                        "hours."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Organism, specimen source, resistance mechanism (if "
                            "known), and whether colonization or infection.",
                            "Precautions initiated, room/cohort assignment, and "
                            "surveillance-testing results.",
                            "For containment organisms: public-health notification "
                            "and point-prevalence survey; assigned severity and all "
                            "notifications.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CDC/HICPAC, Management of Multidrug-Resistant Organisms "
                            "in Healthcare Settings (2006, with updates).",
                            "CDC, Interim Guidance for a Public Health Response to "
                            "Contain Novel or Targeted MDROs (Containment Strategy).",
                            "SHEA/IDSA/APIC Compendium strategies for MRSA, CRE, and "
                            "<i>C. difficile</i>.",
                            "Related: POL-RM-013, POL-IC-020, POL-IC-024.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_tuberculosis() -> PolicyDoc:
    """Tuberculosis exposure control."""
    return PolicyDoc(
        number="POL-IC-026",
        title="Tuberculosis Exposure Control",
        owner="Infection Prevention & Control / Employee Health",
        effective="2023-07-15",
        revised="2026-03-01",
        review="2028-03-01",
        version="3.0",
        approved_by=_APPROVER,
        applies_to="All staff, providers, and areas where patients with suspected or "
        "confirmed tuberculosis may be encountered",
        keywords=[
            "tuberculosis",
            "tb",
            "airborne",
            "aiir",
            "n95",
            "respiratory protection",
            "igra",
            "tst",
            "exposure control plan",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To prevent transmission of <i>Mycobacterium tuberculosis</i> "
                        "to patients and staff through early identification, airborne "
                        "isolation, respiratory protection, and employee testing, "
                        "consistent with CDC guidance and the OSHA respiratory "
                        "protection standard."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Active (infectious) TB</b> — clinically active "
                            "disease, typically pulmonary or laryngeal, capable of "
                            "airborne transmission.",
                            "<b>Latent TB infection (LTBI)</b> — infection without "
                            "active disease; not infectious.",
                            "<b>AIIR</b> — airborne infection isolation room at "
                            "negative pressure with &ge;&nbsp;12 air changes per "
                            "hour.",
                            "<b>IGRA / TST</b> — interferon-gamma release assay or "
                            "tuberculin skin test used for baseline and post-exposure "
                            "screening.",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy and Procedure",
                [
                    Steps(
                        [
                            "Triage: identify patients with signs/symptoms of TB "
                            "(cough &gt;&nbsp;3 weeks, fever, night sweats, weight "
                            "loss) and mask them immediately.",
                            "Place any patient with suspected or confirmed infectious "
                            "TB in an AIIR on Airborne Precautions; keep the door "
                            "closed.",
                            "All staff entering the room wear a fit-tested N95 or "
                            "PAPR; fit testing is performed at least annually per "
                            "OSHA 29 CFR 1910.134.",
                            "Discontinue airborne isolation only when TB is excluded "
                            "or the patient meets criteria for non-infectiousness as "
                            "determined by Infection Prevention and the treating "
                            "provider.",
                        ]
                    ),
                    Note(
                        "A patient with suspected or confirmed infectious TB must be "
                        "placed in an AIIR with the door closed before any "
                        "non-masked contact, and all entrants must wear a fit-tested "
                        "N95 or PAPR. If no AIIR is available, mask the patient, "
                        "limit entries, and contact Infection Prevention "
                        "immediately to arrange transfer."
                    ),
                ],
            ),
            Section(
                "Employee Testing and Exposure",
                [
                    TableBlock(
                        headers=["Situation", "Action"],
                        rows=[
                            [
                                "Baseline (on hire)",
                                "Individual TB risk assessment, symptom evaluation, "
                                "and an IGRA or two-step TST.",
                            ],
                            [
                                "Annual",
                                "No routine testing of asymptomatic staff absent "
                                "exposure or ongoing risk; annual TB education for "
                                "all.",
                            ],
                            [
                                "After unprotected exposure",
                                "Symptom screen and baseline test if not known "
                                "positive; repeat IGRA/TST 8&ndash;10 weeks after the "
                                "last exposure.",
                            ],
                        ],
                        col_widths=[1.9 * inch, 3.9 * inch],
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "TB events follow POL-RM-013. An unprotected staff or patient "
                        "exposure to a patient with confirmed infectious TB, or a "
                        "confirmed healthcare transmission, is escalated as SEV-1 "
                        "&mdash; notify the Nursing Supervisor, Risk Management, "
                        "Infection Prevention, Employee Health, and the "
                        "Administrator-on-Call immediately and within 1 hour; "
                        "Infection Prevention reports confirmed TB to the state "
                        "health department. An isolation or respiratory-protection "
                        "breach requiring an exposure investigation is SEV-2 (notify "
                        "within 4 hours). A breach caught before exposure is a Near "
                        "Miss, reported within 24 hours. Exposed staff follow-up is "
                        "coordinated by Employee Health, including repeat testing at "
                        "8&ndash;10 weeks."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Patient triage, masking, AIIR placement, and isolation "
                            "start/stop times.",
                            "Staff respirator fit-test records and N95/PAPR use.",
                            "For an exposure: list of exposed persons, baseline and "
                            "follow-up test results, assigned severity, public-health "
                            "notification, and all notifications.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CDC, Guidelines for Preventing the Transmission of "
                            "<i>M. tuberculosis</i> in Health-Care Settings, MMWR "
                            "2005; CDC/NTCA Testing of Health Care Personnel (2019).",
                            "OSHA Respiratory Protection Standard, 29 CFR 1910.134 "
                            "(fit testing, medical evaluation).",
                            "CMS Conditions of Participation, 42 CFR 482.42.",
                            "Related: POL-RM-013, POL-IC-024 (isolation), POL-EH-001 "
                            "(occupational exposure).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_reprocessing() -> PolicyDoc:
    """Reusable medical device reprocessing and sterilization."""
    return PolicyDoc(
        number="POL-IC-027",
        title="Reusable Medical Device Reprocessing and Sterilization",
        owner="Sterile Processing / Infection Prevention & Control",
        effective="2023-11-01",
        revised="2026-03-20",
        review="2028-03-20",
        version="2.2",
        approved_by=_APPROVER,
        applies_to="Sterile Processing, perioperative and procedural areas, "
        "endoscopy, and any area that reprocesses reusable devices",
        keywords=[
            "sterilization",
            "disinfection",
            "reprocessing",
            "spaulding",
            "high-level disinfection",
            "endoscope",
            "biological indicator",
            "instructions for use",
            "ifu",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To ensure reusable medical devices are cleaned, disinfected, "
                        "and sterilized correctly and consistently with the "
                        "manufacturer&rsquo;s instructions for use (IFU) and the "
                        "Spaulding classification, consistent with CDC, AAMI, and "
                        "AORN standards."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Cleaning</b> — removal of visible soil and organic "
                            "material; a prerequisite for all disinfection and "
                            "sterilization.",
                            "<b>High-level disinfection (HLD)</b> — a process that "
                            "kills all microorganisms except large numbers of "
                            "bacterial spores.",
                            "<b>Sterilization</b> — a validated process that "
                            "destroys all microbial life, including spores.",
                            "<b>IFU</b> — the device manufacturer&rsquo;s "
                            "instructions for use, which govern the validated "
                            "reprocessing method and are followed exactly.",
                        ]
                    ),
                ],
            ),
            Section(
                "Spaulding Classification",
                [
                    Para(
                        "The required level of reprocessing is determined by how the "
                        "device contacts the patient. When the IFU and this table "
                        "conflict, follow the stricter requirement and consult "
                        "Infection Prevention."
                    ),
                    TableBlock(
                        headers=["Category", "Contact", "Minimum reprocessing"],
                        rows=[
                            [
                                "<b>Critical</b>",
                                "Enters sterile tissue or the vascular system.",
                                "Sterilization (e.g., surgical instruments, "
                                "implants).",
                            ],
                            [
                                "<b>Semi-critical</b>",
                                "Contacts mucous membranes or non-intact skin.",
                                "High-level disinfection (e.g., flexible endoscopes, "
                                "laryngoscope blades).",
                            ],
                            [
                                "<b>Non-critical</b>",
                                "Contacts intact skin only.",
                                "Low- or intermediate-level disinfection (e.g., BP "
                                "cuffs, stethoscopes).",
                            ],
                        ],
                        col_widths=[1.2 * inch, 2.4 * inch, 2.2 * inch],
                    ),
                    Note(
                        "Every sterilizer load containing an implant must include a "
                        "biological indicator, and the implant is quarantined and "
                        "not released until the biological indicator result is "
                        "confirmed negative. Never release an implant on the basis "
                        "of chemical indicators alone."
                    ),
                ],
            ),
            Section(
                "Procedure",
                [
                    Steps(
                        [
                            "Pre-clean at the point of use to prevent soil from "
                            "drying; transport soiled items in a closed, labeled "
                            "container to the decontamination area.",
                            "Clean per IFU, then inspect for cleanliness and "
                            "function before disinfection or sterilization.",
                            "Monitor every sterilizer load with mechanical, chemical, "
                            "and biological indicators; run a biological indicator at "
                            "least daily (and in every implant load).",
                            "Document HLD cycles (solution, concentration test, "
                            "contact time, temperature) and endoscope reprocessing, "
                            "including storage; maintain lot/load traceability to the "
                            "patient.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Reprocessing failures are classified under POL-RM-013. Use "
                        "of an improperly reprocessed critical or semi-critical "
                        "device on a patient, or a positive biological indicator "
                        "requiring patient notification/look-back, is escalated as "
                        "SEV-1 (or SEV-2 if no infection results and only monitoring "
                        "is needed) &mdash; for SEV-1 notify the attending provider, "
                        "Nursing Supervisor, Risk Management, Infection Prevention, "
                        "and the Administrator-on-Call immediately and within 1 hour. "
                        "A documentation or cycle-monitoring lapse without patient "
                        "exposure is SEV-3, and a failed load caught before any "
                        "device is used is a Near Miss; both are reported to "
                        "Infection Prevention within 24 hours. A device-related "
                        "injury may also be reportable to the FDA via MedWatch by "
                        "Risk Management."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Load records with mechanical, chemical, and biological "
                            "indicator results, and lot/load-to-patient "
                            "traceability.",
                            "HLD logs (solution potency test, contact time, "
                            "temperature) and endoscope reprocessing and storage "
                            "records.",
                            "For any failure: devices and patients affected, "
                            "look-back actions, assigned severity, FDA/public-health "
                            "notification if applicable, and all notifications.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CDC, Guideline for Disinfection and Sterilization in "
                            "Healthcare Facilities (2008, with updates); Spaulding "
                            "classification.",
                            "ANSI/AAMI ST79 (steam sterilization) and ST91 (flexible "
                            "endoscope reprocessing); AORN perioperative guidelines.",
                            "The Joint Commission IC standards; CMS Conditions of "
                            "Participation, 42 CFR 482.42.",
                            "Related: POL-RM-013 (severity &amp; reporting), "
                            "POL-IC-020 (hand hygiene).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_batch() -> list[PolicyDoc]:
    """Return this batch's policies, in listed order."""
    return [
        build_hand_hygiene(),
        build_clabsi(),
        build_cauti(),
        build_ssi(),
        build_isolation(),
        build_mdro(),
        build_tuberculosis(),
        build_reprocessing(),
    ]
