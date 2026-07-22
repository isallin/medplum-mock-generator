import random
from datetime import date, timezone, timedelta
from faker import Faker
import config

fake = Faker("pt_BR")

def draw(elements, weights):
    return random.choices(elements, weights=weights, k=1)[0]

def chunk_list(data: list, size: int):
    for i in range(0, len(data), size):
        yield data[i:i + size]

def generate_bundle(resources: list, resource_type: str) -> dict:
    bundle = {"resourceType": "Bundle", "type": "transaction", "entry": []}
    for res in resources:
        entry = {
            "resource": res,
            "request": {"method": "POST", "url": resource_type}
        }
        bundle["entry"].append(entry)
    return bundle

def generate_patient() -> dict:
    selected_gender = draw(config.GENDER_ELEMENTS, config.GENDER_WEIGHTS)
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

    if random.random() < config.P_EXHIGH:
        patient["gender"] = selected_gender

    patient_birth = None
    if random.random() < config.P_EXHIGH:
        patient_birth = fake.date_of_birth(minimum_age=1, maximum_age=100)
        patient["birthDate"] = patient_birth.isoformat()

    if random.random() < config.P_EXHIGH:
        patient["active"] = random.random() < config.P_EXHIGH

    if random.random() < config.P_HIGH:
        if random.random() < config.P_HIGH:
            patient["telecom"] = [{"system": "phone", "value": fake.phone_number(), "use": "mobile"}]
        else:
            patient["telecom"] = [{"system": "email", "value": fake.email(), "use": "home"}]

    if random.random() < config.P_MID:
        patient["address"] = [{
            "use": "home",
            "line": [fake.street_address()],
            "city": fake.city(),
            "state": "GO",
            "postalCode": fake.postcode(),
            "country": "BR",
        }]

    if random.random() < config.P_MID:
        patient["identifier"] = [{
            "use": "official",
            "system": "http://saude.goias.gov/cpf",
            "value": fake.cpf(),
        }]

    if random.random() < config.P_HIGH:
        if random.random() < config.P_EXLOW:
            if patient_birth:
                if random.random() < config.P_MID:
                    dt_morte = fake.date_between_dates(date_start=patient_birth, date_end=date.today())
                    patient["deceasedDateTime"] = dt_morte.isoformat()
                else:
                    patient["deceasedBoolean"] = True
            else:
                dt_morte = fake.date_between(start_date="-50y", end_date=date.today())
                patient["deceasedDateTime"] = dt_morte.isoformat()
        else:
            patient["deceasedBoolean"] = False

    if random.random() < config.P_EXLOW:
        if random.random() < config.P_MID:
            patient["multipleBirthBoolean"] = True
        else:
            patient["multipleBirthInteger"] = random.randint(2, 5)

    minimal_age = date.today().replace(year=date.today().year - 18)
    if patient_birth and patient_birth <= minimal_age and random.random() < config.P_HIGH:
        mrt = draw(config.MARITAGE_ELEMENTS, config.MARITAGE_WEIGHTS)
        patient["maritalStatus"] = {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/v3-MaritalStatus",
                "code": mrt["code"],
                "display": mrt["display"]
            }]
        }

    return patient

def generate_procedure(patient_id: str, patient_name: str) -> dict:
    selected_code = random.choice(config.SNOMED_PROCEDURES)
    
    procedure = {
        "resourceType": "Procedure",
        "status": draw(config.PROCEDURE_STAT, config.PROCEDURE_STAT_WEIGHTS),
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

    if random.random() < config.P_EXHIGH:
        procedure["identifier"] = [{
            "use": "official",
            "system": "http://saude.goias.gov/procedimentos",
            "value": fake.numerify("########")
        }]

    if random.random() < config.P_HIGH:
        category = random.choice(config.PROCEDURE_CATEGORIES)
        procedure["category"] = {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": category["code"],
                "display": category["display"]
            }]
        }

    if random.random() < config.P_EXHIGH:
        dt_performed = fake.date_time_between(start_date="-2y", end_date="now", tzinfo=timezone.utc)
        procedure["performedDateTime"] = dt_performed.isoformat()

    if random.random() < config.P_HIGH:
        reason = random.choice(config.PROCEDURE_REASON_CODES)
        procedure["reasonCode"] = [{
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": reason["code"],
                "display": reason["display"]
            }]
        }]

    if random.random() < config.P_MID:
        procedure["location"] = {
            "display": f"Hospital {fake.company()}"
        }

    if random.random() < config.P_LOW:
        procedure["note"] = [{
            "text": fake.sentence(nb_words=20)
        }]

    return procedure

