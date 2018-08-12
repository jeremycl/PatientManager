from common.config import db

class Patient(db.Model):
    __tablename__ = 'patient'

    id = db.Column(db.Integer, primary_key=True)
    attributes = db.relationship('PatientAttributes', uselist=False, back_populates='patient')

class PatientAttributes(db.Model):
    __tablename__ = 'patient_attributes'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(64))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    birthdate = db.Column(db.Date, default=None)
    sex = db.Column(db.String(1))

    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    patient = db.relationship('Patient', back_populates='attributes')

    def __init__(self, email, first_name, last_name, birthdate, sex, patient):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.sex = sex
        self.patient = patient

    @property
    def serialize(self):
        return {
            'attributes': {
                    'birthdate': self.birthdate,
                    'email': self.email,
                    'first_name': self.first_name,
                    'last_name': self.last_name,
                    'sex': self.sex
            }
        }

