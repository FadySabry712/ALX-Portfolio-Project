from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    last_visit = db.Column(db.DateTime, default=datetime.utcnow)
    next_visit = db.Column(db.DateTime)
    treatment_status = db.Column(db.String(50))
    risk_level = db.Column(db.String(20))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'last_visit': self.last_visit.isoformat() if self.last_visit else None,
            'next_visit': self.next_visit.isoformat() if self.next_visit else None,
            'treatment_status': self.treatment_status,
            'risk_level': self.risk_level,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        }

class Treatment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    treatment_type = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50))
    complications = db.Column(db.Text)
    next_follow_up = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'treatment_type': self.treatment_type,
            'date': self.date.isoformat(),
            'status': self.status,
            'complications': self.complications,
            'next_follow_up': self.next_follow_up.isoformat() if self.next_follow_up else None,
            'created_at': self.created_at.isoformat()
        } 