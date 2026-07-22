import os
import random
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BASE_URL = os.getenv("BASE_URL")
PROJECT_ID = os.getenv("PROJECT_ID")

P_EXHIGH = 0.95
P_HIGH = 0.75
P_MID = 0.50
P_LOW = 0.15
P_EXLOW = 0.02

GENDER_ELEMENTS = ["male", "female", "other", "unknown"]
GENDER_WEIGHTS = [0.48, 0.48, 0.02, 0.02]

MARITAGE_ELEMENTS = [
    {"code": "S", "display": "Never Married"},
    {"code": "M", "display": "Married"},
    {"code": "D", "display": "Divorced"},
    {"code": "W", "display": "Widowed"},
    {"code": "T", "display": "Domestic Partner"}
]
MARITAGE_WEIGHTS = [0.35, 0.35, 0.15, 0.10, 0.05]

PRACTITIONER_QUALIFICATIONS = [
    {"code": "CRM", "display": "Conselho Regional de Medicina", "system": "http://saude.goias.gov/crm"},
    {"code": "COREN", "display": "Conselho Regional de Enfermagem", "system": "http://saude.goias.gov/coren"},
    {"code": "CRF", "display": "Conselho Regional de Farmácia", "system": "http://saude.goias.gov/crf"}
]

PRACTITIONER_SPECIALTIES = [
    {"code": "394579002", "display": "Cardiology"},
    {"code": "394582007", "display": "Dermatology"},
    {"code": "394583002", "display": "Endocrinology"},
    {"code": "394814009", "display": "General practice"},
    {"code": "394591006", "display": "Neurology"}
]

PROCEDURE_STAT = [
    "preparation", "in-progress", "not-done", "on-hold",
    "stopped", "completed", "entered-in-error", "unknown"
]
PROCEDURE_STAT_WEIGHTS = [0.15, 0.25, 0.04, 0.05, 0.05, 0.40, 0.01, 0.05]

SNOMED_PROCEDURES = [
    {"code": "80146002", "display": "Appendectomy"},
    {"code": "11987000", "display": "Excision of lesion of skin"},
    {"code": "232717009", "display": "Coronary artery bypass graft"},
    {"code": "173160006", "display": "Biopsy of breast"},
    {"code": "8032002", "display": "Repair of inguinal hernia"},
    {"code": "235222002", "display": "Colonoscopy"},
    {"code": "387713003", "display": "Surgical procedure"},
    {"code": "18286008", "display": "Laparoscopic cholecystectomy"},
    {"code": "52734007", "display": "Total hip replacement"},
    {"code": "17931000", "display": "Total knee replacement"},
    {"code": "48387007", "display": "Tracheostomy"},
    {"code": "30549001", "display": "Suture of wound"},
    {"code": "71388002", "display": "Upper gastrointestinal endoscopy"},
    {"code": "230056004", "display": "Cerebral angiography"},
    {"code": "116859006", "display": "Blood transfusion"},
    {"code": "182531007", "display": "Hemodialysis"}
]

PROCEDURE_CATEGORIES = [
    {"code": "103693007", "display": "Diagnostic procedure"},
    {"code": "387713003", "display": "Surgical procedure"},
    {"code": "182832007", "display": "Procedure on body system"},
    {"code": "277132007", "display": "Therapeutic procedure"},
    {"code": "410606002", "display": "Social service procedure"},
    {"code": "225358003", "display": "Wound care"},
    {"code": "363687006", "display": "Imaging procedure"},
    {"code": "128927009", "display": "Dental procedure"},
    {"code": "386637004", "display": "Obstetric procedure"},
]

PROCEDURE_REASON_CODES = [
    {"code": "359746009", "display": "Patient's request"},
    {"code": "275245007", "display": "Clinical decision"},
    {"code": "410605003", "display": "Routine checkup"},
    {"code": "281239006", "display": "Urgent condition"}
]

OBSERVATION_STAT = ["registered", "preliminary", "final", "amended", "corrected"]
OBSERVATION_STAT_WEIGHTS = [0.02, 0.08, 0.85, 0.03, 0.02]

LOINC_OBSERVATIONS = [
    {
        "code": "8867-4",
        "display": "Heart rate",
        "unit": "beats/min",
        "ucum": "/min",
        "category": "vital-signs",
        "min": 55, "max": 110, "type": "int"
    },
    {
        "code": "2708-6",
        "display": "Oxygen saturation in Arterial blood by Pulse oximetry",
        "unit": "%",
        "ucum": "%",
        "category": "vital-signs",
        "min": 92, "max": 100, "type": "int"
    },
    {
        "code": "8310-5",
        "display": "Body temperature",
        "unit": "C",
        "ucum": "Cel",
        "category": "vital-signs",
        "min": 35.5, "max": 39.0, "type": "float"
    },
    {
        "code": "2339-0",
        "display": "Glucose [Mass/volume] in Blood",
        "unit": "mg/dL",
        "ucum": "mg/dL",
        "category": "laboratory",
        "min": 70, "max": 180, "type": "int"
    },
    {
        "code": "2947-0",
        "display": "Body weight",
        "unit": "kg",
        "ucum": "kg",
        "category": "vital-signs",
        "min": 50.0, "max": 110.0, "type": "float"
    }
]

