"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: api_routes.py
Purpose: REST API Layer for Frontend & AJAX Calls
----------------------------------------------------------
"""

from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from app.models.student_model import StudentModel
from app.services.notification_service import NotificationService
from app.services.academic_service import AcademicService
from app.services.report_service import ReportService
from app.services.prediction_service import dropout_predictionservice

api_bp = Blueprint("api_bp", __name__)


# ==========================================
# DASHBOARD STATS API
# ==========================================
@api_bp.route("/api/dashboard/stats", methods=["GET"])
@login_required
def dashboard_stats():
    """
    Return admin dashboard stats.
    """

    data = ReportService.get_dashboard_stats()

    return jsonify({
        "success": True,
        "data": data
    })


# ==========================================
# STUDENT SUMMARY API (AI Prediction)
# ==========================================
@api_bp.route("/api/student/summary", methods=["GET"])
@login_required
def student_summary():
    """
    Return logged-in student academic summary
    along with AI prediction.
    """

    user_id = current_user.get_id()

    # Find student using logged-in user_id
    student = StudentModel.get_student_by_user_id(user_id)

    if not student:
        return jsonify({
            "success": False,
            "message": "Student profile not found."
        }), 404

    student_id = student["student_id"]

    # Academic Details
    academic_data = AcademicService.get_student_summary(student_id)

    # AI Prediction
    prediction = dropout_predictionservice.predict_dropout(student_id)

    return jsonify({
        "success": True,
        "academic_data": academic_data,
        "prediction": prediction
    })


# ==========================================
# NOTIFICATIONS API
# ==========================================
@api_bp.route("/api/notifications", methods=["GET"])
@login_required
def get_notifications():
    """
    Get user notifications.
    """

    user_id = current_user.get_id()

    data = NotificationService.get_user_notifications(user_id)

    return jsonify({
        "success": True,
        "data": data
    })


# ==========================================
# UNREAD NOTIFICATIONS COUNT
# ==========================================
@api_bp.route("/api/notifications/unread-count", methods=["GET"])
@login_required
def unread_count():
    """
    Get unread notification count.
    """

    user_id = current_user.get_id()

    count = NotificationService.unread_count(user_id)

    return jsonify({
        "success": True,
        "unread_count": count
    })


# ==========================================
# MARK NOTIFICATION AS READ
# ==========================================
@api_bp.route("/api/notifications/read", methods=["POST"])
@login_required
def mark_read():
    """
    Mark notification as read.
    """

    data = request.get_json()

    notification_id = data.get("notification_id")

    result = NotificationService.mark_as_read(notification_id)

    return jsonify(result)


# ==========================================
# MARK ALL AS READ
# ==========================================
@api_bp.route("/api/notifications/read-all", methods=["POST"])
@login_required
def mark_all_read():
    """
    Mark all notifications as read.
    """

    user_id = current_user.get_id()

    result = NotificationService.mark_all_as_read(user_id)

    return jsonify(result)