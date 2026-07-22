import random
import requests
from typing import Callable
from config import BASE_URL, CLIENT_ID, CLIENT_SECRET, PROJECT_ID
from generators import generate_bundle, chunk_list

def authentication_medplum(session: requests.Session) -> str:
    token_url = f"{BASE_URL}/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": f"project/{PROJECT_ID}"
    }
    response = session.post(token_url, data=data, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

def get_random_patient(session: requests.Session, token: str) -> tuple[str, str]:
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/fhir+json"
    }

    patient_total = f"{BASE_URL}/fhir/R4/Patient?_summary=count"
    res_total = session.get(patient_total, headers=headers, timeout=30)
    res_total.raise_for_status()
    total_count = res_total.json().get("total", 0)

    if total_count == 0:
        raise Exception("Nenhum paciente encontrado na base.")

    random_id = random.randint(0, total_count - 1)
    search_id = f"{BASE_URL}/fhir/R4/Patient?_count=1&_offset={random_id}"
    res_patient = session.get(search_id, headers=headers, timeout=30)
    res_patient.raise_for_status()

    bundle = res_patient.json()
    entries = bundle.get("entry", [])

    if not entries:
        raise Exception("Erro ao recuperar paciente sorteado.")

    patient_resource = entries[0]["resource"]
    patient_id = patient_resource["id"]
    patient_list = patient_resource["name"][0].get("given", [])
    patient_name = patient_list[0]

    return patient_id, patient_name

def send_bundle(session: requests.Session, token: str, bundle: dict) -> dict:
    response = session.post(
        f"{BASE_URL}/fhir/R4",
        json=bundle,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/fhir+json",
            "accept": "application/fhir+json",
        },
        timeout=30
    )
    response.raise_for_status()
    return response.json()

def send_resources(
    session: requests.Session,
    token: str,
    resource_type: str,
    total_count: int,
    generator_fn: Callable,
    batch_size: int,
    requires_patient: bool = True
):
    resources = []
    
    for _ in range(total_count):
        try:
            if requires_patient:
                p_id, p_name = get_random_patient(session, token)
                res = generator_fn(p_id, p_name)
            else:
                res = generator_fn()
                
            resources.append(res)
        except Exception as e:
            print(f"Erro ao gerar {resource_type}: {e}")

    if not resources:
        print(f"Nenhum {resource_type} gerado para envio.")
        return

    for i, batch in enumerate(chunk_list(resources, batch_size), start=1):
        try:
            bundle = generate_bundle(batch, resource_type)
            send_bundle(session, token, bundle)
            print(f"Lote {i} de {resource_type} enviado com sucesso ({len(batch)} itens)!")
        except Exception as e:
            print(f"Erro ao enviar o lote {i} de {resource_type}: {e}")