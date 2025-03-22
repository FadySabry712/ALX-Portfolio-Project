# AI Retention Agent for Dental Clinics

An AI-powered system that helps dental clinics identify patients who haven't returned for follow-up care and highlights potential complications if left untreated.

## Features

- Patient tracking and follow-up monitoring
- AI-powered complication prediction
- Simple web interface for staff
- Patient history visualization

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file with:
```
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///dental.db
```

4. Run the application:
```bash
flask run
```

## Project Structure

- `app.py`: Main Flask application
- `models.py`: Database models
- `ai_agent.py`: AI agent implementation
- `static/`: Frontend assets
- `templates/`: HTML templates

## Team

- Fady Sabry: Backend Engineer
- Abdelrahman Youssif: Frontend Engineer 