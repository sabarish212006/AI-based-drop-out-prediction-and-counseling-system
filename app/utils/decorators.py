"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: decorators.py
Purpose: Authentication & Authorization Decorators
----------------------------------------------------------
"""

from functools import wraps

from flask import flash
from flask import redirect
from flask import session
from flask import url_for


def login_required(view_function):
    """
    Ensures the user is logged in before accessing a route.
    """

    @wraps(view_function)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:
            flash("Please login to continue.", "warning")
            return redirect(url_for("auth.login"))

        return view_function(*args, **kwargs)

    return wrapper


def role_required(*allowed_roles):
    """
    Restrict route access based on user role.

    Example:
        @role_required("Admin")
        @role_required("Student")
        @role_required("Counsellor")
        @role_required("Admin", "Counsellor")
    """

    def decorator(view_function):

        @wraps(view_function)
        def wrapper(*args, **kwargs):

            if "user_id" not in session:
                flash("Please login to continue.", "warning")
                return redirect(url_for("auth.login"))

            user_role = session.get("role")

            if user_role not in allowed_roles:
                flash("You are not authorized to access this page.", "danger")
                return redirect(url_for("auth.login"))

            return view_function(*args, **kwargs)

        return wrapper

    return decorator


def admin_required(view_function):
    """
    Shortcut decorator for Admin only.
    """

    return role_required("Admin")(view_function)


def student_required(view_function):
    """
    Shortcut decorator for Student only.
    """

    return role_required("Student")(view_function)


def counsellor_required(view_function):
    """
    Shortcut decorator for Counsellor only.
    """

    return role_required("Counsellor")(view_function)