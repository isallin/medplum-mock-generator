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

gender_elements = ["male", "female", "other", "unknown"]
gender_weights = [0.48, 0.48, 0.02, 0.02]

maritage_elements = [
    {"code": "S", "display": "Never Married"},
    {"code": "M", "display": "Married"},
    {"code": "D", "display": "Divorced"},
    {"code": "W", "display": "Widowed"},
    {"code": "T", "display": "Domestic Partner"}
]
maritage_weights = [0.45, 0.35, 0.10, 0.07, 0.03]

procedure_stat = [
    "preparation", "in-progress", "not-done", "on-hold",
    "stopped", "completed", "entered-in-error", "unknown"
]
procedure_stat_weights = [0.15, 0.25, 0.04, 0.05, 0.05, 0.40, 0.01, 0.05]

snomed_procedures = [
    {"code": "80146002", "display": "Appendectomy"},
    {"code": "11987000", "display": "Excision of lesion of skin"},
    {"code": "232717009", "display": "Coronary artery bypass graft"},
    {"code": "173160006", "display": "Biopsy of breast"},
    {"code": "8032002", "display": "Repair of inguinal hernia"},
    {"code": "235222002", "display": "Colonoscopy"},
]

def draw(elements, weights):
    return random.choices(elements, weights=weights, k=1)[0]