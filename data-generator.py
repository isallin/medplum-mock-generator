import os
import random
import requests
from faker import Faker
from datetime import date
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
base_url = os.getenv("BASE_URL")
project_id = os.getenv("PROJECT_ID")

fake = Faker("pt_BR")

P_EXHIGH = 0.95
P_HIGH   = 0.75
P_MID    = 0.50
P_LOW    = 0.15
P_EXLOW  = 0.02

gender_elements = ["male", "female", "other", "unknown"]
gender_weights = [0.45, 0.45, 0.05, 0.05]

maritage_elements = [
    {"code": "S", "display": "Never Married"},
    {"code": "M", "display": "Married"},
    {"code": "D", "display": "Divorced"},
    {"code": "W", "display": "Widowed"},
    {"code": "T", "display": "Domestic Partner"}
]
maritage_weights = [0.45, 0.35, 0.10, 0.07, 0.03]

def draw(elements, weights):
    return random.choices(elements, weights=weights, k=1)[0]

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
        if random.random() < P_EXHIGH: patient["active"] = True
        else: patient["active"] = False
    
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
            "state": fake.estado_sigla(),
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

def authentication_medplum(session: requests.Session) -> str:
    token_url = f"{base_url}/oauth2/token"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": f"project/{project_id}"
    }
    
    response = session.post(token_url, data=data, headers=headers)
    response.raise_for_status()
    
    return response.json()["access_token"]


def generate_bundle(patients):
    bundle = {"resourceType": "Bundle", "type": "transaction", "entry": []}

    for patient in patients:
        entry = {"resource": patient, "request": {"method": "POST", "url": "Patient"}}
        bundle["entry"].append(entry)

    return bundle


def send_data(session: requests.Session, token: str, bundle: dict) -> dict:
    response = session.post(
        f"{base_url}/fhir/R4",
        json=bundle,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/fhir+json",
            "accept": "application/fhir+json",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def main():
    with requests.Session() as session:
        try:
            print("Autenticando no Medplum...")
            token = authentication_medplum(session)
        except Exception as e:
            print(f"Falha ao autenticar: {e}")
            return

        try:
            patients = [generate_patient() for _ in range(10)]
            bundle = generate_bundle(patients)

            send_data(session, token, bundle)
            print(f"Bundle enviado com sucesso! (10 pacientes)")
        except Exception as e:
            print(f"Erro ao enviar o bundle: {e}")


if __name__ == "__main__":
    main()