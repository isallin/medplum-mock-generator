import os
import requests
from faker import Faker
from urllib import response
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
base_url = os.getenv("BASE_URL")

fake = Faker("pt_BR")

def generate_telecom():
    telecom_type = fake.random_element(elements=["phone", "email"])
    if telecom_type == "phone":
        return {"system": "phone", "value": fake.phone_number(), "use": "mobile"}
    else:
        return {"system": "email", "value": fake.email(), "use": "home"}

def generate_patient() -> dict:
    selected_gender = fake.random_element(
        elements=["male", "female"]
    )
    if selected_gender == "male":
        first_name = fake.first_name_male()
    elif selected_gender == "female":
        first_name = fake.first_name_female()
    else:
        first_name = fake.first_name()

    return {
        "resourceType": "Patient",
        "gender": selected_gender,
        "name": [
            {
                "use": "official",
                "given": [first_name],
                "family": fake.last_name(),
            }
        ],
        "birthDate": fake.date_of_birth(minimum_age=1, maximum_age=100).isoformat(),
        "active": fake.random_element(elements=[True, False]),
        "telecom": [generate_telecom()],
        "address": [
            {
                "use": "home",
                "line": [fake.street_address()],
                "city": fake.city(),
                "state": fake.estado_sigla(),
                "postalCode": fake.postcode(),
                "country": "BR",
            }
        ],
        "identifier": [
            {
                "use": "official",
                "system": "http://saude.goias.gov/cpf",
                "value": fake.cpf(),
            }
        ],
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

def batch_bundle(size=100) -> dict:
    entries = []
    for _ in range(size):
        patient_data = generate_patient()
        entries.append({
            "request": {
                "method": "POST",
                "url": "Patient"
            },
            "resource": patient_data
        })
        
    return {
        "resourceType": "Bundle",
        "type": "batch",
        "entry": entries
    }

def send_batch_data(token, bundle):
    response = requests.post(
        f"{base_url}/fhir/R4/Patient",
        json=bundle,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/fhir+json",
            "accept": "application/fhir+json",
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def main():
    for i in range(2):
        print(f"Generating patient {i + 1}º...")
        try:
            token = authentication_medplum()
            bundle = batch_bundle(size=100)
            data = send_batch_data(token, bundle)
            print(f"Patient {i + 1}º generated successfully!")
            print(f"ID: {data.get('id')}")
            print(f"lastUpdated: {data.get('meta', {}).get('lastUpdated')}")
        except Exception as e:
            print(f"An error occurred while generating patient {i + 1}º: {e}")

if __name__ == "__main__":
    main()
