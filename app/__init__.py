"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: __init__.py
Purpose: Flask Application Factory
----------------------------------------------------------
"""

from flask import Flask, redirect, url_for

from app.config import Config
from app.extensions import init_extensions, login_manager

# Error Handlers
from app.routes.error_handlers import register_error_handlers

# Blueprints
from app.routes.auth_routes import auth_bp
from app.routes.student_routes import student_bp
from app.routes.admin_routes import admin_bp
from app.routes.counsellor_routes import counsellor_bp
from app.routes.api_routes import api_bp

# Models
from app.models.user_model import UserModel
from app.models.user import User
from app.services.prediction_service import dropout_predictionservice


# ==========================================================
# Flask-Login User Loader
# ==========================================================

@login_manager.user_loader
def load_user(user_id):
    """
    Load user for Flask-Login.
    """

    user_data = UserModel.get_user_by_id(user_id)

    if user_data:
        return User(user_data)

    return None


# ==========================================================
# Application Factory
# ==========================================================

def create_app():
    """
    Create Flask application.
    """

    app = Flask(__name__)

    # Load Config
    app.config.from_object(Config)

    # Initialize Extensions
    init_extensions(app)

    # ======================================================
    # Home Route
    # ======================================================
    @app.route("/")
    def home():
        return redirect(url_for("auth_bp.login"))

    # ======================================================
    # Register Blueprints
    # ======================================================
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(counsellor_bp)
    app.register_blueprint(api_bp)

    # ======================================================
    # Print Registered Routes (Debug)
    # ======================================================
    print("\n========== REGISTERED ROUTES ==========")

    for rule in app.url_map.iter_rules():
        print(rule)

    print("=======================================\n")

    # ======================================================
    # Register Error Handlers
    # ======================================================
    register_error_handlers(app)

    return app