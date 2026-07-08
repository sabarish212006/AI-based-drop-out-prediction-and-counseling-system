"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: counsellor_routes.py
Purpose: Counsellor Portal Routes
----------------------------------------------------------
"""

from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    redirect,
    url_for,
    flash
)
from flask_login import login_required, current_user

from app.services.prediction_service import dropout_predictionservice
from app.services.report_service import ReportService
from app.services.recommendation_service import RecommendationService
from app.models.counselling_model import CounsellingModel
from app.models.student_model import StudentModel
from app.models.prediction_model import PredictionModel

counsellor_bp = Blueprint("counsellor_bp", __name__)


def _ensure_counsellor():
    if current_user.role != "Counsellor":
        flash("You are not authorized to access this page.", "danger")
        return False
    return True


# ==========================================
# COUNSELLOR DASHBOARD
# ==========================================
@counsellor_bp.route("/counsellor/dashboard")
@login_required
def dashboard():
    """
    Counsellor Dashboard
    """

    if not _ensure_counsellor():
        return redirect(url_for("auth_bp.login"))

    # Auto-update overdue notes before displaying dashboard
    CounsellingModel.auto_update_overdue_notes()

    stats = ReportService.get_dashboard_stats()
    predictions = dropout_predictionservice.get_all_dropout_predictions()
    at_risk_students = [
        p for p in predictions
        if p["risk_level"] in ["High", "Medium"]
    ]
    recent_notes = CounsellingModel.get_recent_notes(5)

    return render_template(
        "counsellor/dashboard.html",
        stats=stats,
        at_risk_students=at_risk_students[:5],
        recent_notes=recent_notes
    )


# ==========================================
# AT-RISK STUDENTS
# ==========================================
@counsellor_bp.route("/counsellor/at-risk")
@login_required
def at_risk_students():
    """
    Display only High and Medium risk students.
    """

    if not _ensure_counsellor():
        return redirect(url_for("auth_bp.login"))

    predictions = dropout_predictionservice.get_all_dropout_predictions()
    students = [
        p for p in predictions
        if p["risk_level"] in ["High", "Medium"]
    ]

    return render_template(
        "counsellor/at_risk_students.html",
        students=students
    )


# ==========================================
# STUDENT DETAILS
# ==========================================
@counsellor_bp.route("/counsellor/student/<int:student_id>")
@login_required
def student_detail(student_id):
    """
    Student AI Prediction Details
    """

    if not _ensure_counsellor():
        return redirect(url_for("auth_bp.login"))

    student = StudentModel.get_student_profile(student_id)

    if not student:
        return "Student not found", 404

    prediction = dropout_predictionservice.get_prediction_by_student(student_id)
    counselling_notes = CounsellingModel.get_notes_by_student(student_id)
    recommendation = RecommendationService.get_recommendation(prediction)

    return render_template(
        "counsellor/student_detail.html",
        student=student,
        prediction=prediction,
        counselling_notes=counselling_notes,
        recommendation=recommendation
    )


# ==========================================
# ADD COUNSELLING NOTE
# ==========================================
@counsellor_bp.route("/counsellor/student/<int:student_id>/notes", methods=["POST"])
@login_required
def add_counselling_note(student_id):
    """
    Add a counselling note for a student.
    """

    if not _ensure_counsellor():
        return redirect(url_for("auth_bp.login"))

    student = StudentModel.get_student_profile(student_id)

    if not student:
        flash("Student not found.", "danger")
        return redirect(url_for("counsellor_bp.at_risk_students"))

    recommendation_text = request.form.get("recommendation", "").strip()
    follow_up_date = request.form.get("follow_up_date")

    if not recommendation_text or not follow_up_date:
        flash("Recommendation and follow-up date are required.", "warning")
        return redirect(url_for("counsellor_bp.student_detail", student_id=student_id))

    latest_prediction = PredictionModel.get_latest_prediction(student_id)
    prediction_id = latest_prediction["prediction_id"] if latest_prediction else None

    CounsellingModel.create_note(
        prediction_id=prediction_id,
        counsellor_id=int(current_user.get_id()),
        recommendation=recommendation_text,
        follow_up_date=follow_up_date,
        status="Pending"
    )

    flash("Counselling note saved successfully.", "success")

    return redirect(url_for("counsellor_bp.student_detail", student_id=student_id))


# ==========================================
# UPDATE COUNSELLING NOTE STATUS
# ==========================================
@counsellor_bp.route("/counsellor/student/<int:student_id>/notes/<int:recommendation_id>/status", methods=["POST"])
@login_required
def update_note_status(student_id, recommendation_id):
    """
    Update the status of a counselling note.
    Supports: Pending, Scheduled, In Progress, Completed, Missed
    """

    if not _ensure_counsellor():
        return redirect(url_for("auth_bp.login"))

    new_status = request.form.get("status", "Pending")

    if new_status not in CounsellingModel.VALID_STATUSES:
        flash(f"Invalid status: {new_status}", "danger")
        return redirect(url_for("counsellor_bp.student_detail", student_id=student_id))

    CounsellingModel.update_note_status(recommendation_id, new_status)

    flash(f"Counselling note status updated to: {new_status}", "success")

    return redirect(url_for("counsellor_bp.student_detail", student_id=student_id))


# ==========================================
# COMPLETE COUNSELLING NOTE (legacy route)
# ==========================================
@counsellor_bp.route("/counsellor/student/<int:student_id>/notes/<int:recommendation_id>/complete", methods=["POST"])
@login_required
def complete_counselling_note(student_id, recommendation_id):
    """
    Mark a counselling note as completed (legacy support).
    """

    if not _ensure_counsellor():
        return redirect(url_for("auth_bp.login"))

    CounsellingModel.update_note_status(recommendation_id, "Completed")

    flash("Counselling note marked as completed.", "success")

    return redirect(url_for("counsellor_bp.student_detail", student_id=student_id))


# ==========================================
# COUNSELLOR ANALYTICS
# ==========================================
@counsellor_bp.route("/counsellor/analytics")
@login_required
def analytics():
    """
    Counsellor analytics and AI insight page.
    """

    if not _ensure_counsellor():
        return redirect(url_for("auth_bp.login"))

    stats = ReportService.get_dashboard_stats()
    department_performance = ReportService.get_average_metrics_by_department()
    year_count = ReportService.get_year_student_count()

    return render_template(
        "counsellor/analytics.html",
        stats=stats,
        department_performance=department_performance,
        year_count=year_count
    )


# ==========================================
# RISK SUMMARY API
# ==========================================
@counsellor_bp.route("/counsellor/risk-summary")
@login_required
def risk_summary():
    """
    Risk Summary
    """

    predictions = dropout_predictionservice.get_all_dropout_predictions()

    summary = {
        "High": 0,
        "Medium": 0,
        "Low": 0
    }

    for p in predictions:

        if p["risk_level"] in summary:
            summary[p["risk_level"]] += 1

    return jsonify(summary)


# ==========================================
# EXPORT STUDENT REPORT AS PDF (COUNSELLOR)
# ==========================================
@counsellor_bp.route("/counsellor/student/<int:student_id>/pdf")
@login_required
def export_student_pdf(student_id):
    if not _ensure_counsellor():
        return redirect(url_for("auth_bp.login"))

    from app.services.pdf_service import PDFService
    from app.models.academic_model import AcademicModel
    from flask import send_file

    student = StudentModel.get_student_profile(student_id)
    if not student:
        return "Student not found", 404

    prediction = dropout_predictionservice.predict_dropout(student_id)
    academic_history = AcademicModel.get_records_by_student(student_id)
    counselling_notes = CounsellingModel.get_notes_by_student(student_id)

    pdf_buffer = PDFService.generate_student_report(
        student=student,
        academic=prediction,
        prediction=prediction,
        academic_history=academic_history,
        counselling_notes=counselling_notes
    )

    safe_name = "".join(c for c in student.get("full_name", "Student") if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"Student_Report_{safe_name}_{student['roll_no']}.pdf",
        mimetype="application/pdf"
    )