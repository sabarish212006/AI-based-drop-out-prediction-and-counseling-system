"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: config.py
Purpose: Centralized Application Configuration
----------------------------------------------------------
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# --------------------------------------------------------
# Load Environment Variables
# --------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Config:
    """
    Base configuration class for the application.
    """

    # --------------------------------------------------------
    # General
    # --------------------------------------------------------

    APP_NAME = os.getenv(
        "APP_NAME",
        "AI-Based Dropout Prediction and Counselling System"
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "ChangeThisSecretKey"
    )

    DEBUG = os.getenv(
        "DEBUG",
        "False"
    ).lower() == "true"

    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------

    DB_HOST = os.getenv("DB_HOST", "localhost")

    DB_PORT = int(
        os.getenv("DB_PORT", 3306)
    )

    DB_NAME = os.getenv(
        "DB_NAME",
        "dropout_prediction_db"
    )

    DB_USER = os.getenv(
        "DB_USER",
        "root"
    )

    DB_PASSWORD = os.getenv(
        "DB_PASSWORD",
        ""
    )

    # --------------------------------------------------------
    # Uploads
    # --------------------------------------------------------

    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        "app/static/uploads"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024      # 5 MB

    ALLOWED_IMAGE_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg"
    }

    ALLOWED_DOCUMENT_EXTENSIONS = {
        "pdf",
        "doc",
        "docx"
    }

    # --------------------------------------------------------
    # Machine Learning
    # --------------------------------------------------------

    MODEL_VERSION = os.getenv(
        "MODEL_VERSION",
        "v1"
    )

    MODEL_PATH = os.getenv(
        "MODEL_PATH",
        "app/ml/saved_models/versions/v1"
    )

    # --------------------------------------------------------
    # Logging
    # --------------------------------------------------------

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    LOG_FILE = os.getenv(
        "LOG_FILE",
        "logs/app.log"
    )

    # --------------------------------------------------------
    # Session
    # --------------------------------------------------------

    SESSION_TIMEOUT = int(
        os.getenv(
            "SESSION_TIMEOUT",
            30
        )
    )

    PERMANENT_SESSION_LIFETIME = SESSION_TIMEOUT * 60

    # --------------------------------------------------------
    # Security
    # --------------------------------------------------------

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Enable HTTPS cookie automatically in production
    SESSION_COOKIE_SECURE = not DEBUG