def generate_observation(patient_id: str, patient_name: str) -> dict:
    obs_type = random.choice(config.LOINC_OBSERVATIONS)

    if obs_type["type"] == "float":
        val = round(random.uniform(obs_type["min"], obs_type["max"]), 1)
    else:
        val = random.randint(obs_type["min"], obs_type["max"])

    observation = {
        "resourceType": "Observation",
        "status": draw(config.OBSERVATION_STAT, config.OBSERVATION_STAT_WEIGHTS),
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": obs_type["category"],
                "display": obs_type["category"].capitalize()
            }]
        }],
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": obs_type["code"],
                "display": obs_type["display"]
            }]
        },
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": patient_name
        },
        "valueQuantity": {
            "value": val,
            "unit": obs_type["unit"],
            "system": "http://unitsofmeasure.org",
            "code": obs_type["ucum"]
        }
    }

    if random.random() < config.P_EXHIGH:
        observation["identifier"] = [{
            "use": "official",
            "system": "http://saude.goias.gov/observacoes",
            "value": fake.numerify("########")
        }]

    if random.random() < config.P_EXHIGH:
        dt_effective = fake.date_time_between(start_date="-6m", end_date="now", tzinfo=timezone.utc)
        observation["effectiveDateTime"] = dt_effective.isoformat()

    if random.random() < config.P_HIGH:
        dt_issued = fake.date_time_between(start_date="-1y", end_date="now", tzinfo=timezone.utc)
        observation["issued"] = dt_issued.isoformat()

    if random.random() < config.P_MID:
        observation["note"] = [{
            "text": fake.sentence(nb_words=15)
        }]

    return observation

def generate_medication() -> dict:
    med_item = random.choice(config.MEDICATION_RXNORM)

    medication = {
        "resourceType": "Medication",
        "status": draw(config.MEDICATION_STAT, config.MEDICATION_STAT_WEIGHTS),
        "code": {
            "coding": [{
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": med_item["code"],
                "display": med_item["display"]
            }]
        }
    }

    if random.random() < config.P_EXHIGH:
        medication["identifier"] = [{
            "use": "official",
            "system": "http://saude.goias.gov/medicamentos",
            "value": fake.numerify("########")
        }]

    if random.random() < config.P_HIGH:
        form_info = next(
            (f for f in config.MEDICATION_FORMS if f["code"] == med_item["form_code"]),
            {"code": "385055001", "display": "Tablet"}
        )
        medication["form"] = {
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": form_info["code"],
                "display": form_info["display"]
            }]
        }

    if random.random() < config.P_HIGH:
        medication["batch"] = {
            "lotNumber": fake.bothify(text="LOT-####-??").upper(),
            "expirationDate": fake.date_between(start_date="+6m", end_date="+3y").isoformat()
        }

    if random.random() < config.P_HIGH:
        medication["manufacturer"] = {
            "display": f"Laboratório {fake.company()} S.A."
        }

    return medication

def generate_medication_request(patient_id: str, patient_name: str) -> dict:
    med_item = random.choice(config.MEDICATION_RXNORM)
    category = random.choice(config.MED_REQUEST_CATEGORIES)

    med_request = {
        "resourceType": "MedicationRequest",
        "status": draw(config.MED_REQUEST_STATUS, config.MED_REQUEST_STATUS_WEIGHTS),
        "intent": draw(config.MED_REQUEST_INTENT, config.MED_REQUEST_INTENT_WEIGHTS),
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/medicationrequest-category",
                "code": category["code"],
                "display": category["display"]
            }]
        }],
        "medicationCodeableConcept": {
            "coding": [{
                "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                "code": med_item["code"],
                "display": med_item["display"]
            }]
        },
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": patient_name
        }
    }

    if random.random() < config.P_EXHIGH:
        med_request["identifier"] = [{
            "use": "official",
            "system": "http://saude.goias.gov/prescricoes",
            "value": fake.numerify("########")
        }]

    if random.random() < config.P_EXHIGH:
        dt_authored = fake.date_time_between(start_date="-1y", end_date="now", tzinfo=timezone.utc)
        med_request["authoredOn"] = dt_authored.isoformat()

    if random.random() < config.P_HIGH:
        med_request["requester"] = {
            "display": f"Dr(a). {fake.name()}"
        }

    if random.random() < config.P_HIGH:
        med_request["dosageInstruction"] = [{
            "text": random.choice([
                "Tomar 1 comprimido de 8 em 8 horas por 7 dias.",
                "Tomar 1 cápsula ao dia pela manhã.",
                "Aplicar ou ingerir conforme orientação médica se houver dor.",
                "Tomar 1 comprimido de 12 em 12 horas."
            ])
        }]

    if random.random() < config.P_LOW:
        med_request["note"] = [{
            "text": fake.sentence(nb_words=12)
        }]

    return med_request

