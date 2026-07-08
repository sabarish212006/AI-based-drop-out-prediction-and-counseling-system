"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: notification_model.py
Purpose: Notification Database Operations
----------------------------------------------------------
"""

from app.models.base import BaseModel


class NotificationModel(BaseModel):
    """
    Handles all database operations related to notifications.
    """

    @staticmethod
    def create_notification(
        user_id,
        title,
        message,
        notification_type="General"
    ):
        """
        Create a new notification.
        """

        query = """
        INSERT INTO notifications
        (
            user_id,
            title,
            message,
            notification_type
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        """

        params = (
            user_id,
            title,
            message,
            notification_type
        )

        return NotificationModel.execute_query(query, params)

    @staticmethod
    def get_notification_by_id(notification_id):
        """
        Fetch notification using notification ID.
        """

        query = """
        SELECT *
        FROM notifications
        WHERE notification_id=%s
        LIMIT 1
        """

        return NotificationModel.fetch_one(
            query,
            (notification_id,)
        )

    @staticmethod
    def get_notifications_by_user(user_id):
        """
        Fetch all notifications of a user.
        """

        query = """
        SELECT *
        FROM notifications
        WHERE user_id=%s
        ORDER BY created_at DESC
        """

        return NotificationModel.fetch_all(
            query,
            (user_id,)
        )

    @staticmethod
    def mark_as_read(notification_id):
        """
        Mark notification as read.
        """

        query = """
        UPDATE notifications
        SET is_read=TRUE
        WHERE notification_id=%s
        """

        return NotificationModel.execute_query(
            query,
            (notification_id,)
        )

    @staticmethod
    def mark_all_as_read(user_id):
        """
        Mark all notifications of a user as read.
        """

        query = """
        UPDATE notifications
        SET is_read=TRUE
        WHERE user_id=%s
        """

        return NotificationModel.execute_query(
            query,
            (user_id,)
        )

    @staticmethod
    def delete_notification(notification_id):
        """
        Delete a notification.
        """

        query = """
        DELETE FROM notifications
        WHERE notification_id=%s
        """

        return NotificationModel.execute_query(
            query,
            (notification_id,)
        )

    @staticmethod
    def get_unread_notifications(user_id):
        """
        Fetch unread notifications.
        """

        query = """
        SELECT *
        FROM notifications
        WHERE user_id=%s
        AND is_read=FALSE
        ORDER BY created_at DESC
        """

        return NotificationModel.fetch_all(
            query,
            (user_id,)
        )

    @staticmethod
    def unread_notification_count(user_id):
        """
        Count unread notifications.
        """

        query = """
        SELECT COUNT(*) AS total
        FROM notifications
        WHERE user_id=%s
        AND is_read=FALSE
        """

        return NotificationModel.fetch_one(
            query,
            (user_id,)
        )

    @staticmethod
    def get_all_notifications():
        """
        Fetch all notifications.
        """

        query = """
        SELECT *
        FROM notifications
        ORDER BY created_at DESC
        """

        return NotificationModel.fetch_all(query)