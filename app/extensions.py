"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: extensions.py
Purpose: Initialize Flask Extensions
----------------------------------------------------------
"""

from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# ==========================================================
# Flask Extension Instances
# ==========================================================

login_manager = LoginManager()
csrf = CSRFProtect()

# ==========================================================
# Login Configuration
# ==========================================================

login_manager.login_view = "auth_bp.login"
login_manager.login_message = "Please login to continue."
login_manager.login_message_category = "warning"

# ==========================================================
# Initialize Extensions
# ==========================================================

def init_extensions(app):
    """
    Initialize Flask extensions.
    """

    # ------------------------------------------------------
    # TEMPORARY:
    # CSRF disabled for testing.
    # Uncomment the next line after frontend forms are updated.
    # ------------------------------------------------------
    # csrf.init_app(app)

    login_manager.init_app(app)