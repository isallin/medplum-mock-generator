import os
import random
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
BASE_URL = os.getenv("BASE_URL")
PROJECT_ID = os.getenv("PROJECT_ID")

BATCH_SIZE = 50
TOTAL_PATIENTS = 20
TOTAL_PROCEDURES = 20

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
MARITAGE_WEIGHTS = [0.45, 0.35, 0.10, 0.07, 0.03]

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
]

PROCEDURE_CATEGORIES = [
    {"code": "103693007", "display": "Diagnostic procedure"},
    {"code": "387713003", "display": "Surgical procedure"},
    {"code": "182832007", "display": "Procedure on body system"}
]

PROCEDURE_REASON_CODES = [
    {"code": "359746009", "display": "Patient's request"},
    {"code": "275245007", "display": "Clinical decision"},
    {"code": "410605003", "display": "Routine checkup"},
    {"code": "281239006", "display": "Urgent condition"}
]

def draw(elements, weights):
    return random.choices(elements, weights=weights, k=1)[0]