"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: admin_routes.py
Purpose: Admin Portal Routes
----------------------------------------------------------
"""

from io import BytesIO

from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    send_file
)

from flask_login import login_required

from openpyxl import Workbook

from app.services.auth_service import AuthService
from app.services.report_service import ReportService
from app.services.prediction_service import dropout_predictionservice

from app.models.student_model import StudentModel
from app.models.academic_model import AcademicModel
from app.models.counselling_model import CounsellingModel


admin_bp = Blueprint("admin_bp", __name__)


# ==========================================
# ADMIN DASHBOARD
# ==========================================
@admin_bp.route("/admin/dashboard")
@login_required
def dashboard():

    stats = ReportService.get_dashboard_stats()

    return render_template(
        "admin/dashboard.html",
        stats=stats
    )


# ==========================================
# MANAGE STUDENTS
# ==========================================
@admin_bp.route("/admin/students")
@login_required
def manage_students():

    students = StudentModel.get_all_students_admin()

    return render_template(
        "admin/manage_students.html",
        students=students
    )


# ==========================================
# STUDENT COMPLETE DETAILS
# ==========================================
@admin_bp.route("/admin/student/<int:user_id>")
@login_required
def student_details(user_id):

    user = AuthService.get_user_profile(user_id)

    if not user:
        return "User not found", 404

    student = StudentModel.get_student_by_user_id(user_id)

    if not student:
        return "Student profile not found", 404

    academic = AcademicModel.get_student_academic_summary(
        student["student_id"]
    )

    prediction = dropout_predictionservice.predict_dropout(
        student["student_id"]
    )

    prediction_history = dropout_predictionservice.get_prediction_history(
        student["student_id"]
    )

    counselling_notes = CounsellingModel.get_notes_by_student(
        student["student_id"]
    )

    return render_template(
        "admin/student_detail.html",
        user=user,
        student=student,
        academic=academic,
        prediction=prediction,
        prediction_history=prediction_history,
        counselling_notes=counselling_notes
    )


# ==========================================
# MANAGE COUNSELLORS
# ==========================================
@admin_bp.route("/admin/counsellors")
@login_required
def manage_counsellors():

    counsellors = AuthService.get_users_by_role("Counsellor")

    return render_template(
        "admin/manage_counsellors.html",
        counsellors=counsellors
    )


# ==========================================
# REPORTS
# ==========================================
@admin_bp.route("/admin/reports")
@login_required
def reports():

    stats = ReportService.get_dashboard_stats()

    return render_template(
        "admin/reports.html",
        stats=stats
    )
# ==========================================
# EXPORT REPORT AS EXCEL
# ==========================================
@admin_bp.route("/admin/reports/excel")
@login_required
def export_excel():

    stats = ReportService.get_dashboard_stats()

    workbook = Workbook()

    sheet = workbook.active
    sheet.title = "AI Report"

    sheet.append(["AI Dropout Prediction Report"])
    sheet.append([])

    sheet.append(["Total Students", stats["total_students"]])
    sheet.append(["Total Counsellors", stats["total_counsellors"]])
    sheet.append(["Total Predictions", stats["total_predictions"]])
    sheet.append(["High Risk", stats["high_risk_students"]])
    sheet.append(["Medium Risk", stats["medium_risk_students"]])
    sheet.append(["Low Risk", stats["low_risk_students"]])

    sheet.append([])

    sheet.append([
        "Average CGPA",
        stats["academic_summary"]["average_cgpa"]
    ])

    sheet.append([
        "Average Attendance",
        stats["academic_summary"]["average_attendance"]
    ])

    output = BytesIO()

    workbook.save(output)

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="AI_Dropout_Report.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ==========================================
# EXPORT REPORT AS PDF
# ==========================================
@admin_bp.route("/admin/reports/pdf")
@login_required
def export_pdf():
    from app.services.pdf_service import PDFService

    stats = ReportService.get_dashboard_stats()
    pdf_buffer = PDFService.generate_system_report(stats)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="AI_Dropout_Report.pdf",
        mimetype="application/pdf"
    )


# ==========================================
# EXPORT STUDENT REPORT AS PDF
# ==========================================
@admin_bp.route("/admin/student/<int:user_id>/pdf")
@login_required
def export_student_pdf(user_id):
    from app.services.pdf_service import PDFService

    user = AuthService.get_user_profile(user_id)
    if not user:
        return "User not found", 404

    student = StudentModel.get_student_by_user_id(user_id)
    if not student:
        return "Student profile not found", 404

    student_id = student["student_id"]
    academic = AcademicModel.get_student_academic_summary(student_id)
    prediction = dropout_predictionservice.predict_dropout(student_id)
    academic_history = AcademicModel.get_records_by_student(student_id)
    counselling_notes = CounsellingModel.get_notes_by_student(student_id)

    pdf_buffer = PDFService.generate_student_report(
        student=student,
        academic=academic,
        prediction=prediction,
        academic_history=academic_history,
        counselling_notes=counselling_notes
    )

    # Clean the full name for a safe filename
    safe_name = "".join(c for c in student.get("full_name", "Student") if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_')
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"Student_Report_{safe_name}_{student['roll_no']}.pdf",
        mimetype="application/pdf"
    )

# ==========================================
# ACTIVATE / DEACTIVATE USER
# ==========================================
@admin_bp.route("/admin/user/toggle", methods=["POST"])
@login_required
def toggle_user_status():

    data = request.form

    user_id = int(data.get("user_id"))
    action = data.get("action")

    if action == "activate":
        result = AuthService.activate_user(user_id)
    else:
        result = AuthService.deactivate_user(user_id)

    return jsonify(result)


# ==========================================
# DASHBOARD ANALYTICS API
# ==========================================
@admin_bp.route("/admin/dashboard/data")
@login_required
def dashboard_data():

    stats = ReportService.get_dashboard_stats()

    return jsonify(stats)