"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: auth_service.py
Purpose: Authentication Business Logic
----------------------------------------------------------
"""

from flask_login import login_user, logout_user

from app.models.user_model import UserModel
from app.models.user import User
from app.services.security_service import SecurityService


class AuthService:
    """
    Authentication Service.
    Handles registration, login and logout.
    """

    @staticmethod
    def register_user(
        full_name,
        email,
        password,
        role,
        phone=None
    ):
        """
        Register a new user.
        """

        if UserModel.email_exists(email):
            return {
                "success": False,
                "message": "Email already exists."
            }

        password_hash = SecurityService.hash_password(password)

        user_id = UserModel.create_user(
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role,
            phone=phone
        )

        if user_id is None:
            return {
                "success": False,
                "message": "Unable to create account."
            }

        return {
            "success": True,
            "message": "Registration successful.",
            "user_id": user_id
        }

    @staticmethod
    def login(email, password):
        """
        Authenticate user.
        """

        if SecurityService.is_account_locked():
            remaining = SecurityService.remaining_lock_time()

            return {
                "success": False,
                "message": f"Account temporarily locked. Try again after {remaining} seconds."
            }

        user_data = UserModel.get_user_by_email(email)

        if not user_data:
            SecurityService.record_failed_attempt()

            return {
                "success": False,
                "message": "Invalid email or password."
            }

        if not user_data["is_active"]:
            return {
                "success": False,
                "message": "Account is inactive."
            }

        if not SecurityService.verify_password(
            password,
            user_data["password_hash"]
        ):
            SecurityService.record_failed_attempt()

            return {
                "success": False,
                "message": "Invalid email or password."
            }

        SecurityService.reset_login_attempts()

        user = User(user_data)

        login_user(user)

        return {
            "success": True,
            "message": "Login successful.",
            "user": user
        }

    @staticmethod
    def logout():
        """
        Logout current user.
        """

        logout_user()

        SecurityService.clear_csrf_token()

        return {
            "success": True,
            "message": "Logout successful."
        }

    @staticmethod
    def change_password(
        user_id,
        current_password,
        new_password
    ):
        """
        Change user password.
        """

        user = UserModel.get_user_by_id(user_id)

        if not user:
            return {
                "success": False,
                "message": "User not found."
            }

        if not SecurityService.verify_password(
            current_password,
            user["password_hash"]
        ):
            return {
                "success": False,
                "message": "Current password is incorrect."
            }

        new_hash = SecurityService.hash_password(
            new_password
        )

        UserModel.update_password(
            user_id,
            new_hash
        )

        return {
            "success": True,
            "message": "Password updated successfully."
        }

    @staticmethod
    def deactivate_user(user_id):
        """
        Deactivate user account.
        """

        UserModel.update_status(
            user_id,
            False
        )

        return {
            "success": True,
            "message": "User deactivated."
        }

    @staticmethod
    def activate_user(user_id):
        """
        Activate user account.
        """

        UserModel.update_status(
            user_id,
            True
        )

        return {
            "success": True,
            "message": "User activated."
        }

    @staticmethod
    def get_user_profile(user_id):
        """
        Get complete student profile.
        """

        user = UserModel.get_complete_student_profile(user_id)

        if not user:
         return None

        return user
    @staticmethod
    def get_all_users():
        """
        Return all users.
        """

        return UserModel.get_all_users()

    @staticmethod
    def get_users_by_role(role):
        """
        Return users filtered by role.
        """

        return UserModel.get_users_by_role(role)