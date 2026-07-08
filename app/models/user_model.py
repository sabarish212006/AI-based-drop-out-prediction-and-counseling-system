"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: user_model.py
Purpose: User Database Operations
----------------------------------------------------------
"""

from app.models.base import BaseModel


class UserModel(BaseModel):
    """
    Handles all database operations related to users.
    """

    @staticmethod
    def create_user(
        full_name,
        email,
        password_hash,
        role,
        phone=None
    ):
        """
        Create a new user.
        """

        query = """
        INSERT INTO users
        (
            full_name,
            email,
            password_hash,
            role,
            phone
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        params = (
            full_name,
            email,
            password_hash,
            role,
            phone
        )

        return UserModel.execute_query(query, params)

    @staticmethod
    def get_user_by_email(email):
        """
        Fetch user using email.
        """

        query = """
        SELECT *
        FROM users
        WHERE email=%s
        LIMIT 1
        """

        return UserModel.fetch_one(query, (email,))

    @staticmethod
    def get_user_by_id(user_id):
        """
        Fetch user using ID.
        """

        query = """
        SELECT *
        FROM users
        WHERE user_id=%s
        LIMIT 1
        """

        return UserModel.fetch_one(query, (user_id,))

    @staticmethod
    def get_all_users():
        """
        Fetch all users.
        """

        query = """
        SELECT
            user_id,
            full_name,
            email,
            role,
            phone,
            is_active,
            created_at
        FROM users
        ORDER BY user_id ASC
        """

        return UserModel.fetch_all(query)

    @staticmethod
    def update_user(
        user_id,
        full_name,
        phone
    ):
        """
        Update user profile.
        """

        query = """
        UPDATE users
        SET
            full_name=%s,
            phone=%s
        WHERE user_id=%s
        """

        params = (
            full_name,
            phone,
            user_id
        )

        return UserModel.execute_query(query, params)

    @staticmethod
    def update_password(
        user_id,
        password_hash
    ):
        """
        Update password hash.
        """

        query = """
        UPDATE users
        SET
            password_hash=%s
        WHERE user_id=%s
        """

        return UserModel.execute_query(
            query,
            (
                password_hash,
                user_id
            )
        )

    @staticmethod
    def update_status(
        user_id,
        is_active
    ):
        """
        Activate / Deactivate user.
        """

        query = """
        UPDATE users
        SET
            is_active=%s
        WHERE user_id=%s
        """

        return UserModel.execute_query(
            query,
            (
                is_active,
                user_id
            )
        )

    @staticmethod
    def delete_user(user_id):
        """
        Delete user.
        """

        query = """
        DELETE
        FROM users
        WHERE user_id=%s
        """

        return UserModel.execute_query(
            query,
            (
                user_id,
            )
        )

    @staticmethod
    def email_exists(email):
        """
        Check if email already exists.
        """

        query = """
        SELECT user_id
        FROM users
        WHERE email=%s
        LIMIT 1
        """

        user = UserModel.fetch_one(
            query,
            (
                email,
            )
        )

        return user is not None

    @staticmethod
    def get_users_by_role(role):
        """
        Get users by role.
        """

        query = """
        SELECT
            user_id,
            full_name,
            email,
            phone,
            role,
            is_active
        FROM users
        WHERE role=%s
        ORDER BY full_name
        """

        return UserModel.fetch_all(
            query,
            (
                role,
            )
        )  
    @staticmethod
    def get_complete_student_profile(user_id):
        """
        Get complete student profile by joining users and students tables.
        """

        query = """
        SELECT
            u.user_id,
            u.full_name,
            u.email,
            u.phone,
            u.role,
            u.is_active,
            s.student_id,
            s.roll_no,
            s.department,
            s.year_of_study,
            s.gender,
            s.date_of_birth,
            s.address
        FROM users u
        LEFT JOIN students s
            ON u.user_id = s.user_id
        WHERE u.user_id = %s
        LIMIT 1
        """

        return UserModel.fetch_one(query, (user_id,))   