MEDICATION_STAT = ["active", "inactive", "entered-in-error"]
MEDICATION_STAT_WEIGHTS = [0.85, 0.12, 0.03]

MEDICATION_FORMS = [
    {"code": "385055001", "display": "Tablet"},
    {"code": "385049006", "display": "Capsule"},
    {"code": "385023001", "display": "Solution for injection"},
    {"code": "385018001", "display": "Oral suspension"},
    {"code": "385101003", "display": "Ointment"}
]

MEDICATION_RXNORM = [
    {"code": "197361", "display": "Amoxicillin 500 MG Oral Capsule", "form_code": "385049006"},
    {"code": "198440", "display": "Acetaminophen 500 MG Oral Tablet", "form_code": "385055001"},
    {"code": "197696", "display": "Ibuprofen 600 MG Oral Tablet", "form_code": "385055001"},
    {"code": "310809", "display": "Dipyrone 500 MG/ML Oral Solution", "form_code": "385018001"},
    {"code": "855332", "display": "Metformin hydrochloride 850 MG Oral Tablet", "form_code": "385055001"},
    {"code": "197885", "display": "Losartan potassium 50 MG Oral Tablet", "form_code": "385055001"},
    {"code": "309362", "display": "Omeprazole 20 MG Oral Capsule", "form_code": "385049006"}
]

MED_REQUEST_STATUS = ["active", "on-hold", "cancelled", "completed", "entered-in-error", "stopped", "draft"]
MED_REQUEST_STATUS_WEIGHTS = [0.60, 0.05, 0.05, 0.20, 0.02, 0.05, 0.03]

MED_REQUEST_INTENT = ["proposal", "plan", "order", "original-order", "reflex-order", "filler-order", "instance-order", "option"]
MED_REQUEST_INTENT_WEIGHTS = [0.05, 0.05, 0.80, 0.02, 0.02, 0.02, 0.02, 0.02]

MED_REQUEST_CATEGORIES = [
    {"code": "inpatient", "display": "Inpatient"},
    {"code": "outpatient", "display": "Outpatient"},
    {"code": "community", "display": "Community"},
    {"code": "discharge", "display": "Discharge"}
]

APPOINTMENT_STAT = ["proposed", "pending", "booked", "arrived", "fulfilled", "cancelled", "noshow"]
APPOINTMENT_STAT_WEIGHTS = [0.05, 0.10, 0.40, 0.15, 0.20, 0.05, 0.05]

APPOINTMENT_SERVICE_TYPES = [
    {"code": "408443003", "display": "General medical practice"},
    {"code": "394579002", "display": "Cardiology"},
    {"code": "394582007", "display": "Dermatology"},
    {"code": "394583002", "display": "Endocrinology"},
    {"code": "394814009", "display": "General practice"}
]

ENCOUNTER_STAT = ["planned", "arrived", "triaged", "in-progress", "onleave", "finished", "cancelled"]
ENCOUNTER_STAT_WEIGHTS = [0.05, 0.10, 0.10, 0.25, 0.02, 0.43, 0.05]

ENCOUNTER_CLASSES = [
    {"code": "AMB", "display": "ambulatory"},
    {"code": "EMER", "display": "emergency"},
    {"code": "IMP", "display": "inpatient encounter"},
    {"code": "TELE", "display": "teleconsultation"}
]

ENCOUNTER_TYPES = [
    {"code": "11429006", "display": "Consultation"},
    {"code": "408443003", "display": "General medical practice"},
    {"code": "50849002", "display": "Emergency room admission"},
    {"code": "185349003", "display": "Encounter for check up"}
]

CONDITION_CLINICAL_STATUS = ["active", "recurrence", "relapse", "inactive", "remission", "resolved"]
CONDITION_CLINICAL_STATUS_WEIGHTS = [0.65, 0.05, 0.05, 0.10, 0.05, 0.10]

CONDITION_VERIFICATION_STATUS = ["unconfirmed", "provisional", "differential", "confirmed", "refuted"]
CONDITION_VERIFICATION_STATUS_WEIGHTS = [0.05, 0.10, 0.05, 0.78, 0.02]

CONDITION_CATEGORIES = [
    {"code": "problem-list-item", "display": "Problem List Item"},
    {"code": "encounter-diagnosis", "display": "Encounter Diagnosis"}
]

ICD10_CONDITIONS = [
    {"code": "I10", "display": "Essential (primary) hypertension", "snomed_code": "59621000"},
    {"code": "E11", "display": "Type 2 diabetes mellitus", "snomed_code": "44054006"},
    {"code": "J45", "display": "Asthma", "snomed_code": "195967001"},
    {"code": "K21.9", "display": "Gastro-esophageal reflux disease without esophagitis", "snomed_code": "235595009"},
    {"code": "M81.0", "display": "Age-related osteoporosis without current pathological fracture", "snomed_code": "64859006"},
    {"code": "F41.1", "display": "Generalized anxiety disorder", "snomed_code": "21897009"}
]