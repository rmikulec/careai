# Policy Corpus (test fixtures)

Synthetic but regulation-accurate hospital policy PDFs for testing the Incident Reporting Agent's retrieval, grounding, severity, and notification logic. The facility (“Riverside Regional Medical Center”) and all names are fictional; the cited standards (OSHA, CMS, The Joint Commission, NQF, CDC, FDA, HIPAA, NPIAP, EMTALA, AABB, ISMP, NCC MERP, etc.) are real.

Every policy shares one severity scale — **SEV-1 / SEV-2 / SEV-3 / Near Miss** — defined in `POL-RM-013` and referenced by every other policy, with concrete, time-bound notification deadlines stated in prose for the agent to extract.

Regenerate with:

```bash
python scripts/generate_policy_corpus.py
```

**67 policies.** Index below is auto-generated on each run.

| Policy # | Title | Owner | Pages | File |
|---|---|---|---|---|
| POL-CLN-040 | Rapid Response and Code Blue (Cardiopulmonary Resuscitation) | Resuscitation Committee / Nursing | 3 | `pol_cln_040_rapid_response_and_code_blue.pdf` |
| POL-CLN-041 | Early Warning Score and Deteriorating Patient Escalation | Nursing / Patient Safety | 2 | `pol_cln_041_early_warning_score_and_deteriorating.pdf` |
| POL-CLN-042 | Critical Value and Critical Test Result Reporting | Laboratory / Medical Staff | 2 | `pol_cln_042_critical_value_and_critical_test.pdf` |
| POL-CLN-043 | Massive Transfusion Protocol | Blood Bank / Trauma Services | 2 | `pol_cln_043_massive_transfusion_protocol.pdf` |
| POL-CLN-044 | Venous Thromboembolism (VTE) Prophylaxis | Medical Staff / Pharmacy | 2 | `pol_cln_044_venous_thromboembolism_vte_prophylaxis.pdf` |
| POL-CLN-045 | Contrast Media Reaction Management | Radiology / Nursing | 2 | `pol_cln_045_contrast_media_reaction_management.pdf` |
| POL-CLN-046 | Latex Allergy Management | Nursing / Perioperative Services | 2 | `pol_cln_046_latex_allergy_management.pdf` |
| POL-CMP-082 | Patient Grievance and Complaint Management | Patient Experience / Risk Management | 2 | `pol_cmp_082_patient_grievance_and_complaint_management.pdf` |
| POL-CMP-083 | Patient Rights and Responsibilities | Administration / Patient Experience | 2 | `pol_cmp_083_patient_rights_and_responsibilities.pdf` |
| POL-CMP-084 | Language Access and Interpreter Services | Patient Experience / Compliance | 2 | `pol_cmp_084_language_access_and_interpreter_services.pdf` |
| POL-CMP-085 | Verbal and Telephone Order Read-Back | Medical Staff / Nursing | 2 | `pol_cmp_085_verbal_and_telephone_order_read.pdf` |
| POL-CMP-086 | Primary Source Verification and Credentialing | Medical Staff Office / Human Resources | 2 | `pol_cmp_086_primary_source_verification_and_credentialing.pdf` |
| POL-ED-012 | EMTALA Compliance: Medical Screening and Transfer | Emergency Department / Medical Staff / Compliance | 1 | `pol_ed_012_emtala_compliance_medical_screening_and.pdf` |
| POL-EH-001 | Bloodborne Pathogen Exposure and Needlestick / Sharps Injury | Employee / Occupational Health · Environmental Health & Safety | 2 | `pol_eh_001_bloodborne_pathogen_exposure_and_needlestick.pdf` |
| POL-EH-011 | Workplace Violence Prevention and Reporting | Environmental Health & Safety · Employee Health · Security | 1 | `pol_eh_011_workplace_violence_prevention_and_reporting.pdf` |
| POL-EH-014 | Hazardous Material Spill and Chemical Exposure | Environmental Health & Safety | 1 | `pol_eh_014_hazardous_material_spill_and_chemical.pdf` |
| POL-EM-050 | Fire Safety and Response (Code Red) | Safety / Emergency Management | 3 | `pol_em_050_fire_safety_and_response_code.pdf` |
| POL-EM-051 | Severe Weather and Tornado Response | Emergency Management | 2 | `pol_em_051_severe_weather_and_tornado_response.pdf` |
| POL-EM-052 | Active Shooter and Hostile Event Response (Code Silver) | Security / Emergency Management | 2 | `pol_em_052_active_shooter_and_hostile_event.pdf` |
| POL-EM-053 | Mass Casualty Incident and Emergency Operations Plan Activation (Code Triage) | Emergency Management | 3 | `pol_em_053_mass_casualty_incident_and_emergency.pdf` |
| POL-EM-054 | Utility Systems and Power Failure | Facilities / Environment of Care | 2 | `pol_em_054_utility_systems_and_power_failure.pdf` |
| POL-EM-055 | Medical Gas and Vacuum System Failure | Facilities / Respiratory Therapy | 2 | `pol_em_055_medical_gas_and_vacuum_system.pdf` |
| POL-EM-056 | Bomb Threat Response | Security / Emergency Management | 2 | `pol_em_056_bomb_threat_response.pdf` |
| POL-EM-057 | Infant and Pediatric Abduction (Code Pink) | Security / Women's & Children's Services | 2 | `pol_em_057_infant_and_pediatric_abduction_code.pdf` |
| POL-HIM-080 | HIPAA Privacy and Protected Health Information | Compliance / Health Information Management | 2 | `pol_him_080_hipaa_privacy_and_protected_health.pdf` |
| POL-HIM-081 | Breach Notification | Compliance / Privacy Office | 2 | `pol_him_081_breach_notification.pdf` |
| POL-IC-020 | Hand Hygiene | Infection Prevention & Control | 3 | `pol_ic_020_hand_hygiene.pdf` |
| POL-IC-021 | Central Line-Associated Bloodstream Infection (CLABSI) Prevention | Infection Prevention & Control / Nursing | 2 | `pol_ic_021_central_line_associated_bloodstream_infection.pdf` |
| POL-IC-022 | Catheter-Associated Urinary Tract Infection (CAUTI) Prevention | Infection Prevention & Control / Nursing | 2 | `pol_ic_022_catheter_associated_urinary_tract_infection.pdf` |
| POL-IC-023 | Surgical Site Infection (SSI) Prevention | Infection Prevention & Control / Perioperative Services | 2 | `pol_ic_023_surgical_site_infection_ssi_prevention.pdf` |
| POL-IC-024 | Transmission-Based (Isolation) Precautions | Infection Prevention & Control | 2 | `pol_ic_024_transmission_based_isolation_precautions.pdf` |
| POL-IC-025 | Multidrug-Resistant Organism (MDRO) Management | Infection Prevention & Control | 2 | `pol_ic_025_multidrug_resistant_organism_mdro_management.pdf` |
| POL-IC-026 | Tuberculosis Exposure Control | Infection Prevention & Control / Employee Health | 2 | `pol_ic_026_tuberculosis_exposure_control.pdf` |
| POL-IC-027 | Reusable Medical Device Reprocessing and Sterilization | Sterile Processing / Infection Prevention & Control | 2 | `pol_ic_027_reusable_medical_device_reprocessing_and.pdf` |
| POL-LAB-006 | Blood Transfusion Administration and Reaction Management | Laboratory / Blood Bank (Transfusion Service) · Nursing | 2 | `pol_lab_006_blood_transfusion_administration_and_reaction.pdf` |
| POL-NUR-005 | Restraint and Seclusion | Nursing / Patient Care Services | 2 | `pol_nur_005_restraint_and_seclusion.pdf` |
| POL-NUR-009 | Hospital-Acquired Pressure Injury Prevention and Staging | Nursing / Wound, Ostomy & Continence (WOCN) | 2 | `pol_nur_009_hospital_acquired_pressure_injury_prevention.pdf` |
| POL-PC-060 | Suicide Risk Assessment and Management | Behavioral Health / Nursing | 3 | `pol_pc_060_suicide_risk_assessment_and_management.pdf` |
| POL-PC-061 | Behavioral Emergency and De-escalation (Code Gray) | Nursing / Security | 2 | `pol_pc_061_behavioral_emergency_and_de_escalation.pdf` |
| POL-PC-062 | Pain Assessment and Management | Nursing / Pharmacy | 2 | `pol_pc_062_pain_assessment_and_management.pdf` |
| POL-PC-063 | Code Status, Do-Not-Resuscitate, and Advance Directives | Medical Staff / Nursing | 2 | `pol_pc_063_code_status_do_not_resuscitate.pdf` |
| POL-PC-064 | Death Pronouncement and Postmortem Care | Medical Staff / Nursing | 2 | `pol_pc_064_death_pronouncement_and_postmortem_care.pdf` |
| POL-PC-065 | Against Medical Advice (AMA) Discharge | Medical Staff / Nursing | 2 | `pol_pc_065_against_medical_advice_ama_discharge.pdf` |
| POL-PC-066 | Informed Consent | Medical Staff / Risk Management | 2 | `pol_pc_066_informed_consent.pdf` |
| POL-PC-067 | Disclosure of Unanticipated Outcomes | Risk Management / Medical Staff | 2 | `pol_pc_067_disclosure_of_unanticipated_outcomes.pdf` |
| POL-PH-030 | Anticoagulation Management | Pharmacy / Nursing | 3 | `pol_ph_030_anticoagulation_management.pdf` |
| POL-PH-031 | Insulin and Glycemic Management | Pharmacy / Nursing | 2 | `pol_ph_031_insulin_and_glycemic_management.pdf` |
| POL-PH-032 | High-Alert Medication Management | Pharmacy | 2 | `pol_ph_032_high_alert_medication_management.pdf` |
| POL-PH-033 | Look-Alike / Sound-Alike (LASA) Medication Management | Pharmacy | 2 | `pol_ph_033_look_alike_sound_alike_lasa.pdf` |
| POL-PH-034 | Medication Reconciliation | Pharmacy / Nursing | 2 | `pol_ph_034_medication_reconciliation.pdf` |
| POL-PH-035 | Controlled Substance Diversion Prevention | Pharmacy / Compliance | 2 | `pol_ph_035_controlled_substance_diversion_prevention.pdf` |
| POL-PH-036 | Adverse Drug Reaction Reporting | Pharmacy / Patient Safety | 2 | `pol_ph_036_adverse_drug_reaction_reporting.pdf` |
| POL-PH-037 | Moderate (Procedural) Sedation | Anesthesia / Medical Staff | 3 | `pol_ph_037_moderate_procedural_sedation.pdf` |
| POL-PS-002 | Patient Fall Prevention and Post-Fall Response | Nursing / Patient Safety | 2 | `pol_ps_002_patient_fall_prevention_and_post.pdf` |
| POL-PS-003 | Medication Error and Adverse Drug Event Reporting | Pharmacy / Patient Safety | 2 | `pol_ps_003_medication_error_and_adverse_drug.pdf` |
| POL-PS-008 | Patient Identification | Patient Safety / Nursing | 1 | `pol_ps_008_patient_identification.pdf` |
| POL-RM-004 | Sentinel Event Management and Root Cause Analysis | Risk Management / Patient Safety | 2 | `pol_rm_004_sentinel_event_management_and_root.pdf` |
| POL-RM-013 | Incident Reporting and Event Severity Classification | Risk Management / Patient Safety | 3 | `pol_rm_013_incident_reporting_and_event_severity.pdf` |
| POL-SAF-070 | Radiation Safety (Diagnostic and Interventional) | Radiation Safety / Radiology | 2 | `pol_saf_070_radiation_safety_diagnostic_and_interventional.pdf` |
| POL-SAF-071 | Magnetic Resonance Imaging (MRI) Safety | Radiology / Safety | 2 | `pol_saf_071_magnetic_resonance_imaging_mri_safety.pdf` |
| POL-SAF-072 | Laser Safety | Perioperative Services / Safety | 2 | `pol_saf_072_laser_safety.pdf` |
| POL-SAF-073 | Medical Device Malfunction, Recall, and FDA Reporting | Clinical Engineering / Risk Management | 2 | `pol_saf_073_medical_device_malfunction_recall_and.pdf` |
| POL-SAF-074 | Employee Tuberculosis Screening and Respiratory Protection | Employee Health / Infection Prevention &amp; Control | 2 | `pol_saf_074_employee_tuberculosis_screening_and_respiratory.pdf` |
| POL-SAF-075 | Healthcare Personnel Influenza Vaccination | Employee Health / Infection Prevention &amp; Control | 2 | `pol_saf_075_healthcare_personnel_influenza_vaccination.pdf` |
| POL-SAF-076 | Fitness for Duty and Impaired Practitioner | Medical Staff / Human Resources | 2 | `pol_saf_076_fitness_for_duty_and_impaired.pdf` |
| POL-SEC-010 | Patient Elopement and Missing Patient Response | Security / Nursing / Emergency Management | 1 | `pol_sec_010_patient_elopement_and_missing_patient.pdf` |
| POL-SURG-007 | Universal Protocol: Prevention of Wrong-Site, Wrong-Procedure, and Wrong-Person Surgery | Perioperative Services / Patient Safety | 2 | `pol_surg_007_universal_protocol_prevention_of_wrong.pdf` |
