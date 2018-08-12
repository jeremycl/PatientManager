import os
from datetime import date
from common.config import db, basedir
from models.db_model import Patient, PatientAttributes

# Data to initialize the db with
PATIENTS = [
    {'birthdate': date(2000, 1, 1), 'sex': 'M', 'last_name': 'Robert', 'first_name': 'Bob', 'email': 'bob@robert.com'},
    {'birthdate': date(1950, 2, 5), 'sex': 'F', 'last_name': 'Something', 'first_name': 'Linda', 'email': 'linda@gmail.com'}
]

# Delete db file if it already exists
dbPath = os.path.join(basedir, 'patient.db')
if os.path.exists(dbPath):
    os.remove(dbPath)

# Create db with tables
db.create_all()

# Add Patient and PatientAttributes records
for patient in PATIENTS:
    p = Patient()

    pAttributes = PatientAttributes(email=patient.get('email'), first_name=patient.get('first_name'),
                                    last_name=patient.get('last_name'), birthdate=patient.get('birthdate'),
                                    sex=patient.get('sex'), patient=p)

    db.session.add(pAttributes)

db.session.commit()
