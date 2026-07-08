"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: auth_routes.py
Purpose: Authentication Routes (Login/Register/Logout)
----------------------------------------------------------
"""

from flask import Blueprint, request, jsonify, render_template, redirect, url_for

from app.services.auth_service import AuthService
from app.services.security_service import SecurityService

from flask_login import current_user


auth_bp = Blueprint("auth_bp", __name__)


# ==========================================
# REGISTER
# ==========================================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    User registration route.
    """

    if request.method == "GET":
        return render_template("auth/register.html")

    data = request.form

    result = AuthService.register_user(
        full_name=data.get("full_name"),
        email=data.get("email"),
        password=data.get("password"),
        role=data.get("role"),
        phone=data.get("phone")
    )

    if result["success"]:
        return redirect(url_for("auth_bp.login"))

    return render_template(
        "auth/register.html",
        error=result["message"]
    )


# ==========================================
# LOGIN
# ==========================================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    User login route.
    """

    if request.method == "GET":
        return render_template("auth/login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    result = AuthService.login(email, password)

    if not result["success"]:
        return render_template(
            "auth/login.html",
            error=result["message"]
        )

    user = result["user"]

    # Role-based redirect
    if user.role == "Admin":
        return redirect("/admin/dashboard")

    elif user.role == "Counsellor":
        return redirect("/counsellor/dashboard")

    else:
        return redirect("/student/dashboard")


# ==========================================
# LOGOUT
# ==========================================
@auth_bp.route("/logout")
def logout():
    """
    Logout route.
    """

    AuthService.logout()

    return redirect(url_for("auth_bp.login"))


# ==========================================
# CURRENT USER API (for frontend)
# ==========================================
@auth_bp.route("/me")
def current_user_info():
    """
    Return logged-in user info.
    """

    if not current_user.is_authenticated:
        return jsonify({
            "authenticated": False
        })

    return jsonify({
        "authenticated": True,
        "user": {
            "id": current_user.get_id(),
            "role": current_user.role,
            "email": current_user.email
        }
    })