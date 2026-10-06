"""Emergency Management and Environment of Care policies for the corpus.

This batch holds Riverside Regional Medical Center's life-safety and emergency
preparedness policies (overhead codes, HICS activation, and utility/medical-gas
contingencies). Each policy is fictional-facility prose anchored to the real
governing standards — The Joint Commission Emergency Management (EM) and
Environment of Care (EC) chapters, the CMS Emergency Preparedness Rule (42 CFR
482.15), NFPA 101 / NFPA 99, OSHA, and FBI/DHS and NCMEC guidance — so the
Incident Reporting Agent has realistic material to retrieve, cite, and ground
severity/notification decisions against. Every policy reuses the facility-wide
severity scheme from POL-RM-013 (SEV-1 within 1 hour, SEV-2 within 4 hours,
SEV-3 / Near Miss within 24 hours) and restates the immediate actions a reporter
must surface before intake is complete.
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


def build_fire() -> PolicyDoc:
    """Fire safety and response (Code Red): RACE and PASS."""
    return PolicyDoc(
        number="POL-EM-050",
        title="Fire Safety and Response (Code Red)",
        owner="Safety / Emergency Management",
        effective="2023-04-01",
        revised="2026-02-12",
        review="2028-02-12",
        version="3.2",
        approved_by="Environment of Care Committee",
        applies_to="All staff, licensed providers, students, volunteers, and "
        "contractors, in all buildings and on all shifts",
        keywords=[
            "fire",
            "code red",
            "race",
            "pass",
            "evacuation",
            "fire alarm",
            "life safety",
            "defend in place",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To protect life and property through early fire detection, "
                        "prompt notification, confinement, and — only when necessary "
                        "— extinguishment or evacuation, consistent with the NFPA 101 "
                        "Life Safety Code and The Joint Commission Environment of Care "
                        "and Emergency Management standards. Riverside Regional "
                        "Medical Center is a fully sprinklered, compartmentalized "
                        "facility and follows a <b>defend-in-place</b> strategy: in a "
                        "fire, patients are protected behind fire/smoke barriers "
                        "rather than immediately removed from the building."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to any fire, smoke, or odor of burning discovered in "
                        "any area of the facility, and to the actions of every person "
                        "present regardless of role. Staff who discover a fire act "
                        "immediately; they do not wait for the fire alarm or for "
                        "Security."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Code Red</b> — the overhead alert announcing a fire or "
                            "suspected fire, followed by the specific location.",
                            "<b>RACE</b> — the immediate-action sequence: Rescue, "
                            "Alarm, Confine, Extinguish or Evacuate.",
                            "<b>PASS</b> — the fire-extinguisher technique: Pull, Aim, "
                            "Squeeze, Sweep.",
                            "<b>Defend in place</b> — protecting occupants behind "
                            "rated fire/smoke barriers (closing doors, moving patients "
                            "to an adjacent smoke compartment) instead of leaving the "
                            "building.",
                            "<b>Smoke compartment</b> — an area bounded by "
                            "smoke-resistant barriers and self-closing doors into "
                            "which occupants can be moved horizontally.",
                        ]
                    ),
                ],
            ),
            Section(
                "Procedure — RACE",
                [
                    Note(
                        "<b>RACE: Rescue, Alarm, Confine, Extinguish/Evacuate.</b> "
                        "Rescue anyone in immediate danger, pull the nearest fire "
                        "alarm and call the emergency number to announce Code Red with "
                        "the exact location, close doors to confine smoke and fire, "
                        "then extinguish only a small incipient fire or evacuate. "
                        "Never use elevators during a Code Red."
                    ),
                    Steps(
                        [
                            "<b>R &ndash; Rescue.</b> Remove any person in immediate "
                            "danger from the fire or smoke to a safe adjacent area.",
                            "<b>A &ndash; Alarm.</b> Activate the nearest manual pull "
                            "station and call the emergency number to report a Code "
                            "Red and the exact location; do not assume someone else "
                            "has called.",
                            "<b>C &ndash; Confine.</b> Close all doors and windows to "
                            "contain smoke and fire; clear corridors of equipment.",
                            "<b>E &ndash; Extinguish or Evacuate.</b> If the fire is "
                            "small, incipient, and you are trained, use the nearest "
                            "extinguisher with the PASS technique; otherwise close the "
                            "door and evacuate horizontally to the next smoke "
                            "compartment.",
                        ]
                    ),
                    Para(
                        "<b>Evacuation order (when required):</b> move occupants "
                        "<b>horizontally</b> through smoke-barrier doors to an "
                        "adjacent compartment first; use <b>vertical</b> (stairwell) "
                        "evacuation to a lower floor only if the compartment is "
                        "untenable; <b>full building evacuation</b> is a last resort "
                        "directed by the Incident Commander or the fire department."
                    ),
                ],
            ),
            Section(
                "Evacuation Priority",
                [
                    Para(
                        "When an area must be cleared, evacuate in order of mobility "
                        "and proximity to the fire. The least mobile patients are "
                        "moved first only when they are in the immediate path of fire "
                        "or smoke; otherwise ambulatory patients are moved first to "
                        "clear the egress path."
                    ),
                    TableBlock(
                        headers=["Priority", "Group", "Typical method"],
                        rows=[
                            [
                                "1",
                                "Occupants in the room of fire origin and the "
                                "immediately adjacent rooms.",
                                "Direct carry/assist to the next smoke compartment.",
                            ],
                            [
                                "2",
                                "Ambulatory patients in the affected compartment.",
                                "Walk, staff-escorted, through barrier doors.",
                            ],
                            [
                                "3",
                                "Wheelchair / assisted-mobility patients.",
                                "Wheelchair or transport chair.",
                            ],
                            [
                                "4",
                                "Non-ambulatory / critical patients (ICU, OR, "
                                "ventilated).",
                                "Bed, stretcher, or rescue-sheet drag; staff "
                                "accompany life-support equipment.",
                            ],
                        ],
                        col_widths=[0.8 * inch, 2.6 * inch, 2.4 * inch],
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Fire events are classified under POL-RM-013. A fire causing "
                        "injury, requiring patient evacuation, or resulting in a fire "
                        "department response with suppression is <b>SEV-1</b>: notify "
                        "the Administrator-on-Call, Safety Officer, and Facilities "
                        "immediately and within 1 hour, and activate the Hospital "
                        "Incident Command System (HICS) if the event extends beyond a "
                        "single compartment. A contained incipient fire extinguished "
                        "without injury or evacuation is <b>SEV-2</b> (notify Safety "
                        "and Facilities within 4 hours). A fire-alarm activation with "
                        "no fire, or a code-correctable fire-safety deficiency, is "
                        "<b>SEV-3 / Near Miss</b>, reported within 24 hours. File an "
                        "event report for every Code Red, including false alarms and "
                        "cooking/steam nuisance activations."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Exact location, time of discovery, and how the fire or "
                            "alarm was detected.",
                            "Whether the alarm was activated and the time the fire "
                            "department was notified / arrived.",
                            "Actions taken (RACE steps, extinguisher used, doors "
                            "closed, evacuation performed and to where).",
                            "Any injuries, patient moves, and equipment or structural "
                            "damage.",
                            "Notifications made (who, when, by what method) and HICS "
                            "activation status.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "NFPA 101, Life Safety Code — health care occupancies "
                            "(defend-in-place, smoke compartments, egress).",
                            "NFPA 99, Health Care Facilities Code; NFPA 10 — portable "
                            "fire extinguishers.",
                            "The Joint Commission, Environment of Care (EC.02.03.01) "
                            "and Emergency Management standards; Life Safety (LS) "
                            "chapter.",
                            "CMS Emergency Preparedness Rule, 42 CFR 482.15.",
                            "Related: POL-RM-013 (severity & reporting), POL-EM-053 "
                            "(HICS / Code Triage), POL-EM-054 (utility failure).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_severe_weather() -> PolicyDoc:
    """Severe weather and tornado response (shelter-in-place)."""
    return PolicyDoc(
        number="POL-EM-051",
        title="Severe Weather and Tornado Response",
        owner="Emergency Management",
        effective="2023-05-15",
        revised="2026-02-14",
        review="2028-02-14",
        version="2.3",
        approved_by="Emergency Management Committee",
        applies_to="All staff, patients, and visitors in all buildings; "
        "coordinated through the House Supervisor and HICS",
        keywords=[
            "severe weather",
            "tornado",
            "watch",
            "warning",
            "shelter in place",
            "hazard vulnerability analysis",
            "hics",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To protect patients, staff, and visitors from injury during "
                        "tornadoes, severe thunderstorms, and other high-wind events "
                        "through timely monitoring, shelter-in-place, and — when "
                        "warranted — activation of the Hospital Incident Command "
                        "System, consistent with the CMS Emergency Preparedness Rule "
                        "and The Joint Commission Emergency Management standards. "
                        "Severe weather is addressed in the facility Hazard "
                        "Vulnerability Analysis (HVA)."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to all facility buildings and grounds. The House "
                        "Supervisor (or designee) monitors National Weather Service "
                        "alerts for the county and initiates the actions below on a "
                        "watch or warning."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Tornado Watch</b> — conditions are favorable for "
                            "tornadoes; prepare and monitor.",
                            "<b>Tornado Warning</b> — a tornado has been sighted or "
                            "indicated by radar; take shelter immediately.",
                            "<b>Shelter-in-place</b> — moving occupants to designated "
                            "interior, lowest-feasible-floor areas away from windows "
                            "and exterior walls.",
                            "<b>Safe areas</b> — pre-identified interior corridors, "
                            "stairwell cores, and interior rooms without exterior "
                            "glass, marked on unit emergency maps.",
                        ]
                    ),
                ],
            ),
            Section(
                "Procedure",
                [
                    Note(
                        "On a <b>Tornado Warning</b>, move patients, staff, and "
                        "visitors away from all windows and exterior walls into "
                        "designated interior safe areas on the lowest feasible floor, "
                        "close doors, and have everyone crouch low and protect their "
                        "heads. Do not use elevators. Non-transportable critical "
                        "patients are sheltered in place with blankets/mattresses for "
                        "shielding."
                    ),
                    TableBlock(
                        headers=["Alert", "Actions"],
                        rows=[
                            [
                                "Tornado Watch",
                                "House Supervisor notifies units; identify safe areas "
                                "and shelter routes; charge bed/equipment batteries; "
                                "close blinds; prepare to move patients.",
                            ],
                            [
                                "Tornado Warning",
                                "Announce overhead; move occupants to interior safe "
                                "areas away from glass; close all doors; shield "
                                "non-transportable patients; account for staff; "
                                "consider HICS activation.",
                            ],
                            [
                                "All Clear",
                                "House Supervisor / Incident Commander announces all "
                                "clear; assess for damage, injuries, and utility loss; "
                                "return occupants; document.",
                            ],
                        ],
                        col_widths=[1.4 * inch, 4.4 * inch],
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Severe-weather impacts are classified under POL-RM-013. "
                        "Structural damage, loss of a utility, or any patient/staff "
                        "injury is <b>SEV-1</b>: notify the Administrator-on-Call and "
                        "Safety Officer immediately and within 1 hour, and activate "
                        "HICS. A warning that required shelter-in-place without injury "
                        "or damage is documented as a <b>SEV-3</b> operational event "
                        "within 24 hours; near misses (e.g., unsecured exterior "
                        "equipment identified during a watch) are reported within "
                        "24 hours."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Alert type and time received; time shelter-in-place was "
                            "initiated and lifted.",
                            "Units sheltered and whether any patients were moved; "
                            "staff/patient accounting.",
                            "Injuries, structural damage, and utility impacts "
                            "identified on the post-event survey.",
                            "HICS activation status and notifications made.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CMS Emergency Preparedness Rule, 42 CFR 482.15 "
                            "(all-hazards risk assessment / HVA).",
                            "The Joint Commission, Emergency Management (EM) standards "
                            "— mitigation and response.",
                            "National Weather Service watch/warning definitions.",
                            "Related: POL-RM-013 (severity & reporting), POL-EM-053 "
                            "(HICS / Code Triage), POL-EM-054 (utility failure).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_active_shooter() -> PolicyDoc:
    """Active shooter and hostile event response (Code Silver): Run-Hide-Fight."""
    return PolicyDoc(
        number="POL-EM-052",
        title="Active Shooter and Hostile Event Response (Code Silver)",
        owner="Security / Emergency Management",
        effective="2023-06-01",
        revised="2026-03-02",
        review="2028-03-02",
        version="2.0",
        approved_by="Emergency Management Committee",
        applies_to="All staff, licensed providers, students, volunteers, "
        "contractors, patients, and visitors, in all areas",
        keywords=[
            "active shooter",
            "code silver",
            "weapon",
            "run hide fight",
            "hostile event",
            "lockdown",
            "law enforcement",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To save lives during an active-shooter or armed/hostile "
                        "intruder event through the FBI/DHS <b>Run&ndash;Hide&ndash;"
                        "Fight</b> survival strategy, immediate law-enforcement "
                        "notification, lockdown, and coordination through the Hospital "
                        "Incident Command System, consistent with The Joint Commission "
                        "Emergency Management standards and OSHA workplace-violence "
                        "guidance."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to any event involving an active shooter, a person "
                        "brandishing or threatening with a weapon, or an armed hostile "
                        "intruder anywhere on the campus. Individual survival actions "
                        "take precedence; staff are not expected to confront an armed "
                        "assailant."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Code Silver</b> — the overhead alert for an active "
                            "shooter or person with a weapon, followed by location.",
                            "<b>Run (Avoid)</b> — evacuate away from the threat if "
                            "there is an accessible escape path.",
                            "<b>Hide (Deny)</b> — if escape is not possible, shelter "
                            "out of view behind a locked/barricaded door, silence "
                            "phones, and stay quiet.",
                            "<b>Fight (Defend)</b> — as a last resort when life is in "
                            "imminent danger, act with aggression to incapacitate the "
                            "attacker.",
                            "<b>Lockdown</b> — securing units and the facility to deny "
                            "the attacker access and movement.",
                        ]
                    ),
                ],
            ),
            Section(
                "Procedure — Run, Hide, Fight",
                [
                    Note(
                        "<b>Run &middot; Hide &middot; Fight.</b> RUN: if there is a "
                        "safe escape path, leave belongings and get out, keeping "
                        "hands visible for responding officers. HIDE: if you cannot "
                        "escape, lock/barricade the door, turn off lights, silence "
                        "phones, and stay out of sight. FIGHT: only as a last resort "
                        "to save your life. Call 911 and the facility emergency number "
                        "to announce Code Silver with the location as soon as it is "
                        "safe."
                    ),
                    Steps(
                        [
                            "<b>Run.</b> If there is an accessible escape route, "
                            "evacuate immediately; leave belongings behind, help "
                            "others if possible, and keep hands empty and visible.",
                            "<b>Hide.</b> If you cannot escape, move out of the "
                            "attacker's view; lock and barricade the door with heavy "
                            "furniture; turn off lights; silence all devices; remain "
                            "quiet.",
                            "<b>Fight.</b> As a last resort and only when your life is "
                            "in imminent danger, commit to disrupting or "
                            "incapacitating the attacker using improvised weapons and "
                            "aggression.",
                            "<b>Notify.</b> Call 911 and the facility emergency number "
                            "when safe; report location, number of shooters, "
                            "description, and weapons. Initiate lockdown of your area.",
                            "<b>On law-enforcement arrival.</b> Remain calm, keep "
                            "hands visible and empty, follow all commands, and do not "
                            "run toward or grab officers; they will move to the threat "
                            "first, not to the injured.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "An active-shooter or armed-intruder event is a <b>SEV-1</b> "
                        "catastrophic event under POL-RM-013. Notify law enforcement "
                        "(911) and Security <b>immediately</b>; notify the "
                        "Administrator-on-Call and Safety Officer within 1 hour; "
                        "activate HICS. A casualty surge from the event is managed "
                        "concurrently under POL-EM-053 (Code Triage). A credible "
                        "weapon threat without discharge, or a weapon recovered without "
                        "injury, is at least <b>SEV-2</b> and still reported. File an "
                        "event report once the scene is secure; preserve the scene for "
                        "law enforcement and do not disturb evidence."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Location, time, and how the threat was identified.",
                            "Description of the assailant(s), weapon(s), and direction "
                            "of travel as reported.",
                            "Areas locked down, evacuated, or sheltered; staff and "
                            "patient accounting.",
                            "Injuries and casualties; law-enforcement and EMS response "
                            "times.",
                            "HICS activation and all notifications (who, when, by what "
                            "method).",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "FBI, Active Shooter Resources; DHS/CISA, "
                            "Run&ndash;Hide&ndash;Fight active-shooter guidance.",
                            "The Joint Commission, Emergency Management (EM) and "
                            "workplace-violence requirements.",
                            "OSHA, workplace-violence prevention for healthcare "
                            "(General Duty Clause, Publication 3148).",
                            "Related: POL-RM-013 (severity & reporting), POL-EM-053 "
                            "(Code Triage / HICS), POL-EM-056 (bomb threat), "
                            "POL-EH-011 (workplace violence).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_mass_casualty() -> PolicyDoc:
    """Mass casualty incident and EOP / HICS activation (Code Triage)."""
    return PolicyDoc(
        number="POL-EM-053",
        title="Mass Casualty Incident and Emergency Operations Plan "
        "Activation (Code Triage)",
        owner="Emergency Management",
        effective="2023-07-01",
        revised="2026-03-04",
        review="2028-03-04",
        version="3.1",
        approved_by="Emergency Management Committee",
        applies_to="All departments, the medical staff, and leadership; "
        "coordinated through the Hospital Command Center",
        keywords=[
            "mass casualty",
            "code triage",
            "hics",
            "emergency operations plan",
            "surge",
            "incident command",
            "start triage",
            "command center",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To establish a coordinated, scalable response to a mass "
                        "casualty incident (MCI) or other emergency that exceeds "
                        "routine capacity, through activation of the facility "
                        "Emergency Operations Plan (EOP) and the Hospital Incident "
                        "Command System (HICS), consistent with the CMS Emergency "
                        "Preparedness Rule (42 CFR 482.15) and The Joint Commission "
                        "Emergency Management standards."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to any internal or external event producing a surge "
                        "of patients or a major disruption to operations "
                        "(multi-vehicle crash, industrial event, severe weather, "
                        "infrastructure failure, or an on-campus mass-casualty event). "
                        "The EOP is built on the six critical functions required by "
                        "the Emergency Management standards: communications, "
                        "resources and assets, safety and security, staff "
                        "responsibilities, utilities, and patient clinical/support "
                        "activities."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Code Triage</b> — the overhead alert for activation "
                            "of the EOP for a mass casualty or disaster; announced as "
                            "Code Triage <i>Alert</i> (stand-by) or <i>Activation</i> "
                            "(full response).",
                            "<b>HICS</b> — the Hospital Incident Command System, a "
                            "standardized ICS-based management structure with an "
                            "Incident Commander and Operations, Planning, Logistics, "
                            "and Finance/Administration sections.",
                            "<b>Hospital Command Center (HCC)</b> — the physical or "
                            "virtual location from which the incident is managed.",
                            "<b>START triage</b> — Simple Triage And Rapid Treatment; "
                            "sorts casualties into Immediate (red), Delayed (yellow), "
                            "Minor/walking (green), and Expectant/deceased (black).",
                        ]
                    ),
                ],
            ),
            Section(
                "Procedure — Activation",
                [
                    Note(
                        "Any charge nurse, House Supervisor, or physician recognizing "
                        "a surge beyond capacity may request a Code Triage. The House "
                        "Supervisor or Administrator-on-Call activates the EOP, opens "
                        "the Hospital Command Center, and assumes (or assigns) the "
                        "Incident Commander role until relieved. All responders report "
                        "through HICS and use plain language."
                    ),
                    Steps(
                        [
                            "Recognize and declare: notify the House Supervisor / "
                            "Administrator-on-Call; announce Code Triage Alert or "
                            "Activation overhead.",
                            "Open the Hospital Command Center and establish the "
                            "Incident Commander and needed HICS section chiefs.",
                            "Decompress the ED and surge capacity: discharge/transfer "
                            "eligible patients, open overflow areas, and recall staff "
                            "per the labor pool.",
                            "Triage incoming casualties with START; direct patients to "
                            "designated red/yellow/green treatment areas.",
                            "Manage communications, resources, and documentation "
                            "through HICS; brief at regular operational-period "
                            "intervals.",
                            "Demobilize and debrief when the surge resolves; announce "
                            "all clear and begin recovery.",
                        ]
                    ),
                ],
            ),
            Section(
                "HICS Command and General Staff",
                [
                    TableBlock(
                        headers=["HICS role", "Core responsibility"],
                        rows=[
                            [
                                "Incident Commander",
                                "Overall authority and accountability; sets "
                                "objectives; approves the incident action plan.",
                            ],
                            [
                                "Operations Section Chief",
                                "Directs tactical response — triage, treatment, "
                                "clinical care, and patient movement.",
                            ],
                            [
                                "Planning Section Chief",
                                "Tracks situation status and resources; develops the "
                                "incident action plan and documentation.",
                            ],
                            [
                                "Logistics Section Chief",
                                "Secures staff, supplies, equipment, beds, and "
                                "facility/communications support.",
                            ],
                            [
                                "Finance/Administration Chief",
                                "Tracks cost, time, procurement, and claims.",
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
                        "A mass casualty incident is a <b>SEV-1</b> event under "
                        "POL-RM-013 by definition of its scope. HICS activation itself "
                        "constitutes immediate executive notification; the "
                        "Administrator-on-Call, Safety Officer, and Risk Management are "
                        "engaged within 1 hour. Individual patient-care events "
                        "occurring during the response are classified and reported on "
                        "their own merits once operations stabilize. After-action "
                        "review and an improvement plan are completed by Emergency "
                        "Management, and the event informs the next Hazard "
                        "Vulnerability Analysis."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Time of recognition, declaration, and command-center "
                            "activation; Incident Commander of record.",
                            "HICS organization chart and section assignments "
                            "(HICS 203/207).",
                            "Operational-period objectives and incident action plans "
                            "(HICS 201/202).",
                            "Casualty count by triage category and disposition; bed "
                            "and resource status.",
                            "Demobilization, all-clear time, and the after-action "
                            "report / improvement plan.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "CMS Emergency Preparedness Rule, 42 CFR 482.15 (EOP, "
                            "training/testing, communications).",
                            "The Joint Commission, Emergency Management (EM) chapter — "
                            "six critical functions.",
                            "HHS ASPR, Hospital Incident Command System (HICS) Guidebook "
                            "and forms.",
                            "Related: POL-RM-013 (severity & reporting), POL-EM-050 "
                            "through POL-EM-057 (code-specific response).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_utility_failure() -> PolicyDoc:
    """Utility systems and power failure response."""
    return PolicyDoc(
        number="POL-EM-054",
        title="Utility Systems and Power Failure",
        owner="Facilities / Environment of Care",
        effective="2023-08-15",
        revised="2026-02-22",
        review="2028-02-22",
        version="2.4",
        approved_by="Environment of Care Committee",
        applies_to="All staff in clinical and support areas; coordinated by "
        "Facilities and the House Supervisor",
        keywords=[
            "utility failure",
            "power failure",
            "emergency power",
            "generator",
            "red outlets",
            "water loss",
            "hvac",
            "environment of care",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To maintain safe patient care during failure of a critical "
                        "utility system — electrical power, water, medical gas, HVAC, "
                        "vertical transport, or communications — through an emergency "
                        "power supply system and documented contingency procedures, "
                        "consistent with The Joint Commission Environment of Care "
                        "(utility systems) standards, NFPA 99, NFPA 110, and the CMS "
                        "Emergency Preparedness Rule."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to any interruption of a utility that supports "
                        "patient care or a safe environment. Staff recognize the "
                        "failure, protect patients dependent on the affected utility, "
                        "and notify Facilities so the system can be restored or a "
                        "backup engaged."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Emergency Power Supply System (EPSS)</b> — the "
                            "generator(s) and transfer switches that restore power to "
                            "life-safety, critical, and equipment branches on loss of "
                            "normal power.",
                            "<b>Red (emergency) outlets</b> — receptacles powered by "
                            "the emergency generator branch; life-support and critical "
                            "equipment must be plugged into these.",
                            "<b>Life-safety branch</b> — emergency lighting, exit "
                            "signs, fire alarm, and medical-gas alarms.",
                            "<b>Critical branch</b> — task lighting and receptacles "
                            "serving patient care that is essential to life.",
                        ]
                    ),
                ],
            ),
            Section(
                "Procedure — Power Failure",
                [
                    Note(
                        "On loss of normal power, the emergency generator restores "
                        "power to <b>red outlets</b> within about 10 seconds. "
                        "Immediately verify that all life-support and critical "
                        "equipment (ventilators, monitors, pumps, suction) is on a red "
                        "outlet, confirm it has restarted, and switch any device not "
                        "on emergency power. Keep flashlights at each nurse station; "
                        "never use elevators until cleared."
                    ),
                    Steps(
                        [
                            "Ensure patient safety first: verify ventilators, "
                            "monitors, and infusion pumps are running on emergency "
                            "power; move any to red outlets if not.",
                            "For a device that did not restart, provide manual support "
                            "(e.g., bag-valve ventilation) and call for help.",
                            "Notify Facilities / the plant operator and the House "
                            "Supervisor; report the location and extent of the "
                            "outage.",
                            "Deploy flashlights; secure elevators and verify no one is "
                            "trapped; restrict non-essential elevator and equipment "
                            "use.",
                            "If the outage is prolonged or widespread, the House "
                            "Supervisor considers HICS activation and surge/transfer "
                            "planning.",
                            "File an event report per POL-RM-013 and log the "
                            "generator run and restoration time.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Utility failures are classified under POL-RM-013. A failure "
                        "that harms a patient, or a complete loss of emergency power "
                        "or of a utility to a critical care area (ICU, OR, ED), is "
                        "<b>SEV-1</b>: notify the Administrator-on-Call, Safety "
                        "Officer, and Facilities leadership immediately and within "
                        "1 hour, and activate HICS for a prolonged or facility-wide "
                        "loss. A localized failure requiring intervention without "
                        "patient harm is <b>SEV-2</b> (within 4 hours). A brief "
                        "interruption with automatic restoration and no impact, or a "
                        "deficiency found on rounds, is <b>SEV-3 / Near Miss</b> "
                        "within 24 hours."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Utility affected, location, and time of failure and "
                            "restoration.",
                            "Whether emergency power engaged automatically; generator "
                            "run time.",
                            "Patient-care equipment affected and any manual support "
                            "provided.",
                            "Injuries or clinical impact; notifications and HICS "
                            "status.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "The Joint Commission, Environment of Care — utility "
                            "systems (EC.02.05.01, EC.02.05.03, EC.02.05.07).",
                            "NFPA 99, Health Care Facilities Code; NFPA 110, Emergency "
                            "and Standby Power Systems.",
                            "CMS Emergency Preparedness Rule, 42 CFR 482.15 "
                            "(emergency and standby power).",
                            "Related: POL-RM-013 (severity & reporting), POL-EM-055 "
                            "(medical gas failure), POL-EM-053 (HICS / Code Triage).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_medical_gas() -> PolicyDoc:
    """Medical gas and vacuum system failure response."""
    return PolicyDoc(
        number="POL-EM-055",
        title="Medical Gas and Vacuum System Failure",
        owner="Facilities / Respiratory Therapy",
        effective="2023-09-15",
        revised="2026-02-24",
        review="2028-02-24",
        version="2.1",
        approved_by="Environment of Care Committee",
        applies_to="All clinical staff in areas supplied by medical gases; "
        "Facilities and Respiratory Therapy",
        keywords=[
            "medical gas",
            "oxygen",
            "vacuum",
            "zone valve",
            "nfpa 99",
            "piped gas",
            "e-cylinder",
            "respiratory therapy",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To maintain oxygenation and suction for patients during "
                        "failure, contamination, or depletion of a piped medical gas "
                        "or vacuum system, and to safely isolate a leaking or involved "
                        "zone, consistent with NFPA 99 (medical gas and vacuum "
                        "systems) and The Joint Commission Environment of Care "
                        "standards."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to piped oxygen, medical air, nitrous oxide, and "
                        "medical-surgical vacuum in all patient-care areas. Clinical "
                        "staff maintain patient oxygenation with backup cylinders "
                        "while Facilities and Respiratory Therapy diagnose and restore "
                        "the system."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Zone (shutoff) valve</b> — a wall valve, usually "
                            "outside each patient area, that isolates the medical gas "
                            "supply to that zone.",
                            "<b>Master alarm / area alarm</b> — NFPA 99 alarms that "
                            "annunciate abnormal source or zone pressure to the plant "
                            "and to staffed areas.",
                            "<b>E-cylinder</b> — a portable compressed-gas cylinder "
                            "used as a backup oxygen source at the bedside or during "
                            "transport.",
                            "<b>Medical-surgical vacuum</b> — the piped suction system "
                            "used for airway, wound, and gastric suction.",
                        ]
                    ),
                ],
            ),
            Section(
                "Procedure — Gas Supply Failure",
                [
                    Note(
                        "Only a qualified person closes a zone valve, and only after "
                        "confirming which rooms it feeds and that <b>every</b> patient "
                        "in that zone has an alternate oxygen source (E-cylinder) in "
                        "place. Closing the wrong valve, or closing one before "
                        "patients are converted to cylinders, can stop oxygen to "
                        "ventilated patients. Keep full E-cylinders and regulators "
                        "immediately available on every unit."
                    ),
                    Steps(
                        [
                            "Recognize the failure (alarm, loss of flow/pressure, or "
                            "odor); assess every affected patient's oxygenation.",
                            "Place patients on backup oxygen (E-cylinders with "
                            "regulators); provide manual ventilation for ventilated "
                            "patients if needed and use portable suction.",
                            "Notify Facilities / the plant operator, the House "
                            "Supervisor, and Respiratory Therapy immediately; report "
                            "the gas, area, and symptoms.",
                            "Isolate only if directed: a qualified person closes the "
                            "correct zone valve for a leak or fire after confirming "
                            "all patients are on backup supply.",
                            "Monitor cylinder levels and arrange resupply; plan "
                            "transfer of gas-dependent patients if restoration will be "
                            "prolonged (consider HICS).",
                            "File an event report per POL-RM-013; log alarm, isolation, "
                            "and restoration times.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "Medical gas/vacuum failures are classified under POL-RM-013. "
                        "A loss of oxygen or vacuum to a critical area (ICU, OR, ED, "
                        "NICU), contaminated gas, or any patient harm is <b>SEV-1</b>: "
                        "notify the Administrator-on-Call, Safety Officer, and "
                        "Facilities leadership immediately and within 1 hour, and "
                        "activate HICS for a source-level or facility-wide loss. A "
                        "localized zone failure managed on backup cylinders without "
                        "harm is <b>SEV-2</b> (within 4 hours). A nuisance alarm or a "
                        "deficiency found on inspection with no clinical impact is "
                        "<b>SEV-3 / Near Miss</b> within 24 hours."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Gas or system affected, zone/area, and time of failure "
                            "and restoration.",
                            "Alarms that annunciated; whether a zone valve was closed "
                            "and by whom.",
                            "Patients affected, backup source applied, and any manual "
                            "support.",
                            "Clinical impact/injury; notifications and HICS status.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "NFPA 99, Health Care Facilities Code — medical gas and "
                            "vacuum systems, zone valves, and alarms.",
                            "The Joint Commission, Environment of Care — utility "
                            "systems (medical gas) and inventory of critical "
                            "components.",
                            "CMS Conditions of Participation / Emergency Preparedness "
                            "Rule, 42 CFR 482.15.",
                            "Related: POL-RM-013 (severity & reporting), POL-EM-054 "
                            "(utility / power failure), POL-EM-053 (HICS).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_bomb_threat() -> PolicyDoc:
    """Bomb threat response and checklist."""
    return PolicyDoc(
        number="POL-EM-056",
        title="Bomb Threat Response",
        owner="Security / Emergency Management",
        effective="2023-10-15",
        revised="2026-02-26",
        review="2028-02-26",
        version="2.2",
        approved_by="Emergency Management Committee",
        applies_to="All staff who may receive a threat (operators, unit clerks, "
        "front-line staff); coordinated by Security",
        keywords=[
            "bomb threat",
            "suspicious package",
            "threat checklist",
            "evacuation",
            "law enforcement",
            "search",
            "code black",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To ensure a calm, information-gathering response to a bomb "
                        "threat or suspicious package that protects occupants, "
                        "preserves evidence, and defers tactical decisions to law "
                        "enforcement, consistent with FBI/DHS (CISA) bomb-threat "
                        "guidance and The Joint Commission Emergency Management "
                        "standards."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to any bomb threat received by phone, in writing, by "
                        "email, or verbally, and to the discovery of a suspicious or "
                        "unattended package anywhere on the campus. The person who "
                        "receives a telephoned threat keeps the caller on the line and "
                        "records details; they do not decide whether to evacuate."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Bomb threat</b> — a communicated threat, with or "
                            "without a device, to detonate an explosive to cause harm "
                            "or disruption.",
                            "<b>Suspicious package</b> — an unattended or unusual item "
                            "with characteristics suggesting a possible explosive "
                            "device.",
                            "<b>Bomb-threat checklist</b> — the standardized form used "
                            "to capture caller details, exact wording, and background "
                            "sounds in real time.",
                        ]
                    ),
                ],
            ),
            Section(
                "Procedure — Telephoned Threat",
                [
                    Note(
                        "<b>Stay calm, keep the caller talking, and write down every "
                        "detail.</b> Do not hang up even after the caller does. If a "
                        "suspicious item is found, <b>do not touch, move, or open it</b> "
                        "and <b>do not use radios or cell phones near it</b> — they can "
                        "trigger a device. Call 911 and Security immediately, then "
                        "follow law-enforcement direction on search and evacuation."
                    ),
                    Steps(
                        [
                            "Keep the caller on the line; do not hang up. Signal a "
                            "coworker to call 911 and Security.",
                            "Complete the bomb-threat checklist: exact wording, stated "
                            "location and time of detonation, caller voice/accent, and "
                            "background noises.",
                            "After the call, preserve the caller-ID display and your "
                            "notes; do not erase anything.",
                            "For a suspicious package, do not touch or move it, clear "
                            "and cordon the area, and avoid radio/cell transmissions "
                            "nearby.",
                            "Security and law enforcement direct any search "
                            "(staff know their own areas best) and any evacuation or "
                            "shelter decision.",
                            "File an event report per POL-RM-013 once the scene is "
                            "released.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "A bomb threat is at least a <b>SEV-2</b> event under "
                        "POL-RM-013 and is escalated to <b>SEV-1</b> when a device or "
                        "credible suspicious package is found, an evacuation is "
                        "ordered, or anyone is injured. Notify law enforcement (911) "
                        "and Security <b>immediately</b>; notify the "
                        "Administrator-on-Call and Safety Officer within 1 hour for a "
                        "SEV-1, within 4 hours otherwise, and activate HICS if the "
                        "facility is searched or evacuated. All threats, including "
                        "those deemed non-credible, are documented and reported within "
                        "24 hours."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Completed bomb-threat checklist with exact wording and "
                            "time of the threat.",
                            "Caller-ID / source information and how the threat was "
                            "received.",
                            "Areas searched or evacuated; whether a device or package "
                            "was found and its disposition.",
                            "Law-enforcement notification and response; HICS "
                            "activation and all notifications.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "DHS/CISA, Bomb Threat Guidance and DHS Bomb Threat "
                            "Checklist; FBI bomb-threat resources.",
                            "The Joint Commission, Emergency Management (EM) "
                            "standards.",
                            "CMS Emergency Preparedness Rule, 42 CFR 482.15.",
                            "Related: POL-RM-013 (severity & reporting), POL-EM-052 "
                            "(active shooter), POL-EM-053 (HICS / Code Triage).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_infant_abduction() -> PolicyDoc:
    """Infant and pediatric abduction (Code Pink)."""
    return PolicyDoc(
        number="POL-EM-057",
        title="Infant and Pediatric Abduction (Code Pink)",
        owner="Security / Women's & Children's Services",
        effective="2023-11-15",
        revised="2026-03-06",
        review="2028-03-06",
        version="2.0",
        approved_by="Emergency Management Committee",
        applies_to="All staff, with primary roles in Women's & Children's "
        "Services, Pediatrics, the Nursery/NICU, and Security",
        keywords=[
            "infant abduction",
            "code pink",
            "pediatric abduction",
            "ncmec",
            "lockdown",
            "exit control",
            "security",
            "sentinel event",
        ],
        sections=[
            Section(
                "Purpose",
                [
                    Para(
                        "To prevent the abduction of an infant or child and to mount "
                        "an immediate, coordinated recovery response if one occurs, "
                        "consistent with National Center for Missing &amp; Exploited "
                        "Children (NCMEC) guidelines, The Joint Commission Emergency "
                        "Management and security standards, and the facility infant "
                        "security (electronic tagging) program."
                    ),
                ],
            ),
            Section(
                "Scope",
                [
                    Para(
                        "Applies to all areas serving infants and children, "
                        "especially the Nursery, NICU, Labor &amp; Delivery, "
                        "Postpartum, and Pediatrics. Every staff member participates "
                        "in a Code Pink response: monitoring exits, stairwells, and "
                        "elevators, and observing anyone carrying an infant or a "
                        "bag/package that could conceal one."
                    ),
                ],
            ),
            Section(
                "Definitions",
                [
                    Bullets(
                        [
                            "<b>Code Pink</b> — the overhead alert for a missing or "
                            "abducted infant; <b>Code Purple</b> (or Code Pink&ndash;"
                            "Pediatric, per facility convention) is used for a child.",
                            "<b>Infant security system</b> — electronic tags that alarm "
                            "and may lock doors/elevators if a tagged infant approaches "
                            "or passes an exit.",
                            "<b>Abductor profile (NCMEC)</b> — typically a female "
                            "visitor who may impersonate staff, becomes familiar with "
                            "routines, and carries a large bag; most abducted infants "
                            "are recovered, and planning assumes rapid response saves "
                            "the child.",
                        ]
                    ),
                ],
            ),
            Section(
                "Procedure",
                [
                    Note(
                        "A suspected infant abduction is a <b>SEV-1 sentinel event</b>. "
                        "The moment an infant is unaccounted for, announce Code Pink, "
                        "notify Security and the Administrator-on-Call, and call "
                        "<b>911 / law enforcement immediately</b> &mdash; activate HICS. "
                        "Staff lock down and monitor all exits, stairwells, and "
                        "elevators, and discreetly observe anyone leaving with an "
                        "infant or a large bag. Do not wait to confirm before calling."
                    ),
                    Steps(
                        [
                            "Confirm the infant is missing and announce Code Pink with "
                            "the unit; notify Security and the charge nurse "
                            "immediately.",
                            "Call 911 / law enforcement immediately and notify the "
                            "Administrator-on-Call; activate HICS.",
                            "Initiate lockdown: staff proceed to and monitor all exits, "
                            "stairwells, and elevators; preserve the infant's room as a "
                            "scene.",
                            "Gather and broadcast a description of the infant and of "
                            "any suspect/vehicle; observe and delay (do not physically "
                            "confront) anyone matching the profile.",
                            "Account for all infants and children on the affected "
                            "units; provide the parents a private area and support.",
                            "File an event report and preserve all evidence (footage, "
                            "visitor logs, tag data) for law enforcement and Risk "
                            "Management.",
                        ]
                    ),
                ],
            ),
            Section(
                "Severity & Reporting",
                [
                    Para(
                        "An infant or pediatric abduction is a <b>SEV-1 sentinel "
                        "event</b> under POL-RM-013. Notify the Administrator-on-Call, "
                        "Security, and law enforcement <b>immediately</b> (within "
                        "minutes, never later than 1 hour) and activate HICS. Risk "
                        "Management coordinates mandatory sentinel-event management "
                        "under POL-RM-004, including a comprehensive systematic "
                        "analysis (RCA&sup2;) within 45 business days. An infant or "
                        "child merely missing from the unit (not abducted) is handled "
                        "as an elopement under POL-SEC-010 and is still at least "
                        "<b>SEV-2</b>, escalating to SEV-1 if the child cannot be "
                        "located or is harmed."
                    ),
                ],
            ),
            Section(
                "Documentation Requirements",
                [
                    Bullets(
                        [
                            "Infant/child identity, last-seen time and location, and "
                            "who discovered the absence.",
                            "Description of any suspect and vehicle; whether the infant "
                            "security tag alarmed.",
                            "Exits/elevators secured, lockdown time, and staff "
                            "assignments.",
                            "Law-enforcement notification and response; HICS "
                            "activation and all notifications.",
                            "Evidence preserved (video, visitor logs, tag data) and "
                            "chain of custody.",
                        ]
                    ),
                ],
            ),
            Section(
                "References",
                [
                    Bullets(
                        [
                            "NCMEC, For Healthcare Professionals: Guidelines on "
                            "Prevention of and Response to Infant Abductions.",
                            "The Joint Commission, Emergency Management (EM) and "
                            "security / environment-of-care standards; infant-abduction "
                            "sentinel-event alerts.",
                            "CMS Emergency Preparedness Rule, 42 CFR 482.15.",
                            "Related: POL-RM-013 (severity & reporting), POL-RM-004 "
                            "(sentinel event / RCA&sup2;), POL-SEC-010 (elopement / "
                            "missing patient), POL-EM-053 (HICS).",
                        ]
                    ),
                ],
            ),
        ],
    )


def build_batch() -> list[PolicyDoc]:
    """Return this batch's policies, in listed order."""
    return [
        build_fire(),
        build_severe_weather(),
        build_active_shooter(),
        build_mass_casualty(),
        build_utility_failure(),
        build_medical_gas(),
        build_bomb_threat(),
        build_infant_abduction(),
    ]
