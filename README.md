# Medplum Fake Data Generator
A Python Script to generate data into Medplum FHIR server with synthetically generated patient data. 

## Features
- Generates Patient resources compatible with the HL7 FHIR standard. 
- Uses Faker Library to produce realistic names linked to gender, CPFs, Brazilian addresses, and mixed contact info. 
- Bundles multiple patients into a single FHIR Bundle (transaction) request for batch-mode seeding. 
