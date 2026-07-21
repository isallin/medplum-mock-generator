import random
from datetime import date, timezone
from faker import Faker
from config import (
    P_EXHIGH, P_HIGH, P_MID, P_LOW, P_EXLOW,
    GENDER_ELEMENTS, GENDER_WEIGHTS,
    MARITAGE_ELEMENTS, MARITAGE_WEIGHTS,
    PROCEDURE_STAT, PROCEDURE_STAT_WEIGHTS,
    SNOMED_PROCEDURES, PROCEDURE_CATEGORIES, 
    PROCEDURE_REASON_CODES, draw
)

fake = Faker("pt_BR")

def generate_patient() -> dict:
    selected_gender = draw(GENDER_ELEMENTS, GENDER_WEIGHTS)
    if selected_gender == "male":
        first_name = fake.first_name_male()
    elif selected_gender == "female":
        first_name = fake.first_name_female()
    else:
        first_name = fake.first_name()

    patient = {
        "resourceType": "Patient",
        "name": [{
            "use": "official",
            "given": [first_name],
            "family": fake.last_name(),
        }]
    }

    if random.random() < P_EXHIGH:
        patient["gender"] = selected_gender

    patient_birth = None
    if random.random() < P_EXHIGH:
        patient_birth = fake.date_of_birth(minimum_age=1, maximum_age=100)
        patient["birthDate"] = patient_birth.isoformat()

    if random.random() < P_EXHIGH:
        patient["active"] = random.random() < P_EXHIGH

    if random.random() < P_HIGH:
        if random.random() < P_HIGH:
            patient["telecom"] = [{"system": "phone", "value": fake.phone_number(), "use": "mobile"}]
        else:
            patient["telecom"] = [{"system": "email", "value": fake.email(), "use": "home"}]

    if random.random() < P_MID:
        patient["address"] = [{
            "use": "home",
            "line": [fake.street_address()],
            "city": fake.city(),
            "state": "GO",
            "postalCode": fake.postcode(),
            "country": "BR",
        }]

    if random.random() < P_MID:
        patient["identifier"] = [{
            "use": "official",
            "system": "http://saude.goias.gov/cpf",
            "value": fake.cpf(),
        }]

    if random.random() < P_HIGH:
        if random.random() < P_EXLOW:
            if patient_birth:
                if random.random() < P_MID:
                    dt_morte = fake.date_between_dates(date_start=patient_birth, date_end=date.today())
                    patient["deceasedDateTime"] = dt_morte.isoformat()
                else:
                    patient["deceasedBoolean"] = True
            else:
                dt_morte = fake.date_between(start_date="-50y", end_date=date.today())
                patient["deceasedDateTime"] = dt_morte.isoformat()
        else:
            patient["deceasedBoolean"] = False

    if random.random() < P_EXLOW:
        if random.random() < P_MID:
            patient["multipleBirthBoolean"] = True
        else:
            patient["multipleBirthInteger"] = random.randint(2, 5)

    minimal_age = date.today().replace(year=date.today().year - 18)
    if patient_birth and patient_birth <= minimal_age and random.random() < P_HIGH:
        mrt = draw(MARITAGE_ELEMENTS, MARITAGE_WEIGHTS)
        patient["maritalStatus"] = {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus",
                "code": mrt["code"],
                "display": mrt["display"]
            }]
        }

    return patient

def generate_procedure(patient_id: str, patient_name: str) -> dict:
    selected_code = random.choice(SNOMED_PROCEDURES)
    
    procedure = {
        "resourceType": "Procedure",
        "status": draw(PROCEDURE_STAT, PROCEDURE_STAT_WEIGHTS),
        "code": {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": selected_code["code"],
                "display": selected_code["display"]
            }]
        },
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": patient_name
        }
    }

    if random.random() < P_EXHIGH:
        procedure["identifier"] = [{
            "use": "official",
            "system": "http://saude.goias.gov/procedimentos",
            "value": fake.numerify("########")
        }]

    if random.random() < P_HIGH:
        category = random.choice(PROCEDURE_CATEGORIES)
        procedure["category"] = {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": category["code"],
                "display": category["display"]
            }]
        }

    if random.random() < P_EXHIGH:
        dt_performed = fake.date_time_between(start_date="-2y", end_date="now", tzinfo=timezone.utc)
        procedure["performedDateTime"] = dt_performed.isoformat()

    if random.random() < P_MID:
        reason = random.choice(PROCEDURE_REASON_CODES)
        procedure["reasonCode"] = [{
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": reason["code"],
                "display": reason["display"]
            }]
        }]

    if random.random() < P_MID:
        procedure["location"] = {
            "display": f"Hospital {fake.company()}"
        }

    if random.random() < P_LOW:
        procedure["note"] = [{
            "text": fake.sentence(nb_words=10)
        }]

    return procedure

def generate_bundle(resources: list, resource_type: str) -> dict:
    bundle = {"resourceType": "Bundle", "type": "transaction", "entry": []}
    for res in resources:
        entry = {
            "resource": res,
            "request": {"method": "POST", "url": resource_type}
        }
        bundle["entry"].append(entry)
    return bundle

def chunk_list(data: list, size: int):
    for i in range(0, len(data), size):
        yield data[i:i + size]