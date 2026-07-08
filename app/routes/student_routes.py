"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: student_routes.py
Purpose: Student Portal Routes
----------------------------------------------------------
"""

from flask import Blueprint, request, render_template, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user

from app.models.student_model import StudentModel
from app.services.academic_service import AcademicService
from app.services.notification_service import NotificationService
from app.services.auth_service import AuthService
from app.services.prediction_service import dropout_predictionservice

student_bp = Blueprint("student_bp", __name__)

# ==========================================
# STUDENT DASHBOARD
# ==========================================
@student_bp.route("/student/dashboard")
@login_required
def dashboard():
    """
    Student dashboard page.
    """

    user_id = int(current_user.get_id())

    # Fetch combined user+student profile
    user_profile = AuthService.get_user_profile(user_id)

    academic_records = []
    latest_record = None
    prediction = None
    prediction_history = []

    if user_profile and user_profile.get("student_id"):
        student_id = user_profile["student_id"]

        academic_records = AcademicService.get_student_records(student_id)

        latest_record = AcademicService.get_latest_record(student_id)

        # Try to get latest saved prediction from DB first
        latest_saved = dropout_predictionservice.get_latest_prediction_db(student_id)

        if latest_saved:
            # Normalize DB prediction fields for template rendering
            latest_saved["score"] = latest_saved.get("dropout_probability")
            latest_saved["suggestion"] = latest_saved.get("explanation") or latest_saved.get("suggestion")
            latest_saved["message"] = latest_saved.get("message") or "Saved AI prediction"
            prediction = latest_saved
        else:
            # fall back to live ML prediction
            prediction = dropout_predictionservice.predict_dropout(student_id)

        # Prediction history from DB
        prediction_history = dropout_predictionservice.get_prediction_history(student_id)

    notifications = NotificationService.get_user_notifications(user_id)

    return render_template(
        "student/dashboard.html",
        user=user_profile,
        academic_records=academic_records,
        latest_record=latest_record,
        notifications=notifications,
        prediction=prediction,
        prediction_history=prediction_history
    )


# ==========================================
# STUDENT PROFILE
# ==========================================
@student_bp.route("/student/profile")
@login_required
def profile():
    """
    Student profile page.
    """

    user_id = current_user.get_id()

    user = AuthService.get_user_profile(user_id)

    return render_template(
        "student/profile.html",
        user=user
    )


# ==========================================
# PREDICTION HISTORY PAGE
# ==========================================
@student_bp.route("/student/predictions")
@login_required
def predictions_page():
    user_id = int(current_user.get_id())

    user_profile = AuthService.get_user_profile(user_id)

    if not user_profile or not user_profile.get("student_id"):
        return render_template("student/prediction_history.html", predictions=[])

    student_id = user_profile["student_id"]

    predictions = dropout_predictionservice.get_prediction_history(student_id)

    return render_template("student/prediction_history.html", predictions=predictions, user=user_profile)


# ==========================================
# ACADEMIC HISTORY PAGE
# ==========================================
@student_bp.route("/student/academic/history")
@login_required
def academic_history_page():
    user_id = int(current_user.get_id())

    user_profile = AuthService.get_user_profile(user_id)

    if not user_profile or not user_profile.get("student_id"):
        return render_template("student/academic_history.html", records=[])

    student_id = user_profile["student_id"]

    records = AcademicService.get_student_records(student_id)

    return render_template("student/academic_history.html", records=records, user=user_profile)


# ==========================================
# ADD ACADEMIC RECORD
# ==========================================
@student_bp.route("/student/academic/add", methods=["GET", "POST"])
@login_required
def add_academic():
    """
    Add academic record for student.
    """

    user_id = int(current_user.get_id())

    student = StudentModel.get_student_by_user_id(user_id)

    if not student:
        flash("Student profile not found.", "danger")
        return redirect(url_for("student_bp.dashboard"))

    student_id = student["student_id"]

    if request.method == "GET":
        # Pass student's year_of_study to the template for semester validation
        return render_template(
            "student/academic_form.html",
            student_year=student.get("year_of_study"),
            student=student
        )

    data = request.form

    result = AcademicService.add_academic_record(
        student_id=student_id,
        semester=int(data.get("semester")),
        cgpa=float(data.get("cgpa")),
        attendance=float(data.get("attendance")),
        internal_marks=float(data.get("internal_marks")),
        backlog_count=int(data.get("backlog_count")),
        study_hours=float(data.get("study_hours")),
        year_of_study=student.get("year_of_study")
    )

    if result.get("success"):
        flash("✅ Academic Record Saved Successfully.", "success")
    else:
        flash(result.get("message", "Failed to save record."), "danger")

    return redirect(url_for("student_bp.dashboard"))
# ==========================================
# UPDATE ACADEMIC RECORD
# ==========================================
@student_bp.route("/student/academic/update", methods=["POST"])
@login_required
def update_academic():
    """
    Update academic record.
    """

    data = request.form

    result = AcademicService.update_academic_record(
        academic_id=int(data.get("academic_id")),
        semester=int(data.get("semester")),
        cgpa=float(data.get("cgpa")),
        attendance=float(data.get("attendance")),
        internal_marks=float(data.get("internal_marks")),
        backlog_count=int(data.get("backlog_count")),
        study_hours=float(data.get("study_hours"))
    )

    return jsonify(result)


# ==========================================
# DELETE ACADEMIC RECORD
# ==========================================
@student_bp.route("/student/academic/delete", methods=["POST"])
@login_required
def delete_academic():
    """
    Delete academic record.
    """

    academic_id = int(request.form.get("academic_id"))

    result = AcademicService.delete_academic_record(academic_id)

    return jsonify(result)


# ==========================================
# STUDENT SUMMARY PAGE (HTML)
# ==========================================
@student_bp.route("/student/summary")
@login_required
def student_summary_page():
    """
    Render a user-friendly academic summary page with AI prediction.
    """
    user_id = int(current_user.get_id())
    user_profile = AuthService.get_user_profile(user_id)

    if not user_profile or not user_profile.get("student_id"):
        return render_template("student/academic_summary.html", error="Student profile not found.", student=None, academic_data=None, prediction=None, academic_history=[])

    student_id = user_profile["student_id"]
    student = StudentModel.get_student_by_user_id(user_id)

    summary = AcademicService.get_student_summary(student_id)
    prediction = dropout_predictionservice.predict_dropout(student_id)
    academic_history = AcademicService.get_student_records(student_id)

    return render_template(
        "student/academic_summary.html",
        student=user_profile,
        academic_data=summary,
        prediction=prediction,
        academic_history=academic_history,
        error=None
    )




