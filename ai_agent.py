from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class DentalAIAgent:
    def __init__(self):
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                temperature=0.7,
                google_api_key=os.getenv('GOOGLE_API_KEY')
            )
            self.complication_prompt = PromptTemplate(
                input_variables=["treatment_type", "days_since_visit"],
                template="""
                As a dental AI assistant, analyze the potential complications for a patient who had {treatment_type} 
                {days_since_visit} days ago and hasn't returned for follow-up. Consider:
                1. Immediate risks
                2. Long-term consequences
                3. Recommended action timeline
                
                Provide a concise but comprehensive assessment.
                """
            )
            self.chain = LLMChain(llm=self.llm, prompt=self.complication_prompt)
        except Exception as e:
            print(f"Error initializing AI agent: {str(e)}")
            self.llm = None
            self.chain = None

    def analyze_patient_risk(self, patient_data):
        """Analyze patient risk based on their treatment history and follow-up status."""
        if not self.chain:
            return "AI agent not properly initialized. Please check your Google API key."

        if not patient_data.get('last_visit'):
            return "No previous visit data available"

        try:
            days_since_visit = (datetime.now() - datetime.fromisoformat(patient_data['last_visit'])).days
            treatment_type = patient_data.get('treatment_status', 'general checkup')

            analysis = self.chain.run(
                treatment_type=treatment_type,
                days_since_visit=days_since_visit
            )
            return analysis
        except Exception as e:
            return f"Error analyzing patient risk: {str(e)}"

    def get_risk_level(self, days_since_visit, treatment_type):
        """Determine risk level based on time since last visit and treatment type."""
        if days_since_visit <= 30:
            return "Low"
        elif days_since_visit <= 90:
            return "Medium"
        else:
            return "High"

    def generate_follow_up_reminder(self, patient_data):
        """Generate a personalized follow-up reminder message."""
        if not patient_data.get('last_visit'):
            return "No previous visit data available"

        try:
            days_since_visit = (datetime.now() - datetime.fromisoformat(patient_data['last_visit'])).days
            risk_level = self.get_risk_level(days_since_visit, patient_data.get('treatment_status'))

            reminder = f"""
            Patient: {patient_data['name']}
            Last Visit: {patient_data['last_visit']}
            Days Since Visit: {days_since_visit}
            Risk Level: {risk_level}
            Treatment Status: {patient_data.get('treatment_status', 'Not specified')}
            
            Recommended Action: Schedule a follow-up appointment as soon as possible.
            """
            return reminder
        except Exception as e:
            return f"Error generating reminder: {str(e)}" 