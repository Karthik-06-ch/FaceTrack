# Setup Guide

## Environment Preparation
It is highly recommended to use a Python virtual environment.
1. `python -m venv venv`
2. `source venv/bin/activate` (Linux/Mac) OR `venv\Scripts\activate` (Windows)
3. `pip install -r requirements.txt`

## First-time DB Initialization
The database self-initializes on the first run. For dummy data to test the dashboard right away:
```bash
python -m database.seed_data
```

## Running the Application
Launch the Streamlit Dashboard:
```bash
streamlit run dashboard/app.py
```
