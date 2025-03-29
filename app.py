from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from models import db, Patient, Treatment
from ai_agent import DentalAIAgent
from datetime import datetime
import os
from dotenv import load_dotenv
import re

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
database_url = os.getenv('DATABASE_URL', 'sqlite:///dental.db')
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize database
db.init_app(app)

# Initialize AI agent
ai_agent = DentalAIAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/patients', methods=['GET'])
def get_patients():
    try:
        patients = Patient.query.all()
        return jsonify([patient.to_dict() for patient in patients])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    try:
        patient = Patient.query.get_or_404(patient_id)
        return jsonify(patient.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>/risk', methods=['GET'])
def get_patient_risk(patient_id):
    try:
        patient = Patient.query.get_or_404(patient_id)
        risk_analysis = ai_agent.analyze_patient_risk(patient.to_dict())
        return jsonify({'risk_analysis': risk_analysis})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients/<int:patient_id>/reminder', methods=['GET'])
def get_patient_reminder(patient_id):
    try:
        patient = Patient.query.get_or_404(patient_id)
        reminder = ai_agent.generate_follow_up_reminder(patient.to_dict())
        return jsonify({'reminder': reminder})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patients', methods=['POST'])
def add_patient():
    try:
        data = request.json
        new_patient = Patient(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            last_visit=datetime.fromisoformat(data['last_visit']) if data.get('last_visit') else None,
            next_visit=datetime.fromisoformat(data['next_visit']) if data.get('next_visit') else None,
            treatment_status=data.get('treatment_status'),
            notes=data.get('notes')
        )
        db.session.add(new_patient)
        db.session.commit()
        return jsonify(new_patient.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/treatments', methods=['POST'])
def add_treatment():
    try:
        data = request.json
        new_treatment = Treatment(
            patient_id=data['patient_id'],
            treatment_type=data['treatment_type'],
            date=datetime.fromisoformat(data['date']),
            status=data.get('status'),
            complications=data.get('complications'),
            next_follow_up=datetime.fromisoformat(data['next_follow_up']) if data.get('next_follow_up') else None
        )
        db.session.add(new_treatment)
        db.session.commit()
        return jsonify(new_treatment.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 