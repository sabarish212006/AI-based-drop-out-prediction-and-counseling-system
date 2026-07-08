"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: wsgi.py
Purpose: Production WSGI Entry Point
----------------------------------------------------------
"""

from app import create_app

app = create_app()

# Gunicorn will use: app:app