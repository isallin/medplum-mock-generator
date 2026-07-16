import os
import requests
from faker import Faker
from dotenv import load_dotenv
from faker.providers import DynamicProvider

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
base_url = os.getenv('BASE_URL')

## SPECIAL CONDITIONS FOR GENERATING DATA AND PROVIDERS
gender = ['male', 'female', 'other', 'unknown']
gender_probability = [0.45, 0.45, 0.05, 0.05]
gender_provider = DynamicProvider(
    provider_name="gender",
    elements=gender,
    weights=gender_probability
)

active = [True, False]
active_probability = [0.85, 0.15]
active_provider = DynamicProvider(
    provider_name="active",
    elements=active,
    weights=active_probability
)

telecom = ['phone', 'email']
telecom_provider = DynamicProvider(
    provider_name="telecom",
    elements=telecom,
    weights=[0.7, 0.3]
)

fake = Faker('pt_BR')
fake.add_provider(gender_provider)
fake.add_provider(active_provider)
fake.add_provider(telecom_provider)

def generate_telecom():
    telecom_type = fake.telecom()
    if telecom_type == 'phone':
        return {
            "system": "phone",
            "value": fake.phone_number(),
            "use": "mobile"
        }
    else:
        return {
            "system": "email",
            "value": fake.email(),
            "use": "home"
        }

def generate_patient_fhire(): 
  patient =  {
    "resourceType": "Patient",
    "name": [
      {
        "use": "official",
        "given": [fake.first_name(), fake.middle_name()],
        "family": fake.last_name()
      }
    ],
    "gender": fake.random_element(gender),
    "birthDate": fake.date_of_birth(minimum_age=1, maximum_age=100).strftime("%d-%m-%Y"),
    "active": fake.active(),
    "telecom": [
      generate_telecom()
    ],
    "address": [
      {
        "line": [fake.street_address()],
        "city": "São Paulo",
        "state": "SP",
        "postalCode": "01000-000"
      }
    ]
  }
  return patient

def authentication_medplum():
    token_url = f"{base_url}/oauth2/token"
    data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
    }
    response = requests.post(
        token_url,
        data=data
    )
    return response.json()["access_token"]

def generate_fake_data(token):
    patient = generate_patient_fhire()
    return patient

def main():
    try:
        print("Authenticating in medplum...")
        token = authentication_medplum()
        print("Authentication completed successfully!")
        
        print("Generating fake data...")
        fake_data = generate_fake_data(token)
        print("Fake data generated successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()