def generate_appointment(patient_id: str, patient_name: str) -> dict:
    service_type = random.choice(config.APPOINTMENT_SERVICE_TYPES)
    
    # Início e término da consulta
    start_dt = fake.date_time_between(start_date="-3m", end_date="+3m", tzinfo=timezone.utc)
    duration_minutes = random.choice([15, 30, 45, 60])
    end_dt = start_dt + timedelta(minutes=duration_minutes)

    # Estrutura base
    appointment = {
        "resourceType": "Appointment",
        "status": draw(config.APPOINTMENT_STAT, config.APPOINTMENT_STAT_WEIGHTS),
        "serviceType": [{
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": service_type["code"],
                "display": service_type["display"]
            }]
        }],
        "start": start_dt.isoformat(),
        "end": end_dt.isoformat(),
        "minutesDuration": duration_minutes,
        "participant": [
            {
                "actor": {
                    "reference": f"Patient/{patient_id}",
                    "display": patient_name
                },
                "status": "accepted"
            }
        ]
    }

    if random.random() < config.P_EXHIGH:
        appointment["identifier"] = [{
            "use": "official",
            "system": "http://saude.goias.gov/agendamentos",
            "value": fake.numerify("########")
        }]

    # Profissional
    if random.random() < config.P_HIGH:
        appointment["participant"].append({
            "actor": {
                "display": f"Dr(a). {fake.name()}"
            },
            "status": "accepted"
        })

    # Motivo do agendamento
    if random.random() < config.P_MID:
        appointment["description"] = f"Consulta de {service_type['display']}"

    # Anotações
    if random.random() < config.P_LOW:
        appointment["comment"] = fake.sentence(nb_words=10)

    return appointment

def generate_encounter(patient_id: str, patient_name: str) -> dict:
    enc_class = random.choice(config.ENCOUNTER_CLASSES)
    enc_type = random.choice(config.ENCOUNTER_TYPES)
    
    # Início e término do atendimento
    start_dt = fake.date_time_between(start_date="-6m", end_date="now", tzinfo=timezone.utc)
    duration_minutes = random.choice([20, 30, 45, 60, 120])
    end_dt = start_dt + timedelta(minutes=duration_minutes)

    # Estrutura base
    encounter = {
        "resourceType": "Encounter",
        "status": draw(config.ENCOUNTER_STAT, config.ENCOUNTER_STAT_WEIGHTS),
        "class": {
            "system": "http://terminology.hl7.org/CodeSystem/v3-ActCode",
            "code": enc_class["code"],
            "display": enc_class["display"]
        },
        "type": [{
            "coding": [{
                "system": "http://snomed.info/sct",
                "code": enc_type["code"],
                "display": enc_type["display"]
            }]
        }],
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": patient_name
        },
        "period": {
            "start": start_dt.isoformat(),
            "end": end_dt.isoformat()
        }
    }

    if random.random() < config.P_EXHIGH:
        encounter["identifier"] = [{
            "use": "official",
            "system": "http://saude.goias.gov/atendimentos",
            "value": fake.numerify("########")
        }]

    # Profissional
    if random.random() < config.P_HIGH:
        encounter["participant"] = [{
            "individual": {
                "display": f"Dr(a). {fake.name()}"
            }
        }]

    # Local
    if random.random() < config.P_MID:
        encounter["location"] = [{
            "location": {
                "display": f"Consultório {random.randint(1, 20)} - Hospital {fake.company()}"
            }
        }]

    return encounter

def generate_condition(patient_id: str, patient_name: str) -> dict:
    cond_item = random.choice(config.ICD10_CONDITIONS)
    category = random.choice(config.CONDITION_CATEGORIES)
    
    # Estrutura base
    condition = {
        "resourceType": "Condition",
        "clinicalStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                "code": draw(config.CONDITION_CLINICAL_STATUS, config.CONDITION_CLINICAL_STATUS_WEIGHTS)
            }]
        },
        "verificationStatus": {
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                "code": draw(config.CONDITION_VERIFICATION_STATUS, config.CONDITION_VERIFICATION_STATUS_WEIGHTS)
            }]
        },
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/condition-category",
                "code": category["code"],
                "display": category["display"]
            }]
        }],
        "code": {
            "coding": [
                {
                    "system": "http://hl7.org/fhir/sid/icd-10",
                    "code": cond_item["code"],
                    "display": cond_item["display"]
                },
                {
                    "system": "http://snomed.info/sct",
                    "code": cond_item["snomed_code"],
                    "display": cond_item["display"]
                }
            ]
        },
        "subject": {
            "reference": f"Patient/{patient_id}",
            "display": patient_name
        }
    }

    if random.random() < config.P_EXHIGH:
        condition["identifier"] = [{
            "use": "official",
            "system": "http://saude.goias.gov/diagnosticos",
            "value": fake.numerify("########")
        }]

    # Data diagnóstico
    if random.random() < config.P_EXHIGH:
        dt_onset = fake.date_time_between(start_date="-5y", end_date="now", tzinfo=timezone.utc)
        condition["onsetDateTime"] = dt_onset.isoformat()

    # Data registro
    if random.random() < config.P_HIGH:
        dt_recorded = fake.date_time_between(start_date="-2y", end_date="now", tzinfo=timezone.utc)
        condition["recordedDate"] = dt_recorded.isoformat()

    # Profissional/médico
    if random.random() < config.P_MID:
        condition["recorder"] = {
            "display": f"Dr(a). {fake.name()}"
        }

    # Anotações
    if random.random() < config.P_LOW:
        condition["note"] = [{
            "text": fake.sentence(nb_words=12)
        }]

    return condition