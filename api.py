import random
import requests
from config import BASE_URL, CLIENT_ID, CLIENT_SECRET, PROJECT_ID
from generators import generate_patient, generate_procedure, generate_bundle

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
    
    # Busca o primeiro nome com segurança
    patient_name = "Desconhecido"
    if "name" in patient_resource and len(patient_resource["name"]) > 0:
        given_list = patient_resource["name"][0].get("given", [])
        if given_list:
            patient_name = given_list[0]

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
            bundle = generate_bundle(patients, "Patient")
            send_bundle(session, token, bundle)
            print("10 Pacientes enviados!")
        except Exception as e:
            print(f"Erro ao enviar pacientes: {e}")

        procedures = []
        for _ in range(2):
            try:
                p_id, p_name = get_random_patient(session, token)
                print(f"Sorteado: {p_name} ({p_id})")
                proc = generate_procedure(p_id, p_name)
                procedures.append(proc)
            except Exception as e:
                print(f"Erro ao sortear paciente: {e}")

        if procedures:
            proc_bundle = generate_bundle(procedures, "Procedure")
            send_bundle(session, token, proc_bundle)
            print("Procedures enviadas com sucesso!")


if __name__ == "__main__":
    main()