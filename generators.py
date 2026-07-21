import random
from datetime import date
from faker import Faker
from config import (
    P_EXHIGH, P_HIGH, P_MID, P_EXLOW,
    gender_elements, gender_weights,
    maritage_elements, maritage_weights,
    procedure_stat, procedure_stat_weights,
    snomed_procedures, draw
)

fake = Faker("pt_BR")

def generate_patient() -> dict:
    selected_gender = draw(gender_elements, gender_weights)
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
        mrt = draw(maritage_elements, maritage_weights)
        patient["maritalStatus"] = {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus",
                "code": mrt["code"],
                "display": mrt["display"]
            }]
        }

    return patient


def generate_procedure(patient_id: str, patient_name: str) -> dict:
    selected_code = random.choice(snomed_procedures)
    return {
        "resourceType": "Procedure",
        "status": draw(procedure_stat, procedure_stat_weights),
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

def generate_bundle(resources: list, resource_type: str) -> dict:
    bundle = {"resourceType": "Bundle", "type": "transaction", "entry": []}
    for res in resources:
        entry = {
            "resource": res,
            "request": {"method": "POST", "url": resource_type}
        }
        bundle["entry"].append(entry)
    return bundle

