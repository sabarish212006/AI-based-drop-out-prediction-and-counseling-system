"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: notification_service.py
Purpose: Notification Business Logic Layer
----------------------------------------------------------
"""

from app.models.notification_model import NotificationModel


class NotificationService:
    """
    Handles notification logic for students,
    counsellors, and admin users.
    """

    # ==========================================
    # Create Notifications
    # ==========================================

    @staticmethod
    def send_notification(
        user_id,
        title,
        message,
        notification_type="General"
    ):
        """
        Send a single notification.
        """

        NotificationModel.create_notification(
            user_id,
            title,
            message,
            notification_type
        )

        return {
            "success": True,
            "message": "Notification sent successfully."
        }

    @staticmethod
    def send_bulk_notifications(user_ids, title, message, notification_type="General"):
        """
        Send notifications to multiple users.
        """

        for user_id in user_ids:
            NotificationModel.create_notification(
                user_id,
                title,
                message,
                notification_type
            )

        return {
            "success": True,
            "message": "Bulk notifications sent successfully."
        }

    # ==========================================
    # Dropout Risk Alerts
    # ==========================================

    @staticmethod
    def send_dropout_alert(student_id, risk_level, probability):
        """
        Send dropout risk alert to counsellor/admin.
        """

        if risk_level == "High":
            title = "🚨 High Dropout Risk Alert"
        elif risk_level == "Medium":
            title = "⚠️ Medium Dropout Risk Warning"
        else:
            title = "ℹ️ Low Risk Notification"

        message = (
            f"Student ID: {student_id}\n"
            f"Risk Level: {risk_level}\n"
            f"Dropout Probability: {probability}%"
        )

        # For now assume admin/counsellor user_id = 1,2 (can be dynamic later)
        NotificationModel.create_notification(1, title, message, "Alert")
        NotificationModel.create_notification(2, title, message, "Alert")

        return {
            "success": True,
            "message": "Dropout alert sent."
        }

    # ==========================================
    # Academic Notifications
    # ==========================================

    @staticmethod
    def notify_academic_update(student_id, semester):
        """
        Notify when academic record is added/updated.
        """

        title = "📘 Academic Record Updated"
        message = f"New academic record added for Semester {semester}."

        return NotificationService.send_notification(
            user_id=student_id,
            title=title,
            message=message,
            notification_type="Academic"
        )

    # ==========================================
    # System Notifications
    # ==========================================

    @staticmethod
    def system_message(user_id, message):
        """
        Send system-wide message.
        """

        return NotificationService.send_notification(
            user_id,
            title="System Message",
            message=message,
            notification_type="System"
        )

    # ==========================================
    # Read / Fetch
    # ==========================================

    @staticmethod
    def get_user_notifications(user_id):
        """
        Get all notifications of a user.
        """

        return NotificationModel.get_notifications_by_user(user_id)

    @staticmethod
    def get_unread(user_id):
        """
        Get unread notifications.
        """

        return NotificationModel.get_unread_notifications(user_id)

    @staticmethod
    def mark_as_read(notification_id):
        """
        Mark notification as read.
        """

        return NotificationModel.mark_as_read(notification_id)

    @staticmethod
    def mark_all_as_read(user_id):
        """
        Mark all notifications as read.
        """

        return NotificationModel.mark_all_as_read(user_id)

    @staticmethod
    def delete_notification(notification_id):
        """
        Delete a notification.
        """

        return NotificationModel.delete_notification(notification_id)

    @staticmethod
    def unread_count(user_id):
        """
        Get unread notification count.
        """

        result = NotificationModel.unread_notification_count(user_id)

        return result["total"] if result else 0