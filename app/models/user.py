"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: user.py
Purpose: Flask-Login User Class
----------------------------------------------------------
"""

from flask_login import UserMixin


class User(UserMixin):
    """
    Flask-Login compatible User object.
    """

    def __init__(self, user_data: dict):
        self.user_id = user_data["user_id"]
        self.full_name = user_data["full_name"]
        self.email = user_data["email"]
        self.password_hash = user_data["password_hash"]
        self.role = user_data["role"]
        self.phone = user_data.get("phone")
        self.is_active_user = bool(user_data["is_active"])
        self.created_at = user_data.get("created_at")

    def get_id(self):
        """
        Flask-Login requires string ID.
        """
        return str(self.user_id)

    @property
    def is_active(self):
        """
        Returns account active status.
        """
        return self.is_active_user

    @property
    def is_admin(self):
        return self.role == "Admin"

    @property
    def is_student(self):
        return self.role == "Student"

    @property
    def is_counsellor(self):
        return self.role == "Counsellor"

    def to_dict(self):
        """
        Return user information as dictionary.
        """

        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
            "is_active": self.is_active_user,
            "created_at": self.created_at
        }