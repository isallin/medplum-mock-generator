import os
import json
import random
import requests
from faker import Faker
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
base_url = os.getenv("BASE_URL")

# Configuring random probabilities
prob_elements = [True, False]
exhigh_prob = [0.95, 0.05], high_prob = [0.75, 0.25], mid_prob = [0.5, 0.5]
low_prob = [0.15, 0.85], exlow_prob = [0.02, 0.98]

gender_elements = ["male", "female", "other", "unknown"]
gender_weights = [0.45, 0.45, 0.05, 0.05]

maritage_elements = [
    {"code": "S", "display": "Never Married"},
    {"code": "M", "display": "Married"},
    {"code": "D", "display": "Divorced"},
    {"code": "W", "display": "Widowed"},
    {"code": "T", "display": "Domestic Partner"}
]
maritage_weights = [45, 35, 10, 7, 3]

telecom_elements = ["phone", "email"]
telecom_weights = [0.7, 0.3]

fake = Faker("pt_BR")

def generate_telecom():
    telecom_type = random.choices(telecom_elements, weights=telecom_weights, k=1)[0]
    if telecom_type == "phone":
        return {"system": "phone", "value": fake.phone_number(), "use": "mobile"}
    else:
        return {"system": "email", "value": fake.email(), "use": "home"}

def generate_patient() -> dict:
    # Defining gender
    selected_gender = random.choices(gender_elements, weights=gender_weights, k=1)[0]
    if selected_gender == "male":
        first_name = fake.first_name_male()
    elif selected_gender == "female":
        first_name = fake.first_name_female()
    else:
        first_name = fake.first_name()

    if random.choices(prob_elements, weights=exhigh_prob, k=1)[0]:
        patient_name = {
            "use": "official",
            "given": [first_name],
            "family": fake.last_name(),
        }
    
    if random.choices(prob_elements, weights=exhigh_prob, k=1)[0]:
        patient_gender = selected_gender
    
    if random.choices(prob_elements, weights=exhigh_prob, k=1)[0]:
        patient_birth = fake.date_of_birth(minimum_age=1, maximum_age=100).isoformat()
    
    if random.choices(prob_elements, weights=high_prob, k=1)[0]:
        patient_active = random.choices(prob_elements, weights=high_prob, k=1)[0]
    
    if random.choices(prob_elements, weights=high_prob, k=1)[0]:
        patient_telecom = [generate_telecom()]
    
    if random.choices(prob_elements, weights=mid_prob, k=1)[0]:
        patient_address = [
            {
                "use": "home",
                "line": [fake.street_address()],
                "city": fake.city(),
                "state": fake.estado_sigla(),
                "postalCode": fake.postcode(),
                "country": "BR",
            }
        ]
        
    if random.choices(prob_elements, weights=mid_prob, k=1)[0]:
        patient_identify = [
            {
                "use": "official",
                "system": "http://saude.goias.gov/cpf",
                "value": fake.cpf(),
            }
        ]

    if random.choices(prob_elements, weights=high_prob, k=1)[0]:
        if random.choices(prob_elements, weights=exlow_prob, k=1)[0]:
            if patient_birth:
                if random.choices(prob_elements, weights=mid_prob, k=1)[0]:
                    patient_deceased = fake.date_between_dates(date_start=patient_birth, date_end="today")
                else:
                    patient_deceased = True
            else:
                patient_deceased = fake.date_between(start_date="-50y", end_date="today")
        else:
            patient_deceased = False

    if random.choices(prob_elements, weights=exlow_prob, k=1)[0]:
        if random.choices(prob_elements, weights=mid_prob, k=1)[0]:
            patient_multbirth = True
        else:
            patient_multbirth = random.randint(2, 5)

    if random.choices(prob_elements, weights=high_prob, k=1)[0]:
        mrtsorted = random.choices(maritage_elements, weights=maritage_weights, k=1)[0]
        patient_marital = {
            "coding": [
                {
                    "system": "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus",
                    "code": mrtsorted["code"],
                    "display": mrtsorted["display"]
                }
            ]
        }

def authentication_medplum():
    token_url = f"{base_url}/oauth2/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(token_url, data=data)
    return response.json()["access_token"]


def generate_bundle(patients):
    bundle = {"resourceType": "Bundle", "type": "transaction", "entry": []}

    for patient in patients:
        entry = {"resource": patient, "request": {"method": "POST", "url": "Patient"}}
        bundle["entry"].append(entry)

    return bundle


def send_data(token, bundle):
    response = requests.post(
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
    for i in range(10):
        try:
            token = authentication_medplum()
            patients = [generate_patient() for _ in range(50)]
            bundle = generate_bundle(patients)
            data = send_data(token, bundle)
            print(f"Bundle {i + 1}º generated successfully!")
        except Exception as e:
            print(f"An error occurred while generating bundle {i + 1}º: {e}")


if __name__ == "__main__":
    main()