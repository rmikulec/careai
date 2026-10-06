"""Safety-domain policy batch for the hospital policy corpus generator.

This module holds seven fictional-facility safety policies (POL-SAF-070 through
POL-SAF-076) covering diagnostic/interventional radiation safety, MRI safety,
laser safety, medical-device malfunction and FDA reporting, employee
tuberculosis screening and respiratory protection, healthcare-personnel
influenza vaccination, and fitness-for-duty / impaired-practitioner handling.
Each policy is anchored to the governing real-world standard (NRC 10 CFR 20/35,
ACR MRI zones, ANSI Z136.3/AORN, FDA 21 CFR 803, CDC/OSHA, CMS/CDC), reuses the
facility-wide SEV-1/SEV-2/SEV-3/Near Miss scale from POL-RM-013, and states
concrete, time-bound notification deadlines so the Incident Reporting Agent has
realistic material to retrieve, cite, and ground severity decisions against.
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


def build_radiation_safety() -> PolicyDoc:
    """Diagnostic and interventional radiation safety (NRC 10 CFR 20/35)."""
    return PolicyDoc(
        number="POL-SAF-070",
        title="Radiation Safety (Diagnostic and Interventional)",
        owner="Radiation Safety / Radiology",
        effective="2023-09-01",
        revised="2026-03-12",
        review="2028-03-12",
        version="3.1",
        approved_by="Radiation Safety Committee",
        applies_to="All personnel who operate, assist with, or work near "
        "ionizing-radiation sources, including radiology, interventional "
        "radiology, cardiac cath lab, nuclear medicine, and operating-room staff",
        keywords=[
            "radiation safety",
            "alara",
            "dose limit",
            "dosimeter",
            "fluoroscopy",
            "radioactive material",
            "radiation safety officer",
            "declared pregnant worker",
        ],
        sections=[
            Section(
                "Purpose and Scope",
                [
                    Para(
                        "This policy establishes the facility radiation-protection "
                        "program for all sources of ionizing radiation at Riverside "
                        "Regional Medical Center, consistent with the "
                        "<b>as-low-as-reasonably-achievable (ALARA)</b> principle. "
                        "It applies to diagnostic x-ray, fluoroscopy, interventional "
                        "procedures, and byproduct material used under the facility "
                        "radioactive-materials license."
                    ),
                    Para(
                        "The program is administered by the <b>Radiation Safety "
                        "Officer (RSO)</b> under the oversight of the Radiation "
                        "Safety Committee and conforms to U.S. Nuclear Regulatory "
                        "Commission standards for protection against radiation "
                        "(10 CFR Part 20) and for the medical use of byproduct "
                        "material (10 CFR Part 35), as adopted by the State "
                        "radiation-control program."
                    ),
                ],
            ),
            Section(
                "Occupational Dose Limits",
                [
                    Para(
                        "Occupational exposures shall be kept ALARA and shall not "
                        "exceed the annual limits below (10 CFR 20.1201, 20.1207, "
                        "20.1208). Facility investigation levels are set at a "
                        "fraction of the regulatory limit to prompt review before a "
                        "limit is approached."
                    ),
                    TableBlock(
                        headers=[
                            "Exposure category",
                            "Annual limit",
                            "Facility action level",
                        ],
                        rows=[
                            [
                                "Total effective dose equivalent (whole body)",
                                "5 rem (50 mSv)",
                                "1.25 rem / quarter",
                            ],
                            [
                                "Lens of the eye",
                                "15 rem (150 mSv)",
                                "3.75 rem / quarter",
                            ],
                            [
                                "Skin / any extremity",
                                "50 rem (500 mSv)",
                                "12.5 rem / quarter",
                            ],
                            [
                                "Minor (under 18)",
                                "10% of adult limits",
                                "Any measurable reading reviewed",
                            ],
                            [
                                "Declared pregnant worker (gestation)",
                                "0.5 rem (5 mSv) to embryo/fetus",
                                "0.05 rem / month",
                            ],
                        ],
                        col_widths=[2.6 * inch, 1.7 * inch, 1.5 * inch],
                    ),
                    Para(
                        "A worker may <b>declare a pregnancy in writing</b> to the "
                        "RSO to invoke the embryo/fetus limit; the declaration may "
                        "be withdrawn at any time in writing."
                    ),
                ],
            ),
            Section(
                "Dosimetry and ALARA Controls",
                [
                    Bullets(
                        items=[
                            "Personnel likely to receive &gt;10% of an annual limit "
                            "are issued dosimeters; collar badges are worn outside "
                            "the apron at the collar, with a second under-apron badge "
                            "for declared pregnant workers.",
                            "Dosimeters are exchanged and read monthly; results are "
                            "reviewed by the RSO against facility action levels.",
                            "Apply time, distance, and shielding: minimize beam-on "
                            "time, maximize distance from the source, and use lead "
                            "aprons, thyroid shields, and ceiling-suspended shields.",
                            "Fluoroscopy operators are credentialed and monitor "
                            "cumulative air-kerma and fluoroscopy time; prolonged "
                            "procedures trigger a substantial-radiation-dose review.",
                            "Radioactive materials are secured, labeled, surveyed, "
                            "and disposed of per the license and 10 CFR 35.",
                        ]
                    ),
                ],
            ),
            Section(
                "Overexposure and Patient Dose Events",
                [
                    Para(
                        "A suspected overexposure, lost or contaminated source, or "
                        "unintended high patient dose must be reported immediately "
                        "to the RSO, who determines regulatory reportability "
                        "(e.g., a 10 CFR 35.3045 medical event) and State "
                        "radiation-control notification obligations."
                    ),
                    Note(
                        "If a dosimeter reading or clinical finding suggests an "
                        "overexposure or a lost/unsecured radioactive source, "
                        "<b>stop the activity, secure the area, and call the "
                        "Radiation Safety Officer immediately (24/7 pager via "
                        "operator)</b>. Do not resume use until the RSO clears the "
                        "area."
                    ),
                ],
            ),
            Section(
                "Severity &amp; Reporting",
                [
                    Para(
                        "Classify and notify per the facility-wide severity scale in "
                        "<b>POL-RM-013</b>. A radioactive-source exposure causing "
                        "serious injury or a reportable medical event with major "
                        "patient harm is a <b>SEV-1</b>; a significant protocol "
                        "deviation or action-level exceedance without serious harm "
                        "is a <b>SEV-2</b>; a minor variance or a Near Miss is "
                        "<b>SEV-3 / Near Miss</b>."
                    ),
                    TableBlock(
                        headers=["Severity", "Notify", "Deadline"],
                        rows=[
                            [
                                "SEV-1 (catastrophic / sentinel)",
                                "RSO, Risk Management, administrator on call",
                                "Within 1 hour",
                            ],
                            [
                                "SEV-2 (major)",
                                "RSO and department manager",
                                "Within 4 hours",
                            ],
                            [
                                "SEV-3 / Near Miss (minor)",
                                "RSO via electronic event report",
                                "Within 24 hours",
                            ],
                        ],
                        col_widths=[2.0 * inch, 2.3 * inch, 1.5 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                    Para(
                        "The RSO reports regulatory events to the State "
                        "radiation-control program and NRC as required; staff-injury "
                        "aspects are cross-referenced to the bloodborne/exposure "
                        "policy <b>POL-EH-001</b> where applicable."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        items=[
                            "10 CFR Part 20 &mdash; Standards for Protection Against "
                            "Radiation (NRC).",
                            "10 CFR Part 35 &mdash; Medical Use of Byproduct Material "
                            "(NRC), including 35.3045 medical-event reporting.",
                            "State radiation-control program regulations and the "
                            "facility radioactive-materials license.",
                            "POL-RM-013 &mdash; Incident Reporting and Event Severity "
                            "Classification.",
                            "POL-EH-001 &mdash; Bloodborne Pathogen Exposure and "
                            "Needlestick.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_mri_safety() -> PolicyDoc:
    """MRI safety program with ACR zones I-IV and MR labeling."""
    return PolicyDoc(
        number="POL-SAF-071",
        title="Magnetic Resonance Imaging (MRI) Safety",
        owner="Radiology / Safety",
        effective="2023-11-01",
        revised="2026-04-08",
        review="2028-04-08",
        version="2.3",
        approved_by="Radiation Safety Committee",
        applies_to="All staff, providers, patients, visitors, contractors, and "
        "emergency responders entering or working in the MRI suite",
        keywords=[
            "mri safety",
            "acr zones",
            "mr conditional",
            "ferromagnetic",
            "projectile",
            "quench",
            "screening",
            "static magnetic field",
        ],
        sections=[
            Section(
                "Purpose and Scope",
                [
                    Para(
                        "This policy establishes a four-zone access-control and "
                        "screening program for the MRI environment to prevent "
                        "ferromagnetic-projectile, burn, implant, acoustic, and "
                        "cryogen-quench hazards. It follows the American College of "
                        "Radiology (ACR) Manual on MR Safety and applies to the "
                        "entire MRI suite at all times &mdash; the static magnetic "
                        "field is <b>always on</b>, even when no scan is in progress."
                    ),
                    Para(
                        "The program is led by the <b>MR Medical Director</b> and the "
                        "<b>MR Safety Officer (MRSO)</b>, supported by MR Safety "
                        "Experts, with authority to restrict access."
                    ),
                ],
            ),
            Section(
                "ACR Safety Zones",
                [
                    Para(
                        "Access is controlled across four zones of increasing field "
                        "strength and restriction. No one enters Zone III or IV "
                        "without completing MR screening."
                    ),
                    TableBlock(
                        headers=["Zone", "Area", "Access"],
                        rows=[
                            [
                                "Zone I",
                                "General public areas outside the MR department",
                                "Open; no screening required",
                            ],
                            [
                                "Zone II",
                                "Reception, changing, and initial screening "
                                "interface between public and controlled space",
                                "Patients under staff supervision",
                            ],
                            [
                                "Zone III",
                                "Controlled area around the console/magnet, where "
                                "unscreened ferromagnetic items are dangerous",
                                "Screened, MR-trained personnel only",
                            ],
                            [
                                "Zone IV",
                                "The magnet (scanner) room itself",
                                "Screened persons under direct MR-staff supervision",
                            ],
                        ],
                        col_widths=[0.7 * inch, 3.1 * inch, 2.0 * inch],
                    ),
                    Note(
                        "<b>No ferromagnetic item may cross into Zone IV.</b> Oxygen "
                        "cylinders, IV poles, wheelchairs, tools, and pens must be "
                        "MR-conditional or MR-safe and screened. A ferromagnetic "
                        "object becomes a lethal projectile near the bore."
                    ),
                ],
            ),
            Section(
                "Device and Implant Labeling",
                [
                    Para(
                        "Every device, implant, and item brought near the magnet must "
                        "carry a known MR classification before entry:"
                    ),
                    Bullets(
                        items=[
                            "<b>MR Safe</b> &mdash; poses no known hazard in any MR "
                            "environment (non-conducting, non-metallic, "
                            "non-magnetic).",
                            "<b>MR Conditional</b> &mdash; safe only within the "
                            "specified conditions (field strength, gradient, and "
                            "RF limits) documented by the manufacturer.",
                            "<b>MR Unsafe</b> &mdash; poses an unacceptable hazard and "
                            "is prohibited from Zone IV.",
                            "Implant eligibility is verified against manufacturer MR "
                            "conditions and documented by the MRSO/radiologist "
                            "before scanning.",
                        ]
                    ),
                ],
            ),
            Section(
                "Screening and Emergency Response",
                [
                    Steps(
                        items=[
                            "Complete a written MR screening form for every patient "
                            "and any person entering Zone III/IV; reconcile metal "
                            "implants, devices, and prior injuries.",
                            "Perform a verbal re-check and ferromagnetic detection at "
                            "the Zone III/IV threshold.",
                            "Remove external ferromagnetic items and use only "
                            "MR-conditional ancillary equipment inside Zone IV.",
                            "For cardiac arrest, remove the patient from Zone IV "
                            "before resuscitation; code teams do not bring "
                            "ferromagnetic equipment into the magnet room.",
                            "For a cryogen quench (oxygen-displacement and frostbite "
                            "risk), evacuate the room, do not re-enter until cleared, "
                            "and press the magnet-rundown/quench button only when a "
                            "projectile traps a patient against the bore.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity &amp; Reporting",
                [
                    Para(
                        "Classify and notify per <b>POL-RM-013</b>. A ferromagnetic "
                        "projectile event causing serious injury, or an "
                        "unintended quench with patient/staff harm, is a "
                        "<b>SEV-1</b>; a projectile event or burn without serious "
                        "injury is a <b>SEV-2</b>; a screening breach with no harm is "
                        "a <b>SEV-3 / Near Miss</b>."
                    ),
                    TableBlock(
                        headers=["Severity", "Notify", "Deadline"],
                        rows=[
                            [
                                "SEV-1 (catastrophic / sentinel)",
                                "MR Medical Director, MRSO, Risk Management, "
                                "administrator on call",
                                "Within 1 hour",
                            ],
                            [
                                "SEV-2 (major)",
                                "MRSO and Radiology manager",
                                "Within 4 hours",
                            ],
                            [
                                "SEV-3 / Near Miss (minor)",
                                "MRSO via electronic event report",
                                "Within 24 hours",
                            ],
                        ],
                        col_widths=[2.0 * inch, 2.3 * inch, 1.5 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                    Para(
                        "If a projectile involved a medical device, also follow the "
                        "device-reporting policy <b>POL-SAF-073</b>; staff injuries "
                        "are cross-referenced to <b>POL-EH-001</b>."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        items=[
                            "ACR Manual on MR Safety &mdash; zones I&ndash;IV and "
                            "MR Safe / MR Conditional / MR Unsafe labeling.",
                            "POL-RM-013 &mdash; Incident Reporting and Event Severity "
                            "Classification.",
                            "POL-SAF-073 &mdash; Medical Device Malfunction, Recall, "
                            "and FDA Reporting.",
                            "POL-EH-001 &mdash; Bloodborne Pathogen Exposure and "
                            "Needlestick.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_laser_safety() -> PolicyDoc:
    """Health-care laser safety (ANSI Z136.3, AORN)."""
    return PolicyDoc(
        number="POL-SAF-072",
        title="Laser Safety",
        owner="Perioperative Services / Safety",
        effective="2023-10-15",
        revised="2026-02-20",
        review="2028-02-20",
        version="2.1",
        approved_by="Environment of Care Committee",
        applies_to="All personnel who operate, assist with, or are present during "
        "the use of surgical and therapeutic lasers in the OR, procedure rooms, "
        "and clinics",
        keywords=[
            "laser safety",
            "ansi z136.3",
            "laser safety officer",
            "eyewear",
            "nominal hazard zone",
            "laser plume",
            "fire safety",
            "class 4 laser",
        ],
        sections=[
            Section(
                "Purpose and Scope",
                [
                    Para(
                        "This policy governs the safe use of Class 3B and Class 4 "
                        "health-care lasers to prevent eye and skin injury, airway "
                        "and surgical fires, and plume-inhalation hazards. It "
                        "follows <b>ANSI Z136.3</b> (Safe Use of Lasers in Health "
                        "Care) and AORN perioperative guidance."
                    ),
                    Para(
                        "A designated <b>Laser Safety Officer (LSO)</b> administers "
                        "the program, approves operators, and defines the "
                        "<b>Nominal Hazard Zone (NHZ)</b> for each device."
                    ),
                ],
            ),
            Section(
                "Controls and Protective Measures",
                [
                    Bullets(
                        items=[
                            "Wavelength-specific protective eyewear with the correct "
                            "optical density is worn by everyone in the NHZ; the "
                            "patient&rsquo;s eyes are protected per wavelength.",
                            "Controlled-access signage and a lit warning sign are "
                            "posted at every entrance to the NHZ; windows are "
                            "covered when required.",
                            "The laser is kept in <b>STANDBY</b> except during active "
                            "firing; only the operator activates emission, on the "
                            "surgeon&rsquo;s command.",
                            "A smoke-evacuation system captures surgical plume at the "
                            "source; high-filtration respiratory protection is used "
                            "where indicated.",
                            "Fire-risk controls apply during airway and head/neck "
                            "cases: minimize supplemental oxygen, use "
                            "laser-resistant endotracheal tubes, and keep saline and "
                            "wet sponges available.",
                        ]
                    ),
                    Note(
                        "<b>If a surgical or airway fire ignites, STOP gas flow and "
                        "the laser, remove burning material, and extinguish "
                        "immediately</b> (for an airway fire, remove the tube and "
                        "disconnect oxygen). Then treat the patient and activate the "
                        "fire response."
                    ),
                ],
            ),
            Section(
                "Operation and Credentialing",
                [
                    Steps(
                        items=[
                            "Verify operator credentialing and device-specific "
                            "training before the case.",
                            "Complete a pre-use safety time-out: confirm eyewear, "
                            "signage, NHZ boundaries, plume evacuation, and fire "
                            "precautions.",
                            "Test-fire the laser into an appropriate target, confirm "
                            "settings, and keep it in STANDBY between activations.",
                            "Account for all protective measures at case end and "
                            "document laser use in the operative record.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity &amp; Reporting",
                [
                    Para(
                        "Classify and notify per <b>POL-RM-013</b>. A surgical or "
                        "airway fire causing serious injury, or a laser eye injury, "
                        "is a <b>SEV-1</b>; a minor burn or an unintended tissue "
                        "injury without serious harm is a <b>SEV-2</b>; a control "
                        "lapse without injury is a <b>SEV-3 / Near Miss</b>."
                    ),
                    TableBlock(
                        headers=["Severity", "Notify", "Deadline"],
                        rows=[
                            [
                                "SEV-1 (catastrophic / sentinel)",
                                "LSO, OR charge, Risk Management, administrator "
                                "on call",
                                "Within 1 hour",
                            ],
                            [
                                "SEV-2 (major)",
                                "LSO and perioperative manager",
                                "Within 4 hours",
                            ],
                            [
                                "SEV-3 / Near Miss (minor)",
                                "LSO via electronic event report",
                                "Within 24 hours",
                            ],
                        ],
                        col_widths=[2.0 * inch, 2.3 * inch, 1.5 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                    Para(
                        "If the event involved a laser-device malfunction, also "
                        "follow <b>POL-SAF-073</b>; staff plume or burn exposures are "
                        "cross-referenced to <b>POL-EH-001</b>."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        items=[
                            "ANSI Z136.3 &mdash; Safe Use of Lasers in Health Care.",
                            "AORN Guideline for Laser Safety.",
                            "POL-RM-013 &mdash; Incident Reporting and Event Severity "
                            "Classification.",
                            "POL-SAF-073 &mdash; Medical Device Malfunction, Recall, "
                            "and FDA Reporting.",
                            "POL-EH-001 &mdash; Bloodborne Pathogen Exposure and "
                            "Needlestick.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_device_reporting() -> PolicyDoc:
    """Device malfunction, recall, and FDA MDR reporting (21 CFR 803)."""
    return PolicyDoc(
        number="POL-SAF-073",
        title="Medical Device Malfunction, Recall, and FDA Reporting",
        owner="Clinical Engineering / Risk Management",
        effective="2024-02-01",
        revised="2026-05-04",
        review="2028-05-04",
        version="3.0",
        approved_by="Environment of Care Committee",
        applies_to="All staff and providers who use, maintain, or manage medical "
        "devices, and Clinical Engineering, Supply Chain, and Risk Management",
        keywords=[
            "medical device reporting",
            "mdr",
            "21 cfr 803",
            "device malfunction",
            "recall",
            "safe medical devices act",
            "sequestration",
            "user facility",
        ],
        sections=[
            Section(
                "Purpose and Scope",
                [
                    Para(
                        "This policy defines how Riverside Regional Medical Center, "
                        "as a <b>device user facility</b>, identifies, sequesters, "
                        "investigates, and reports medical-device malfunctions, "
                        "serious injuries, and deaths, and how it manages recalls. "
                        "It implements the Safe Medical Devices Act and FDA Medical "
                        "Device Reporting requirements at <b>21 CFR Part 803</b>."
                    ),
                ],
            ),
            Section(
                "Immediate Actions and Sequestration",
                [
                    Steps(
                        items=[
                            "Ensure patient safety first; if a device is implicated "
                            "in harm, remove it from service.",
                            "<b>Sequester</b> the device and all associated "
                            "accessories, packaging, disposables, and settings &mdash; "
                            "do not alter, clean, reset, or discard them.",
                            "Tag the device &ldquo;Do Not Use &mdash; Quarantine for "
                            "Investigation&rdquo; and notify Clinical Engineering.",
                            "Record device make, model, serial/lot number, and "
                            "settings at the time of the event.",
                            "Notify Risk Management, which determines FDA/manufacturer "
                            "reportability.",
                        ]
                    ),
                    Note(
                        "<b>Do not return, repair, discard, or reset a device "
                        "involved in a death or serious injury.</b> Sequester it "
                        "exactly as found &mdash; it is evidence, and FDA/manufacturer "
                        "reporting deadlines begin the moment the facility becomes "
                        "aware."
                    ),
                ],
            ),
            Section(
                "FDA Reporting Timeframes",
                [
                    Para(
                        "Reports are submitted <b>as soon as practicable</b> and no "
                        "later than the deadlines below, measured from when the "
                        "facility becomes aware of the event (21 CFR 803.30, "
                        "803.32). Deadlines are counted in <b>work days</b>."
                    ),
                    TableBlock(
                        headers=["Event", "Report to", "Deadline"],
                        rows=[
                            [
                                "Device-related death",
                                "FDA (MedWatch 3500A) and manufacturer, if known",
                                "Within 10 work days",
                            ],
                            [
                                "Device-related serious injury",
                                "Manufacturer; FDA if manufacturer unknown",
                                "Within 10 work days",
                            ],
                            [
                                "Annual summary of device reports",
                                "FDA",
                                "By January 1 each year",
                            ],
                        ],
                        col_widths=[1.9 * inch, 2.4 * inch, 1.5 * inch],
                        row_shades=[_SEV1, _SEV2, None],
                    ),
                    Para(
                        "A device <b>malfunction</b> that did not cause death or "
                        "serious injury but could if it recurred is investigated and "
                        "may be reported to the manufacturer; the manufacturer, not "
                        "the user facility, carries the 30-day MDR obligation to FDA."
                    ),
                ],
            ),
            Section(
                "Recall Management",
                [
                    Bullets(
                        items=[
                            "Clinical Engineering and Supply Chain triage FDA and "
                            "manufacturer recall/safety notices on receipt and "
                            "classify urgency (Class I, II, III).",
                            "Affected devices and lots are located, removed from "
                            "service, quarantined, and reconciled against inventory.",
                            "Clinical units are notified of substitutes and interim "
                            "workarounds; completion is documented and tracked to "
                            "closure.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity &amp; Reporting",
                [
                    Para(
                        "Classify and notify per <b>POL-RM-013</b>. A device-related "
                        "death or a malfunction causing serious patient harm is a "
                        "<b>SEV-1</b>; a malfunction with major impact but no serious "
                        "injury is a <b>SEV-2</b>; a minor malfunction or a Near Miss "
                        "is a <b>SEV-3 / Near Miss</b>. Internal severity "
                        "notification is independent of &mdash; and does not replace "
                        "&mdash; the FDA/manufacturer MDR deadlines above."
                    ),
                    TableBlock(
                        headers=["Severity", "Notify", "Deadline"],
                        rows=[
                            [
                                "SEV-1 (catastrophic / sentinel)",
                                "Clinical Engineering, Risk Management, administrator "
                                "on call",
                                "Within 1 hour",
                            ],
                            [
                                "SEV-2 (major)",
                                "Clinical Engineering and department manager",
                                "Within 4 hours",
                            ],
                            [
                                "SEV-3 / Near Miss (minor)",
                                "Clinical Engineering via electronic event report",
                                "Within 24 hours",
                            ],
                        ],
                        col_widths=[2.0 * inch, 2.3 * inch, 1.5 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        items=[
                            "Safe Medical Devices Act of 1990.",
                            "21 CFR Part 803 &mdash; Medical Device Reporting (user "
                            "facility 10-work-day death and serious-injury reports; "
                            "manufacturer 30-day reports).",
                            "POL-RM-013 &mdash; Incident Reporting and Event Severity "
                            "Classification.",
                            "POL-SAF-071 &mdash; Magnetic Resonance Imaging (MRI) "
                            "Safety.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_tb_screening() -> PolicyDoc:
    """Employee TB screening and respiratory protection (CDC, OSHA 1910.134)."""
    return PolicyDoc(
        number="POL-SAF-074",
        title="Employee Tuberculosis Screening and Respiratory Protection",
        owner="Employee Health / Infection Prevention &amp; Control",
        effective="2023-08-01",
        revised="2026-01-22",
        review="2028-01-22",
        version="2.4",
        approved_by="Infection Prevention &amp; Control Committee",
        applies_to="All employees, licensed providers, students, volunteers, and "
        "contractors with potential occupational exposure to Mycobacterium "
        "tuberculosis",
        keywords=[
            "tuberculosis",
            "tb screening",
            "respiratory protection",
            "n95",
            "fit testing",
            "airborne precautions",
            "igra",
            "osha 1910.134",
        ],
        sections=[
            Section(
                "Purpose and Scope",
                [
                    Para(
                        "This policy establishes tuberculosis (TB) screening for "
                        "health-care personnel and the respiratory-protection "
                        "program for airborne-pathogen exposure. It follows current "
                        "CDC recommendations for TB screening, testing, and "
                        "treatment of health-care personnel and the OSHA Respiratory "
                        "Protection standard, <b>29 CFR 1910.134</b>."
                    ),
                ],
            ),
            Section(
                "TB Screening Requirements",
                [
                    Para(
                        "All personnel receive a <b>baseline (preplacement) TB "
                        "screening</b>: a symptom and risk assessment plus a TB test "
                        "(IGRA blood test or two-step tuberculin skin test) unless a "
                        "prior positive is documented. Routine serial testing of "
                        "personnel without known exposure is not recommended absent "
                        "ongoing transmission risk; testing frequency otherwise "
                        "follows the exposure-risk assessment below."
                    ),
                    TableBlock(
                        headers=["Risk category", "Baseline", "After exposure"],
                        rows=[
                            [
                                "No ongoing exposure risk",
                                "Symptom/risk assessment + TB test",
                                "Test on documented exposure only",
                            ],
                            [
                                "Potential / recurring exposure",
                                "Symptom/risk assessment + TB test",
                                "Annual symptom assessment; education",
                            ],
                            [
                                "Documented unprotected exposure",
                                "Not applicable",
                                "Test at baseline and again at 8&ndash;10 weeks",
                            ],
                            [
                                "Prior positive TB test",
                                "Symptom screen; chest imaging as indicated",
                                "Annual symptom screen (no repeat test)",
                            ],
                        ],
                        col_widths=[1.9 * inch, 2.1 * inch, 1.8 * inch],
                    ),
                ],
            ),
            Section(
                "Respiratory Protection",
                [
                    Bullets(
                        items=[
                            "Personnel entering airborne-isolation rooms or caring "
                            "for suspected/confirmed TB patients wear a NIOSH-"
                            "approved N95 or higher respirator.",
                            "Respirator users are <b>medically cleared, fit-tested, "
                            "and trained</b> before use and fit-tested at least "
                            "annually and when facial features change.",
                            "Patients with suspected pulmonary TB are placed in an "
                            "airborne-infection-isolation (negative-pressure) room "
                            "under Airborne Precautions.",
                            "A user seal check is performed each time a respirator is "
                            "donned.",
                        ]
                    ),
                    Note(
                        "<b>After an unprotected exposure to a patient with "
                        "infectious TB, report to Employee Health within 24 hours.</b> "
                        "You will be screened at baseline and retested at "
                        "8&ndash;10 weeks; do not wait for symptoms."
                    ),
                ],
            ),
            Section(
                "Severity &amp; Reporting",
                [
                    Para(
                        "Classify and notify per <b>POL-RM-013</b>. A cluster of "
                        "occupational TB conversions or confirmed nosocomial "
                        "transmission is a <b>SEV-1</b>; a single confirmed "
                        "conversion or a significant respiratory-protection failure "
                        "is a <b>SEV-2</b>; an individual unprotected exposure without "
                        "conversion, or a Near Miss, is a <b>SEV-3 / Near Miss</b>."
                    ),
                    TableBlock(
                        headers=["Severity", "Notify", "Deadline"],
                        rows=[
                            [
                                "SEV-1 (catastrophic / sentinel)",
                                "Employee Health, Infection Prevention, "
                                "administrator on call",
                                "Within 1 hour",
                            ],
                            [
                                "SEV-2 (major)",
                                "Employee Health and Infection Prevention",
                                "Within 4 hours",
                            ],
                            [
                                "SEV-3 / Near Miss (minor)",
                                "Employee Health via electronic event report",
                                "Within 24 hours",
                            ],
                        ],
                        col_widths=[2.0 * inch, 2.3 * inch, 1.5 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                    Para(
                        "Bloodborne or sharps aspects of an exposure are "
                        "cross-referenced to <b>POL-EH-001</b>."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        items=[
                            "CDC recommendations for TB screening, testing, and "
                            "treatment of health-care personnel.",
                            "29 CFR 1910.134 &mdash; OSHA Respiratory Protection "
                            "standard (medical evaluation, fit testing, training).",
                            "POL-RM-013 &mdash; Incident Reporting and Event Severity "
                            "Classification.",
                            "POL-EH-001 &mdash; Bloodborne Pathogen Exposure and "
                            "Needlestick.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_influenza_vaccination() -> PolicyDoc:
    """Healthcare-personnel influenza vaccination (CMS/CDC)."""
    return PolicyDoc(
        number="POL-SAF-075",
        title="Healthcare Personnel Influenza Vaccination",
        owner="Employee Health / Infection Prevention &amp; Control",
        effective="2023-09-15",
        revised="2026-03-01",
        review="2028-03-01",
        version="2.2",
        approved_by="Infection Prevention &amp; Control Committee",
        applies_to="All employees, licensed providers, students, volunteers, and "
        "contractors with patient or patient-environment contact",
        keywords=[
            "influenza vaccination",
            "flu shot",
            "healthcare personnel",
            "declination",
            "masking",
            "cms reporting",
            "nhsn",
            "vaccine exemption",
        ],
        sections=[
            Section(
                "Purpose and Scope",
                [
                    Para(
                        "This policy establishes annual seasonal influenza "
                        "vaccination for health-care personnel to protect patients "
                        "and the workforce. It aligns with CDC recommendations for "
                        "influenza vaccination of health-care personnel and with CMS "
                        "requirements to track and report personnel vaccination "
                        "status through the CDC National Healthcare Safety Network "
                        "(NHSN)."
                    ),
                ],
            ),
            Section(
                "Vaccination Requirement",
                [
                    Bullets(
                        items=[
                            "All in-scope personnel are vaccinated annually during "
                            "the facility influenza campaign (typically "
                            "October&ndash;March) unless an approved exemption "
                            "applies.",
                            "Vaccine is offered on-site at no cost; externally "
                            "obtained vaccine is accepted with documentation.",
                            "Vaccination status is recorded in Employee Health and "
                            "aggregated for CMS/NHSN reporting.",
                        ]
                    ),
                ],
            ),
            Section(
                "Exemptions and Masking",
                [
                    Para(
                        "Personnel may request a <b>medical</b> or <b>religious</b> "
                        "exemption through Employee Health and Human Resources with "
                        "required documentation."
                    ),
                    Note(
                        "<b>Unvaccinated personnel (including approved exemptions) "
                        "must wear a surgical mask in all patient-care areas for the "
                        "entire declared influenza season.</b> Declination or "
                        "exemption does not waive the masking requirement."
                    ),
                ],
            ),
            Section(
                "Compliance and Documentation",
                [
                    Steps(
                        items=[
                            "Obtain vaccination or submit an exemption/declination "
                            "form by the campaign deadline.",
                            "Employee Health verifies and records status and issues "
                            "masking requirements to exempt/declining staff.",
                            "Managers monitor unit compliance; non-compliant "
                            "personnel are escalated to Employee Health and HR.",
                            "The facility reports aggregate personnel vaccination "
                            "coverage to CMS via NHSN for the reporting period.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity &amp; Reporting",
                [
                    Para(
                        "Classify and notify per <b>POL-RM-013</b>. A nosocomial "
                        "influenza outbreak linked to unvaccinated personnel with "
                        "patient death/harm is a <b>SEV-1</b>; a unit outbreak or "
                        "systemic compliance failure is a <b>SEV-2</b>; an individual "
                        "masking lapse or documentation gap is a "
                        "<b>SEV-3 / Near Miss</b>."
                    ),
                    TableBlock(
                        headers=["Severity", "Notify", "Deadline"],
                        rows=[
                            [
                                "SEV-1 (catastrophic / sentinel)",
                                "Infection Prevention, Employee Health, "
                                "administrator on call",
                                "Within 1 hour",
                            ],
                            [
                                "SEV-2 (major)",
                                "Infection Prevention and Employee Health",
                                "Within 4 hours",
                            ],
                            [
                                "SEV-3 / Near Miss (minor)",
                                "Employee Health via electronic event report",
                                "Within 24 hours",
                            ],
                        ],
                        col_widths=[2.0 * inch, 2.3 * inch, 1.5 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        items=[
                            "CDC recommendations for influenza vaccination of "
                            "health-care personnel (ACIP).",
                            "CMS requirements for reporting health-care-personnel "
                            "influenza vaccination via CDC NHSN.",
                            "POL-RM-013 &mdash; Incident Reporting and Event Severity "
                            "Classification.",
                            "POL-SAF-074 &mdash; Employee Tuberculosis Screening and "
                            "Respiratory Protection.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_fitness_for_duty() -> PolicyDoc:
    """Fitness for duty and impaired-practitioner handling."""
    return PolicyDoc(
        number="POL-SAF-076",
        title="Fitness for Duty and Impaired Practitioner",
        owner="Medical Staff / Human Resources",
        effective="2024-01-10",
        revised="2026-04-18",
        review="2028-04-18",
        version="2.0",
        approved_by="Medical Executive Committee",
        applies_to="All employees, licensed independent practitioners, allied "
        "health professionals, students, and contracted staff",
        keywords=[
            "fitness for duty",
            "impaired practitioner",
            "reasonable suspicion",
            "substance use",
            "wellness committee",
            "for-cause testing",
            "patient safety",
            "self-report",
        ],
        sections=[
            Section(
                "Purpose and Scope",
                [
                    Para(
                        "This policy protects patients and staff by ensuring that all "
                        "personnel are fit to perform their duties and by providing a "
                        "non-punitive pathway to identify, remove from duty, and "
                        "refer impaired practitioners for evaluation and treatment. "
                        "It is grounded in State licensing-board requirements, the "
                        "medical-staff bylaws, and the facility practitioner-health "
                        "program."
                    ),
                    Para(
                        "&ldquo;Impairment&rdquo; means an inability to practice or "
                        "work with reasonable skill and safety due to substance use, "
                        "a physical or mental health condition, or fatigue."
                    ),
                ],
            ),
            Section(
                "Identification and Reasonable Suspicion",
                [
                    Bullets(
                        items=[
                            "Any person who observes behavior suggesting impairment "
                            "has a duty to report it to a supervisor, the "
                            "administrator on call, or Medical Staff Services.",
                            "<b>Reasonable suspicion</b> is based on specific, "
                            "articulable observations &mdash; slurred speech, odor of "
                            "alcohol, unsteady gait, erratic behavior, or "
                            "deteriorating performance &mdash; documented "
                            "contemporaneously.",
                            "A practitioner may <b>self-report</b> a condition "
                            "confidentially to the Practitioner Wellness Committee "
                            "without automatic disciplinary action.",
                        ]
                    ),
                    Note(
                        "<b>If you reasonably suspect a colleague is impaired and "
                        "patients are at risk, act immediately: remove the person "
                        "from patient care and notify the supervisor or administrator "
                        "on call now.</b> Patient safety takes priority over the "
                        "individual&rsquo;s schedule."
                    ),
                ],
            ),
            Section(
                "Removal, Evaluation, and For-Cause Testing",
                [
                    Steps(
                        items=[
                            "Relieve the individual of duties and arrange safe "
                            "transport; do not allow them to drive if impaired.",
                            "Arrange for-cause / reasonable-suspicion fitness-for-duty "
                            "evaluation and testing per HR and medical-staff "
                            "procedures.",
                            "Refer to the Practitioner Wellness Committee or Employee "
                            "Assistance Program for assessment and a monitored "
                            "return-to-work plan.",
                            "Determine reporting obligations to the State licensing "
                            "board, consistent with bylaws and applicable law.",
                        ]
                    ),
                ],
            ),
            Section(
                "Return to Work and Confidentiality",
                [
                    Para(
                        "Return to practice follows a documented, monitored agreement "
                        "with defined conditions. Health information is handled "
                        "confidentially and separately from routine disciplinary "
                        "records, consistent with the non-punitive intent of the "
                        "practitioner-health program and applicable law."
                    ),
                ],
            ),
            Section(
                "Severity &amp; Reporting",
                [
                    Para(
                        "Classify and notify per <b>POL-RM-013</b>. Impairment that "
                        "contributes to a patient death or serious harm is a "
                        "<b>SEV-1</b>; removal of an impaired practitioner from active "
                        "patient care, or a credible threat, is a <b>SEV-2</b>; a "
                        "fitness concern addressed before any patient contact, or a "
                        "Near Miss, is a <b>SEV-3 / Near Miss</b>."
                    ),
                    TableBlock(
                        headers=["Severity", "Notify", "Deadline"],
                        rows=[
                            [
                                "SEV-1 (catastrophic / sentinel)",
                                "Medical Staff Office, HR, Risk Management, "
                                "administrator on call",
                                "Within 1 hour",
                            ],
                            [
                                "SEV-2 (major)",
                                "Supervisor, Medical Staff Office, and HR",
                                "Within 4 hours",
                            ],
                            [
                                "SEV-3 / Near Miss (minor)",
                                "Supervisor / HR via electronic event report",
                                "Within 24 hours",
                            ],
                        ],
                        col_widths=[2.0 * inch, 2.3 * inch, 1.5 * inch],
                        row_shades=[_SEV1, _SEV2, _SEV3],
                    ),
                    Para(
                        "If impairment presents as threatening or violent behavior, "
                        "also follow the workplace-violence policy "
                        "<b>POL-EH-011</b>."
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        items=[
                            "State licensing-board requirements for reporting and "
                            "managing impaired practitioners.",
                            "Medical-staff bylaws and the facility "
                            "practitioner-health / wellness program.",
                            "POL-RM-013 &mdash; Incident Reporting and Event Severity "
                            "Classification.",
                            "POL-EH-011 &mdash; Workplace Violence Prevention.",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_batch() -> list[PolicyDoc]:
    """Return this batch's policies, in listed order."""
    return [
        build_radiation_safety(),
        build_mri_safety(),
        build_laser_safety(),
        build_device_reporting(),
        build_tb_screening(),
        build_influenza_vaccination(),
        build_fitness_for_duty(),
    ]
