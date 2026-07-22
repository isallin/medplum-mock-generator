import requests
import generators
from api import authentication_medplum, send_resources

def main():
    with requests.Session() as session:
        try:
            print("Autenticando no Medplum...")
            token = authentication_medplum(session)
        except Exception as e:
            print(f"Falha ao autenticar: {e}")
            return

        BATCH_SIZE = 50
        TOTAL_PATIENTS = 10
        TOTAL_PROCEDURES = 10
        TOTAL_OBSERVATIONS = 10
        TOTAL_MEDICATIONS = 10
        TOTAL_MEDICATION_REQUESTS = 10
        TOTAL_APPOINTMENTS = 10
        TOTAL_ENCOUNTERS = 10
        TOTAL_CONDITIONS = 10

        send_resources(
            session=session,
            token=token,
            resource_type="Patient",
            total_count=TOTAL_PATIENTS,
            generator_fn=generators.generate_patient,
            batch_size=BATCH_SIZE,
            requires_patient=False
        )

        send_resources(
            session=session,
            token=token,
            resource_type="Procedure",
            total_count=TOTAL_PROCEDURES,
            generator_fn=generators.generate_procedure,
            batch_size=BATCH_SIZE,
            requires_patient=True
        )

        send_resources(
            session=session,
            token=token,
            resource_type="Observation",
            total_count=TOTAL_OBSERVATIONS,
            generator_fn=generators.generate_observation,
            batch_size=BATCH_SIZE,
            requires_patient=True
        )

        send_resources(
            session=session,
            token=token,
            resource_type="Medication",
            total_count=TOTAL_MEDICATIONS,
            generator_fn=generators.generate_medication,
            batch_size=BATCH_SIZE,
            requires_patient=False
        )

        send_resources(
            session=session,
            token=token,
            resource_type="MedicationRequest",
            total_count=TOTAL_MEDICATION_REQUESTS,
            generator_fn=generators.generate_medication_request,
            batch_size=BATCH_SIZE,
            requires_patient=True
        )

        send_resources(
            session=session,
            token=token,
            resource_type="Appointment",
            total_count=TOTAL_APPOINTMENTS,
            generator_fn=generators.generate_appointment,
            batch_size=BATCH_SIZE,
            requires_patient=True
        )

        send_resources(
            session=session,
            token=token,
            resource_type="Encounter",
            total_count=TOTAL_ENCOUNTERS,
            generator_fn=generators.generate_encounter,
            batch_size=BATCH_SIZE,
            requires_patient=True
        )

        send_resources(
            session=session,
            token=token,
            resource_type="Condition",
            total_count=TOTAL_CONDITIONS,
            generator_fn=generators.generate_condition,
            batch_size=BATCH_SIZE,
            requires_patient=True
        )

if __name__ == "__main__":
    main()