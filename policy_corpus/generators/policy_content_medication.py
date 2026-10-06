"""Medication-safety batch of the hospital policy corpus.

This module holds eight high-risk medication-management policies for the
fictional Riverside Regional Medical Center (anticoagulation, insulin/glycemic
control, high-alert medications, look-alike/sound-alike pairs, medication
reconciliation, controlled-substance diversion prevention, adverse drug
reaction reporting, and moderate/procedural sedation). Each ``build_*``
function returns one :class:`PolicyDoc` anchored to a real standard (TJC NPSG,
ISMP, NCC MERP, CMS CoP, DEA, FDA MedWatch, ASA sedation guidelines) and tied
into the facility-wide severity scale defined in POL-RM-013, cross-referencing
the medication-error policy POL-PS-003 where relevant.
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

_APPROVER = "Pharmacy & Therapeutics Committee"


def build_anticoagulation() -> PolicyDoc:
    """Safe management of anticoagulant therapy per TJC NPSG.03.05.01."""
    return PolicyDoc(
        number="POL-PH-030",
        title="Anticoagulation Management",
        owner="Pharmacy / Nursing",
        effective="2023-06-01",
        revised="2026-03-12",
        review="2028-03-12",
        version="3.1",
        approved_by=_APPROVER,
        applies_to="All prescribers, pharmacists, and nurses who order, dispense, "
        "administer, or monitor therapeutic anticoagulation in any inpatient or "
        "observation unit",
        keywords=[
            "anticoagulation",
            "warfarin",
            "heparin",
            "doac",
            "inr",
            "reversal",
            "npsg",
            "high-alert",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To reduce patient harm associated with therapeutic "
                        "anticoagulant therapy through standardized ordering, "
                        "weight-based dosing, laboratory monitoring, patient "
                        "education, and defined reversal protocols, in compliance "
                        "with The Joint Commission National Patient Safety Goal "
                        "NPSG.03.05.01."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to all therapeutic anticoagulation: warfarin, "
                        "unfractionated heparin (UFH) infusions, low-molecular-weight "
                        "heparins (LMWH), and direct oral anticoagulants (DOACs). It "
                        "does not apply to routine short-term prophylactic "
                        "venous-thromboembolism (VTE) prevention related to a "
                        "procedure or hospitalization, which is addressed by the VTE "
                        "prophylaxis order set."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Anticoagulant</b> — a medication that reduces the "
                            "blood&rsquo;s ability to clot; a high-alert medication per "
                            "the ISMP list.",
                            "<b>DOAC</b> — direct oral anticoagulant (e.g., apixaban, "
                            "rivaroxaban, dabigatran, edoxaban).",
                            "<b>Therapeutic range</b> — the target INR band for "
                            "warfarin (commonly 2.0&ndash;3.0; 2.5&ndash;3.5 for "
                            "mechanical mitral valves) or the aPTT/anti-Xa band for a "
                            "heparin infusion.",
                            "<b>Reversal agent</b> — a product that restores "
                            "hemostasis by countering an anticoagulant (e.g., vitamin "
                            "K, 4-factor PCC, idarucizumab, andexanet alfa, protamine "
                            "sulfate).",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy and Procedure",
                [
                    Para(
                        "Use the approved weight-based order sets and nomograms for "
                        "all anticoagulant orders; free-text anticoagulant orders are "
                        "not permitted. Current weight in kilograms must be in the "
                        "record before the first dose. Baseline labs (CBC, INR/PT, "
                        "aPTT, renal function) are obtained before initiation and "
                        "monitored per the nomogram."
                    ),
                    Steps(
                        [
                            "Verify indication, current weight (kg), renal/hepatic "
                            "function, and baseline coagulation labs before the first "
                            "dose.",
                            "Enter the order through the approved anticoagulant order "
                            "set; pharmacy performs an independent dose and "
                            "interaction check before dispensing.",
                            "Two nurses independently verify drug, concentration, "
                            "pump settings, and dose for all heparin infusions "
                            "(independent double check).",
                            "Monitor the appropriate parameter (INR, aPTT, or "
                            "anti-Xa) on the schedule defined by the nomogram and "
                            "adjust per protocol.",
                            "Provide anticoagulant-specific education to the patient "
                            "and family and document understanding before discharge.",
                        ]
                    ),
                    Note(
                        "For any major or life-threatening bleed on an "
                        "anticoagulant, hold all further doses immediately, notify "
                        "the prescriber STAT, and initiate the approved reversal "
                        "protocol for that specific agent without waiting for lab "
                        "results. Treat as SEV-1 and notify Risk Management within "
                        "1 hour."
                    ),
                ],
            ),
            Section(
                "Reversal Agents by Anticoagulant",
                [
                    Para(
                        "The following approved reversal strategies are stocked and "
                        "available on a STAT basis."
                    ),
                    TableBlock(
                        headers=["Anticoagulant", "First-line reversal", "Notes"],
                        rows=[
                            [
                                "Warfarin",
                                "Vitamin K + 4-factor PCC",
                                "Dose PCC by weight &amp; INR; give FFP if PCC "
                                "unavailable.",
                            ],
                            [
                                "UFH / LMWH",
                                "Protamine sulfate",
                                "Weight- &amp; time-based dosing; partial LMWH "
                                "reversal only.",
                            ],
                            [
                                "Dabigatran",
                                "Idarucizumab",
                                "Dialyzable; idarucizumab is the specific antidote.",
                            ],
                            [
                                "Apixaban / rivaroxaban",
                                "Andexanet alfa",
                                "4-factor PCC is an alternative if unavailable.",
                            ],
                        ],
                        col_widths=[1.5 * inch, 1.7 * inch, 2.6 * inch],
                    ),
                ],
            ),
            Section(
                "Severity &amp; Reporting",
                [
                    Para(
                        "Classify anticoagulation events on the facility-wide scale "
                        "in POL-RM-013 and report through the event system; medication "
                        "errors are additionally graded by the NCC MERP A&ndash;I harm "
                        "index per POL-PS-003."
                    ),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "Fatal or life-threatening bleed; intracranial "
                                "hemorrhage requiring reversal.",
                                "Prescriber, Nursing Supervisor &amp; Risk Mgmt "
                                "within 1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Supratherapeutic INR with bleed requiring "
                                "transfusion or prolonging stay.",
                                "Prescriber &amp; Risk Mgmt within 4 hours.",
                            ],
                            [
                                "SEV-3 / Near Miss",
                                "Missed INR draw with no harm; wrong dose "
                                "intercepted by pharmacy.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[1.2 * inch, 2.9 * inch, 1.7 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Indication, agent, dose, route, and current weight (kg) "
                            "used for dosing.",
                            "Baseline and ongoing monitoring values (INR, aPTT, or "
                            "anti-Xa) against the target range.",
                            "Independent double check performed for heparin infusions, "
                            "with both verifier names.",
                            "Anticoagulant-specific patient/family education and "
                            "confirmation of understanding.",
                            "Any reversal agent given, with dose, time, and "
                            "prescriber notification.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission NPSG.03.05.01 — Reduce the "
                            "likelihood of patient harm associated with the use of "
                            "anticoagulant therapy.",
                            "ISMP List of High-Alert Medications in Acute Care "
                            "Settings.",
                            "CMS Conditions of Participation, 42 CFR 482.25 "
                            "(pharmaceutical services).",
                            "Related: POL-RM-013 (severity &amp; reporting); "
                            "POL-PS-003 (medication-error reporting); POL-PH-032 "
                            "(high-alert medications).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_insulin() -> PolicyDoc:
    """Safe insulin use and inpatient glycemic management."""
    return PolicyDoc(
        number="POL-PH-031",
        title="Insulin and Glycemic Management",
        owner="Pharmacy / Nursing",
        effective="2023-07-10",
        revised="2026-03-18",
        review="2028-03-18",
        version="2.3",
        approved_by=_APPROVER,
        applies_to="All prescribers, pharmacists, and nurses managing insulin, oral "
        "hypoglycemics, or inpatient glucose in any care area",
        keywords=[
            "insulin",
            "glycemic",
            "hypoglycemia",
            "hyperglycemia",
            "high-alert",
            "blood glucose",
            "basal bolus",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To standardize safe prescribing, dispensing, administration, "
                        "and monitoring of insulin and other glucose-lowering agents, "
                        "and to define the response to hypoglycemia. Insulin is a "
                        "high-alert medication on the ISMP acute-care list."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Hypoglycemia</b> — blood glucose below 70 mg/dL; "
                            "severe hypoglycemia is below 40 mg/dL or any value "
                            "requiring assistance.",
                            "<b>Basal-bolus regimen</b> — scheduled long-acting "
                            "(basal) insulin plus mealtime (bolus/nutritional) and "
                            "correction insulin.",
                            "<b>Concentrated insulin</b> — products more concentrated "
                            "than U-100 (e.g., U-200, U-300, U-500) that require "
                            "special handling.",
                            "<b>Point-of-care (POC) glucose</b> — a bedside capillary "
                            "glucose measurement used to guide dosing.",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy and Procedure",
                [
                    Para(
                        "Insulin orders must specify product, concentration, dose in "
                        "units, and timing relative to meals; the abbreviation "
                        "&ldquo;U&rdquo; for units is prohibited &mdash; write "
                        "&ldquo;units&rdquo; in full. Insulin is dispensed in "
                        "ready-to-use strengths; U-500 and other concentrated "
                        "insulins are stored separately from U-100."
                    ),
                    Steps(
                        [
                            "Confirm a current POC or lab glucose before "
                            "administering mealtime or correction insulin.",
                            "Perform an independent double check of product, "
                            "concentration, and units for every IV insulin infusion "
                            "and for all pediatric doses.",
                            "Match nutritional insulin to actual intake; hold or "
                            "adjust the nutritional dose if the patient is NPO or not "
                            "eating.",
                            "Use only insulin-specific (unit-marked) syringes or the "
                            "approved pen device; never draw insulin into a "
                            "tuberculin or standard syringe.",
                            "Monitor glucose per the ordered schedule and the "
                            "hypoglycemia protocol.",
                        ]
                    ),
                    Note(
                        "For blood glucose below 70 mg/dL, treat immediately per the "
                        "nurse-driven hypoglycemia protocol (15 g fast-acting "
                        "carbohydrate if the patient can swallow safely, or IV "
                        "dextrose / IM glucagon if not), recheck glucose in 15 "
                        "minutes, and notify the provider. Do not delay treatment to "
                        "obtain an order."
                    ),
                ],
            ),
            Section(
                "Glucose Monitoring and Response Parameters",
                [
                    TableBlock(
                        headers=["POC glucose (mg/dL)", "Action"],
                        rows=[
                            [
                                "Less than 54",
                                "Severe hypoglycemia &mdash; treat STAT, give IV "
                                "dextrose/glucagon, notify provider, recheck q15 min.",
                            ],
                            [
                                "54&ndash;69",
                                "Hypoglycemia &mdash; 15 g oral carbohydrate, recheck "
                                "in 15 minutes, repeat until above 70.",
                            ],
                            [
                                "70&ndash;180",
                                "Target inpatient range &mdash; continue ordered "
                                "regimen.",
                            ],
                            [
                                "Greater than 300",
                                "Marked hyperglycemia &mdash; confirm value, assess "
                                "for DKA/HHS, notify provider.",
                            ],
                        ],
                        col_widths=[1.6 * inch, 4.2 * inch],
                    ),
                ],
            ),
            Section(
                "Severity &amp; Reporting",
                [
                    Para(
                        "Classify glycemic and insulin events on the POL-RM-013 scale "
                        "and grade medication errors by the NCC MERP index per "
                        "POL-PS-003."
                    ),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "Severe hypoglycemia causing seizure, coma, or death; "
                                "10-fold insulin overdose.",
                                "Provider, Nursing Supervisor &amp; Risk Mgmt within "
                                "1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Hypoglycemia requiring IV dextrose/glucagon or "
                                "prolonging stay.",
                                "Provider &amp; Risk Mgmt within 4 hours.",
                            ],
                            [
                                "SEV-3 / Near Miss",
                                "Delayed glucose check, no harm; wrong insulin "
                                "intercepted before administration.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[1.2 * inch, 2.9 * inch, 1.7 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Insulin product, concentration, dose in units, route, "
                            "and timing relative to meals.",
                            "POC/lab glucose value and time supporting each dose.",
                            "Independent double check for IV insulin and pediatric "
                            "doses, with verifier names.",
                            "Hypoglycemia treatment given, recheck values, and "
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
                            "ISMP List of High-Alert Medications in Acute Care "
                            "Settings.",
                            "ISMP List of Error-Prone Abbreviations, Symbols, and "
                            "Dose Designations (&ldquo;U&rdquo; for units).",
                            "The Joint Commission NPSG.03.06.01 (medication "
                            "reconciliation) and medication-management standards.",
                            "Related: POL-RM-013 (severity &amp; reporting); "
                            "POL-PS-003 (medication-error reporting); POL-PH-032 "
                            "(high-alert medications).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_high_alert() -> PolicyDoc:
    """Management and double-check controls for high-alert medications."""
    return PolicyDoc(
        number="POL-PH-032",
        title="High-Alert Medication Management",
        owner="Pharmacy",
        effective="2023-05-20",
        revised="2026-02-25",
        review="2028-02-25",
        version="3.0",
        approved_by=_APPROVER,
        applies_to="All staff who prescribe, dispense, administer, or stock "
        "medications identified as high-alert",
        keywords=[
            "high-alert",
            "ismp",
            "independent double check",
            "concentrated electrolytes",
            "neuromuscular blocker",
            "chemotherapy",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To define the identification, storage, prescribing, and "
                        "administration controls for high-alert medications &mdash; "
                        "drugs bearing a heightened risk of significant patient harm "
                        "when used in error &mdash; consistent with the ISMP List of "
                        "High-Alert Medications and CMS pharmaceutical-services "
                        "requirements."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>High-alert medication</b> — a drug with a heightened "
                            "risk of causing significant harm when used in error, "
                            "even though mistakes may or may not be more common.",
                            "<b>Independent double check (IDC)</b> — two qualified "
                            "clinicians separately verify the drug, concentration, "
                            "dose, rate, and patient without prompting each other.",
                            "<b>Maximum concentration</b> — the highest approved "
                            "concentration stocked for a given high-alert drug to "
                            "limit the harm of a programming error.",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy and Procedure",
                [
                    Para(
                        "Pharmacy maintains and publishes the facility high-alert "
                        "medication list, based on the ISMP list and local event "
                        "history, and reviews it at least annually. High-alert "
                        "products are labeled with an auxiliary &ldquo;HIGH "
                        "ALERT&rdquo; indicator and are dispensed in standardized, "
                        "ready-to-administer concentrations whenever possible."
                    ),
                    Steps(
                        [
                            "Prescribe high-alert drugs through standardized order "
                            "sets with built-in dose limits and alerts.",
                            "Perform an independent double check before administering "
                            "the drugs designated as requiring IDC.",
                            "Use smart-pump drug libraries with hard limits for all "
                            "high-alert IV infusions.",
                            "Remove concentrated electrolytes (e.g., potassium "
                            "chloride, concentrated sodium chloride) from floor stock "
                            "except in approved critical-care locations.",
                            "Segregate and distinctively label neuromuscular blocking "
                            "agents, with warnings that they cause respiratory "
                            "arrest/paralysis.",
                        ]
                    ),
                    Note(
                        "Concentrated potassium chloride and other concentrated "
                        "electrolytes must never be stored in general nursing-unit "
                        "floor stock. If a concentrated electrolyte is found in an "
                        "unapproved location, secure it immediately, notify Pharmacy, "
                        "and file a near-miss report within 24 hours."
                    ),
                ],
            ),
            Section(
                "Representative High-Alert Classes and Controls",
                [
                    TableBlock(
                        headers=["Class / example", "Primary control"],
                        rows=[
                            [
                                "Insulin (all forms)",
                                "IDC for IV infusions; separate U-100 from "
                                "concentrated products.",
                            ],
                            [
                                "Anticoagulants (heparin, DOACs)",
                                "Weight-based order sets; IDC for heparin infusions.",
                            ],
                            [
                                "Opioids &amp; parenteral sedatives",
                                "Smart-pump limits; PCA double check; controlled "
                                "access.",
                            ],
                            [
                                "Concentrated electrolytes (KCl)",
                                "Removed from floor stock; pharmacy-prepared only.",
                            ],
                            [
                                "Neuromuscular blocking agents",
                                "Segregated storage; &ldquo;paralyzing agent&rdquo; "
                                "warning labels.",
                            ],
                            [
                                "Chemotherapy / cytotoxics",
                                "Independent verification of regimen, dose, and body "
                                "surface area.",
                            ],
                        ],
                        col_widths=[2.4 * inch, 3.4 * inch],
                    ),
                ],
            ),
            Section(
                "Severity &amp; Escalation",
                [
                    Para(
                        "Classify high-alert medication events on the POL-RM-013 "
                        "scale; a high-alert error that reaches the patient is "
                        "classified at least SEV-2. Grade the error by the NCC MERP "
                        "index per POL-PS-003."
                    ),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "Paralytic given to a non-ventilated patient; fatal "
                                "KCl bolus.",
                                "Provider, Nursing Supervisor &amp; Risk Mgmt within "
                                "1 hour.",
                            ],
                            [
                                "SEV-2",
                                "High-alert drug reaching the patient with temporary "
                                "harm needing intervention.",
                                "Provider &amp; Risk Mgmt within 4 hours.",
                            ],
                            [
                                "SEV-3 / Near Miss",
                                "Missing IDC with no harm; wrong concentration "
                                "intercepted by pharmacy.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[1.2 * inch, 2.9 * inch, 1.7 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Drug, concentration, dose, and route, with the "
                            "high-alert designation noted.",
                            "Independent double check performed and both verifier "
                            "names, where required.",
                            "Smart-pump library selection and any limit override, "
                            "with reason.",
                            "Storage-location corrections for any misplaced "
                            "high-alert product.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "ISMP List of High-Alert Medications in Acute Care "
                            "Settings.",
                            "ISMP Targeted Medication Safety Best Practices for "
                            "Hospitals.",
                            "CMS Conditions of Participation, 42 CFR 482.25 "
                            "(pharmaceutical services).",
                            "Related: POL-RM-013 (severity &amp; reporting); "
                            "POL-PS-003 (medication-error reporting); POL-PH-030, "
                            "POL-PH-031, POL-PH-033.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_lasa() -> PolicyDoc:
    """Controls for look-alike / sound-alike medication confusion."""
    return PolicyDoc(
        number="POL-PH-033",
        title="Look-Alike / Sound-Alike (LASA) Medication Management",
        owner="Pharmacy",
        effective="2023-08-01",
        revised="2026-01-30",
        review="2028-01-30",
        version="2.0",
        approved_by=_APPROVER,
        applies_to="All staff involved in procurement, storage, prescribing, "
        "dispensing, and administration of medications",
        keywords=[
            "lasa",
            "look-alike sound-alike",
            "tall man lettering",
            "ismp",
            "confused drug names",
            "medication safety",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To reduce errors caused by medications whose names look "
                        "alike or sound alike (LASA) through a managed LASA list, "
                        "tall man lettering, storage separation, and verification "
                        "at the point of care, consistent with ISMP guidance and "
                        "The Joint Commission medication-management standards."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>LASA pair</b> — two drug names that are easily "
                            "confused in print (look-alike) or speech (sound-alike), "
                            "e.g., hydrALAZINE / hydrOXYzine.",
                            "<b>Tall man lettering</b> — selective capitalization of "
                            "dissimilar letters within similar names to highlight the "
                            "difference (e.g., predniSONE / prednisoLONE).",
                            "<b>Physical separation</b> — storing confusable products "
                            "in non-adjacent locations or bins to break the error "
                            "chain.",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy and Procedure",
                [
                    Para(
                        "Pharmacy maintains the facility LASA list (drawn from the "
                        "ISMP list of confused drug names and local events), applies "
                        "tall man lettering in the EHR, pharmacy system, labels, and "
                        "automated dispensing cabinets, and reviews the list at least "
                        "annually."
                    ),
                    Steps(
                        [
                            "Store LASA pairs apart, with auxiliary "
                            "&ldquo;LASA&rdquo; shelf and bin warnings.",
                            "Display tall man lettering wherever the drug name "
                            "appears electronically or on a label.",
                            "Read back and confirm any verbal or telephone "
                            "medication order, spelling the drug name.",
                            "Confirm the indication on orders for high-risk LASA "
                            "pairs to disambiguate intent.",
                            "Verify the drug name against the order and the patient "
                            "indication at administration using two patient "
                            "identifiers.",
                        ]
                    ),
                    Note(
                        "For verbal and telephone medication orders, the receiver "
                        "must write down and read back the complete order and spell "
                        "the drug name letter by letter when it belongs to a LASA "
                        "pair, before the medication is prepared or given."
                    ),
                ],
            ),
            Section(
                "Representative LASA Pairs",
                [
                    TableBlock(
                        headers=["Name A", "Name B", "Risk"],
                        rows=[
                            ["hydrALAZINE", "hydrOXYzine", "Look &amp; sound-alike"],
                            ["predniSONE", "prednisoLONE", "Look-alike"],
                            ["DOPamine", "DOBUTamine", "Look &amp; sound-alike"],
                            ["cefTRIAXone", "cefTAZidime", "Look-alike"],
                            ["HumaLOG", "HumuLIN", "Look &amp; sound-alike"],
                            ["vinBLAStine", "vinCRIStine", "Look-alike; fatal if IT"],
                        ],
                        col_widths=[1.9 * inch, 1.9 * inch, 2.0 * inch],
                    ),
                ],
            ),
            Section(
                "Severity &amp; Reporting",
                [
                    Para(
                        "Classify LASA events on the POL-RM-013 scale and grade "
                        "errors by the NCC MERP index per POL-PS-003. Even "
                        "intercepted LASA mix-ups should be reported so the list and "
                        "storage controls can be improved."
                    ),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "vinCRIStine given by wrong route; LASA swap "
                                "contributing to death.",
                                "Provider, Nursing Supervisor &amp; Risk Mgmt within "
                                "1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Wrong LASA drug reaching the patient with temporary "
                                "harm needing treatment.",
                                "Provider &amp; Risk Mgmt within 4 hours.",
                            ],
                            [
                                "SEV-3 / Near Miss",
                                "LASA swap reaching patient without harm; mix-up "
                                "caught at verification.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[1.2 * inch, 2.9 * inch, 1.7 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Both drug names involved and the point in the process "
                            "where confusion occurred.",
                            "Whether tall man lettering and storage separation were "
                            "in place.",
                            "Read-back performed for any verbal/telephone order.",
                            "Whether the error reached the patient and the NCC MERP "
                            "category.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "ISMP List of Confused Drug Names.",
                            "ISMP and FDA Tall Man Lettering lists.",
                            "The Joint Commission medication-management standards "
                            "(verbal/telephone order read-back).",
                            "Related: POL-RM-013 (severity &amp; reporting); "
                            "POL-PS-003 (medication-error reporting); POL-PH-032 "
                            "(high-alert medications).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_med_rec() -> PolicyDoc:
    """Medication reconciliation at every transition of care."""
    return PolicyDoc(
        number="POL-PH-034",
        title="Medication Reconciliation",
        owner="Pharmacy / Nursing",
        effective="2024-01-08",
        revised="2026-03-05",
        review="2028-03-05",
        version="2.2",
        approved_by=_APPROVER,
        applies_to="All prescribers, pharmacists, and nurses responsible for "
        "medication histories and orders at admission, transfer, and discharge",
        keywords=[
            "medication reconciliation",
            "npsg",
            "home medications",
            "transitions of care",
            "discharge",
            "bpmh",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To prevent medication discrepancies &mdash; omissions, "
                        "duplications, dosing errors, and interactions &mdash; by "
                        "comparing the medications a patient is taking against new "
                        "orders at every transition of care, in compliance with The "
                        "Joint Commission National Patient Safety Goal "
                        "NPSG.03.06.01."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Medication reconciliation</b> — the process of "
                            "creating the most accurate list of all medications a "
                            "patient is taking and comparing it against new orders.",
                            "<b>Best possible medication history (BPMH)</b> — a "
                            "history obtained using at least one reliable source "
                            "beyond the patient interview.",
                            "<b>Transition of care</b> — admission, transfer between "
                            "levels of care or services, and discharge.",
                            "<b>Discrepancy</b> — any unexplained difference between "
                            "the medication history and current orders.",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy and Procedure",
                [
                    Para(
                        "A medication history is obtained and reconciled at "
                        "admission, at every transfer, and at discharge. The patient "
                        "or family receives a written, reconciled medication list at "
                        "discharge with instructions to share it with their next "
                        "providers."
                    ),
                    Steps(
                        [
                            "Collect a BPMH using the patient/family plus at least "
                            "one additional source (pharmacy fill history, prior "
                            "records, or provider).",
                            "Document name, dose, route, frequency, and last dose for "
                            "each medication, including OTCs, supplements, and "
                            "inhalers.",
                            "Compare the history against admission/transfer orders "
                            "and resolve every discrepancy with the prescriber.",
                            "At discharge, reconcile home, hospital, and new "
                            "medications into a single list and explain changes to "
                            "the patient.",
                            "Provide the reconciled list to the patient and the "
                            "next provider of care.",
                        ]
                    ),
                    Note(
                        "Every unexplained discrepancy identified during "
                        "reconciliation must be resolved with the prescriber before "
                        "the next medication pass; a high-alert medication "
                        "discrepancy must be escalated to the prescriber immediately "
                        "rather than carried forward."
                    ),
                ],
            ),
            Section(
                "Reconciliation Points and Required Actions",
                [
                    TableBlock(
                        headers=["Transition", "Required action"],
                        rows=[
                            [
                                "Admission",
                                "Obtain BPMH; reconcile against admission orders "
                                "within 24 hours.",
                            ],
                            [
                                "Transfer",
                                "Re-reconcile when level of care or service changes.",
                            ],
                            [
                                "Discharge",
                                "Produce one reconciled list; counsel patient; send "
                                "to next provider.",
                            ],
                            [
                                "High-alert meds",
                                "Resolve any discrepancy with the prescriber "
                                "immediately.",
                            ],
                        ],
                        col_widths=[1.5 * inch, 4.3 * inch],
                    ),
                ],
            ),
            Section(
                "Severity &amp; Reporting",
                [
                    Para(
                        "Classify reconciliation failures on the POL-RM-013 scale and "
                        "grade resulting errors by the NCC MERP index per POL-PS-003."
                    ),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "Omitted anticoagulant at discharge contributing to "
                                "fatal thrombosis.",
                                "Provider, Nursing Supervisor &amp; Risk Mgmt within "
                                "1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Duplicate therapy or omitted critical drug causing "
                                "harm needing intervention.",
                                "Provider &amp; Risk Mgmt within 4 hours.",
                            ],
                            [
                                "SEV-3 / Near Miss",
                                "Discrepancy reaching patient without harm; omission "
                                "caught at pharmacist review.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[1.2 * inch, 2.9 * inch, 1.7 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Sources used to build the BPMH and who obtained it.",
                            "Full medication list with dose, route, frequency, and "
                            "last dose.",
                            "Each discrepancy identified, its resolution, and "
                            "prescriber contacted.",
                            "Discharge reconciled list given to the patient and sent "
                            "to the next provider.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission NPSG.03.06.01 — Maintain and "
                            "communicate accurate patient medication information.",
                            "CMS Conditions of Participation, 42 CFR 482.25 "
                            "(pharmaceutical services).",
                            "ISMP guidance on medication reconciliation.",
                            "Related: POL-RM-013 (severity &amp; reporting); "
                            "POL-PS-003 (medication-error reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_diversion() -> PolicyDoc:
    """Prevention, detection, and response for controlled-substance diversion."""
    return PolicyDoc(
        number="POL-PH-035",
        title="Controlled Substance Diversion Prevention",
        owner="Pharmacy / Compliance",
        effective="2023-09-15",
        revised="2026-02-14",
        review="2028-02-14",
        version="2.4",
        approved_by=_APPROVER,
        applies_to="All staff with access to controlled substances, including "
        "prescribers, pharmacists, nurses, and pharmacy technicians",
        keywords=[
            "controlled substance",
            "diversion",
            "dea",
            "opioids",
            "waste",
            "automated dispensing cabinet",
            "chain of custody",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To prevent, detect, and respond to the diversion of "
                        "controlled substances through access controls, "
                        "reconciliation, witnessed waste, and surveillance, in "
                        "compliance with the federal Controlled Substances Act and "
                        "DEA regulations at 21 CFR Part 1300 and following."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Diversion</b> — the transfer of a controlled "
                            "substance from a lawful to an unlawful channel of "
                            "distribution or use.",
                            "<b>Chain of custody</b> — the documented, unbroken "
                            "trail of accountability for a controlled substance from "
                            "receipt to administration, waste, or return.",
                            "<b>Witnessed waste</b> — disposal of an unused "
                            "controlled-substance portion verified in real time by a "
                            "second authorized witness.",
                            "<b>ADC</b> — automated dispensing cabinet providing "
                            "controlled, auditable access to medications.",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy and Procedure",
                [
                    Para(
                        "Controlled substances are secured, inventoried, and "
                        "reconciled per DEA requirements. Access is limited to "
                        "authorized staff with unique credentials; biometric or "
                        "individual login is required at every ADC transaction. "
                        "Discrepancies are investigated and resolved before the end "
                        "of shift."
                    ),
                    Steps(
                        [
                            "Access controlled substances only under your own unique "
                            "credential for a specific patient and order.",
                            "Reconcile counts at each handoff and resolve any "
                            "discrepancy before leaving the unit.",
                            "Waste any unused portion immediately with a real-time "
                            "authorized witness and document both names.",
                            "Return unused or recovered doses to Pharmacy through the "
                            "approved return process; never pocket or discard "
                            "unwitnessed.",
                            "Run and review ADC transaction and anomaly reports on "
                            "the required cadence.",
                        ]
                    ),
                    Note(
                        "Suspected diversion or a controlled-substance count "
                        "discrepancy that cannot be reconciled must be reported to "
                        "the Pharmacy Diversion Officer and the supervisor "
                        "immediately. Do not confront the suspected individual; "
                        "preserve all records and secure the medication and "
                        "equipment involved."
                    ),
                ],
            ),
            Section(
                "Red Flags and Required Response",
                [
                    TableBlock(
                        headers=["Indicator", "Response"],
                        rows=[
                            [
                                "Unreconciled count discrepancy",
                                "Investigate before end of shift; escalate if "
                                "unresolved.",
                            ],
                            [
                                "Excessive waste or unwitnessed waste",
                                "Review transactions; interview; refer to Diversion "
                                "Officer.",
                            ],
                            [
                                "Removals without a matching order",
                                "Audit ADC logs; compare to MAR; secure records.",
                            ],
                            [
                                "Tampered packaging or substituted product",
                                "Quarantine product; notify Pharmacy and Security "
                                "immediately.",
                            ],
                        ],
                        col_widths=[2.6 * inch, 3.2 * inch],
                    ),
                ],
            ),
            Section(
                "Severity &amp; Escalation",
                [
                    Para(
                        "Classify diversion events on the POL-RM-013 scale. "
                        "Confirmed diversion carries mandatory external reporting to "
                        "the DEA (via DEA Form 106 for significant loss or theft) and "
                        "the state board as required."
                    ),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "Confirmed diversion causing patient harm or "
                                "substituted/diluted patient doses.",
                                "Diversion Officer, Nursing Supervisor &amp; Risk "
                                "Mgmt within 1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Confirmed diversion without patient harm; "
                                "significant unresolved loss.",
                                "Diversion Officer &amp; Compliance within 4 hours.",
                            ],
                            [
                                "SEV-3 / Near Miss",
                                "Reconciled discrepancy or policy lapse with no "
                                "diversion confirmed.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[1.2 * inch, 2.9 * inch, 1.7 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Drug, strength, quantity, and the complete chain of "
                            "custody from removal to administration/waste.",
                            "Witness name and time for every waste event.",
                            "Count discrepancies, investigation steps, and "
                            "resolution.",
                            "Any external report filed (DEA Form 106, state board) "
                            "with date and reference number.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "Controlled Substances Act; DEA regulations at 21 CFR "
                            "Part 1300 et seq. (security, recordkeeping, disposal).",
                            "DEA Form 106 — Report of Theft or Loss of Controlled "
                            "Substances.",
                            "CMS Conditions of Participation, 42 CFR 482.25 "
                            "(pharmaceutical services).",
                            "Related: POL-RM-013 (severity &amp; reporting); "
                            "POL-PS-003 (medication-error reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_adr() -> PolicyDoc:
    """Detection, treatment, and reporting of adverse drug reactions."""
    return PolicyDoc(
        number="POL-PH-036",
        title="Adverse Drug Reaction Reporting",
        owner="Pharmacy / Patient Safety",
        effective="2023-10-01",
        revised="2026-03-20",
        review="2028-03-20",
        version="2.1",
        approved_by=_APPROVER,
        applies_to="All prescribers, pharmacists, and nurses who observe, treat, or "
        "document suspected adverse drug reactions",
        keywords=[
            "adverse drug reaction",
            "adr",
            "medwatch",
            "anaphylaxis",
            "pharmacovigilance",
            "allergy",
            "fda",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To standardize recognition, immediate treatment, "
                        "documentation, and reporting of adverse drug reactions "
                        "(ADRs), including internal surveillance and external "
                        "reporting to the FDA MedWatch program, per CMS "
                        "pharmaceutical-services requirements."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Adverse drug reaction (ADR)</b> — a noxious and "
                            "unintended response to a medication used at normal doses "
                            "(distinct from a preventable medication error).",
                            "<b>Serious ADR</b> — an outcome that is fatal, "
                            "life-threatening, results in or prolongs "
                            "hospitalization, causes disability, or requires "
                            "intervention to prevent permanent harm.",
                            "<b>Anaphylaxis</b> — a severe, rapid-onset, potentially "
                            "fatal systemic hypersensitivity reaction.",
                            "<b>MedWatch</b> — the FDA program for reporting adverse "
                            "events and product problems.",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy and Procedure",
                [
                    Para(
                        "All suspected ADRs are treated clinically, documented in the "
                        "record (including updating the allergy/intolerance list), "
                        "and reported to Pharmacy for assessment and "
                        "pharmacovigilance. Serious and unexpected reactions are "
                        "reported externally to FDA MedWatch (and to the "
                        "manufacturer where applicable)."
                    ),
                    Steps(
                        [
                            "Stop the suspected medication and provide clinically "
                            "indicated treatment.",
                            "Notify the prescriber and obtain orders for ongoing "
                            "management.",
                            "Update the allergy/intolerance list with the reaction "
                            "type and severity.",
                            "File an ADR report to Pharmacy; assess causality and "
                            "preventability.",
                            "Submit serious or unexpected reactions to FDA MedWatch "
                            "per the facility process.",
                        ]
                    ),
                    Note(
                        "For suspected anaphylaxis, stop the drug and give "
                        "intramuscular epinephrine without delay, call for emergency "
                        "assistance, and support the airway and circulation. Do not "
                        "wait for a provider order to administer epinephrine under "
                        "the approved anaphylaxis protocol."
                    ),
                ],
            ),
            Section(
                "ADR Severity and External Reporting",
                [
                    TableBlock(
                        headers=["ADR type", "Example", "External reporting"],
                        rows=[
                            [
                                "Life-threatening",
                                "Anaphylaxis; Stevens-Johnson syndrome.",
                                "FDA MedWatch; manufacturer.",
                            ],
                            [
                                "Serious",
                                "Reaction prolonging stay or needing intervention.",
                                "FDA MedWatch.",
                            ],
                            [
                                "Non-serious",
                                "Mild self-limited rash; transient nausea.",
                                "Internal pharmacovigilance log.",
                            ],
                        ],
                        col_widths=[1.4 * inch, 2.7 * inch, 1.7 * inch],
                    ),
                ],
            ),
            Section(
                "Severity &amp; Reporting",
                [
                    Para(
                        "Classify ADRs on the POL-RM-013 scale. Because an ADR at "
                        "normal doses is generally not a preventable error, the NCC "
                        "MERP index in POL-PS-003 applies only when a medication "
                        "error contributed to the reaction."
                    ),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "Fatal or life-threatening reaction (anaphylaxis, "
                                "SJS/TEN).",
                                "Provider, Nursing Supervisor &amp; Risk Mgmt within "
                                "1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Reaction requiring intervention or prolonging "
                                "hospitalization.",
                                "Provider &amp; Risk Mgmt within 4 hours.",
                            ],
                            [
                                "SEV-3 / Near Miss",
                                "Mild, self-limited reaction; reaction averted by "
                                "allergy-alert interception.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[1.2 * inch, 2.9 * inch, 1.7 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Suspected medication, dose, and route, and the reaction "
                            "onset and description.",
                            "Treatment given and the patient&rsquo;s response.",
                            "Updated allergy/intolerance list entry with severity.",
                            "Causality/preventability assessment and any MedWatch "
                            "submission reference.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "FDA MedWatch — The FDA Safety Information and Adverse "
                            "Event Reporting Program.",
                            "CMS Conditions of Participation, 42 CFR 482.25 "
                            "(pharmaceutical services, ADR reporting).",
                            "ISMP and pharmacovigilance best-practice guidance.",
                            "Related: POL-RM-013 (severity &amp; reporting); "
                            "POL-PS-003 (medication-error reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_sedation() -> PolicyDoc:
    """Safe administration of moderate (procedural) sedation per ASA/TJC."""
    return PolicyDoc(
        number="POL-PH-037",
        title="Moderate (Procedural) Sedation",
        owner="Anesthesia / Medical Staff",
        effective="2024-02-01",
        revised="2026-03-28",
        review="2028-03-28",
        version="2.0",
        approved_by=_APPROVER,
        applies_to="All credentialed providers and nurses administering or "
        "monitoring moderate sedation outside the operating room",
        keywords=[
            "moderate sedation",
            "procedural sedation",
            "conscious sedation",
            "asa",
            "rescue",
            "capnography",
            "reversal",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To ensure safe patient selection, monitoring, and rescue "
                        "during moderate (procedural) sedation, consistent with the "
                        "American Society of Anesthesiologists (ASA) continuum of "
                        "depth of sedation and The Joint Commission "
                        "moderate-sedation standards."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to moderate sedation administered outside the "
                        "operating room by credentialed non-anesthesiologist "
                        "providers. It does not govern minimal sedation (anxiolysis) "
                        "or deep sedation/general anesthesia, which require "
                        "anesthesia privileging."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Moderate sedation (&ldquo;conscious "
                            "sedation&rdquo;)</b> — drug-induced depression of "
                            "consciousness in which the patient responds purposefully "
                            "to verbal commands, alone or with light tactile "
                            "stimulation.",
                            "<b>Rescue</b> — the ability to recognize and manage a "
                            "level of sedation deeper than intended; providers must be "
                            "able to rescue a patient from the next deeper level.",
                            "<b>Capnography</b> — continuous monitoring of exhaled "
                            "carbon dioxide to detect hypoventilation and apnea.",
                            "<b>ASA Physical Status</b> — the ASA I&ndash;VI "
                            "classification used to assess pre-procedure risk.",
                        ]
                    ),
                ],
            ),
            Section(
                "Policy and Procedure",
                [
                    Para(
                        "A pre-sedation assessment (history, airway evaluation, ASA "
                        "physical status, and NPO status) is completed and documented "
                        "before sedation. A qualified individual whose sole "
                        "responsibility is monitoring the patient must be present "
                        "throughout; the provider performing the procedure does not "
                        "also serve as the monitor."
                    ),
                    Steps(
                        [
                            "Complete and document the pre-sedation assessment, "
                            "airway exam, ASA status, and NPO verification.",
                            "Confirm emergency equipment, suction, oxygen, reversal "
                            "agents, and resuscitation support are immediately "
                            "available.",
                            "Monitor oxygenation (pulse oximetry), ventilation "
                            "(capnography), level of consciousness, blood pressure, "
                            "and heart rate continuously.",
                            "Titrate sedatives/analgesics to the lightest effective "
                            "depth, reassessing after each increment.",
                            "Recover the patient to defined discharge criteria before "
                            "release.",
                        ]
                    ),
                    Note(
                        "If a patient progresses to a deeper level of sedation than "
                        "intended (unresponsive to verbal/tactile stimulation, airway "
                        "compromise, or apnea), stop sedation, support the airway and "
                        "ventilation immediately, call for anesthesia/code "
                        "assistance, and administer reversal agents per protocol. The "
                        "team must be able to rescue from deep sedation."
                    ),
                ],
            ),
            Section(
                "Sedation Continuum and Reversal Agents",
                [
                    TableBlock(
                        headers=["Level", "Responsiveness", "Airway"],
                        rows=[
                            [
                                "Minimal (anxiolysis)",
                                "Normal response to verbal stimuli.",
                                "Unaffected.",
                            ],
                            [
                                "Moderate (target)",
                                "Purposeful to verbal / light tactile.",
                                "No intervention; adequate ventilation.",
                            ],
                            [
                                "Deep",
                                "Purposeful after repeated or painful stimulation.",
                                "May need intervention.",
                            ],
                            [
                                "General anesthesia",
                                "Not arousable, even with pain.",
                                "Often requires intervention.",
                            ],
                        ],
                        col_widths=[1.5 * inch, 2.6 * inch, 1.7 * inch],
                        row_shades=[None, _SEV3, _SEV2, _SEV1],
                    ),
                    Para(
                        "Reversal agents must be immediately available: "
                        "<b>naloxone</b> for opioid-induced respiratory depression "
                        "and <b>flumazenil</b> for benzodiazepine over-sedation."
                    ),
                ],
            ),
            Section(
                "Severity &amp; Escalation",
                [
                    Para(
                        "Classify sedation events on the POL-RM-013 scale; when a "
                        "medication error contributes, grade it by the NCC MERP index "
                        "per POL-PS-003."
                    ),
                    TableBlock(
                        headers=["Severity", "Example", "Notify / timeframe"],
                        rows=[
                            [
                                "SEV-1",
                                "Respiratory arrest, unplanned intubation, or death "
                                "during sedation.",
                                "Provider, Nursing Supervisor &amp; Risk Mgmt within "
                                "1 hour.",
                            ],
                            [
                                "SEV-2",
                                "Oversedation requiring reversal, bag-mask "
                                "ventilation, or prolonged recovery.",
                                "Provider &amp; Risk Mgmt within 4 hours.",
                            ],
                            [
                                "SEV-3 / Near Miss",
                                "Transient desaturation self-corrected; monitoring "
                                "lapse caught with no harm.",
                                "Event report within 24 hours.",
                            ],
                        ],
                        col_widths=[1.2 * inch, 2.9 * inch, 1.7 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Pre-sedation assessment, airway exam, ASA physical "
                            "status, and NPO verification.",
                            "Medications, doses, and times, and the monitoring "
                            "individual&rsquo;s name.",
                            "Continuous vitals, oxygenation, and capnography at "
                            "defined intervals.",
                            "Any reversal agent given and the patient&rsquo;s "
                            "response.",
                            "Recovery scoring and that discharge criteria were met.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "ASA Continuum of Depth of Sedation: Definition of "
                            "General Anesthesia and Levels of Sedation/Analgesia.",
                            "ASA Practice Guidelines for Moderate "
                            "Procedural Sedation and Analgesia.",
                            "The Joint Commission moderate-sedation standards "
                            "(Provision of Care).",
                            "CMS Conditions of Participation, 42 CFR 482.52 "
                            "(anesthesia services).",
                            "Related: POL-RM-013 (severity &amp; reporting); "
                            "POL-PS-003 (medication-error reporting).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_batch() -> list[PolicyDoc]:
    """Return this batch's policies, in listed order."""
    return [
        build_anticoagulation(),
        build_insulin(),
        build_high_alert(),
        build_lasa(),
        build_med_rec(),
        build_diversion(),
        build_adr(),
        build_sedation(),
    ]
