"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: student_model.py
Purpose: Student Database Operations
----------------------------------------------------------
"""

from app.models.base import BaseModel


class StudentModel(BaseModel):
    """
    Handles all database operations related to students.
    """

    @staticmethod
    def create_student(
        user_id,
        roll_no,
        department,
        year_of_study,
        gender,
        date_of_birth,
        address
    ):
        """
        Create a new student record.
        """

        query = """
        INSERT INTO students
        (
            user_id,
            roll_no,
            department,
            year_of_study,
            gender,
            date_of_birth,
            address
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        params = (
            user_id,
            roll_no,
            department,
            year_of_study,
            gender,
            date_of_birth,
            address
        )

        return StudentModel.execute_query(query, params)

    @staticmethod
    def get_student_by_id(student_id):
        """
        Get student using student ID.
        """

        query = """
        SELECT *
        FROM students
        WHERE student_id = %s
        LIMIT 1
        """

        return StudentModel.fetch_one(query, (student_id,))

    @staticmethod
    def get_student_by_user_id(user_id):
        """
        Get student using user ID.
        """

        query = """
        SELECT *
        FROM students
        WHERE user_id = %s
        LIMIT 1
        """

        return StudentModel.fetch_one(query, (user_id,))

    @staticmethod
    def get_student_by_roll_no(roll_no):
        """
        Get student using roll number.
        """

        query = """
        SELECT *
        FROM students
        WHERE roll_no = %s
        LIMIT 1
        """

        return StudentModel.fetch_one(query, (roll_no,))

    @staticmethod
    def get_all_students():
        """
        Fetch all students.
        """

        query = """
        SELECT *
        FROM students
        ORDER BY student_id ASC
        """

        return StudentModel.fetch_all(query)

    @staticmethod
    def update_student(
        student_id,
        department,
        year_of_study,
        gender,
        date_of_birth,
        address
    ):
        """
        Update student information.
        """

        query = """
        UPDATE students
        SET
            department=%s,
            year_of_study=%s,
            gender=%s,
            date_of_birth=%s,
            address=%s
        WHERE student_id=%s
        """

        params = (
            department,
            year_of_study,
            gender,
            date_of_birth,
            address,
            student_id
        )

        return StudentModel.execute_query(query, params)

    @staticmethod
    def delete_student(student_id):
        """
        Delete student record.
        """

        query = """
        DELETE FROM students
        WHERE student_id=%s
        """

        return StudentModel.execute_query(
            query,
            (student_id,)
        )

    @staticmethod
    def student_exists(student_id):
        """
        Check whether student exists.
        """

        query = """
        SELECT student_id
        FROM students
        WHERE student_id=%s
        LIMIT 1
        """

        student = StudentModel.fetch_one(
            query,
            (student_id,)
        )
        return student is not None

    @staticmethod
    def get_all_students_admin():
        """
        Fetch all students with latest academic and prediction data for admin management.
        """

        query = """
        SELECT
            u.user_id,
            u.full_name,
            u.email,
            u.phone,
            u.is_active,
            s.student_id,
            s.roll_no,
            s.department,
            s.year_of_study,
            a.cgpa,
            a.attendance,
            a.internal_marks,
            a.backlog_count,
            p.risk_level,
            p.probability AS prediction_score,
            p.predicted_on
        FROM users u
        INNER JOIN students s
            ON u.user_id = s.user_id
        LEFT JOIN academic_records a
            ON a.student_id = s.student_id
            AND a.semester = (
                SELECT MAX(semester)
                FROM academic_records
                WHERE student_id = s.student_id
            )
        LEFT JOIN dropout_predictions p
            ON p.student_id = s.student_id
            AND p.predicted_on = (
                SELECT MAX(predicted_on)
                FROM dropout_predictions
                WHERE student_id = s.student_id
            )
        WHERE u.role = 'Student'
        ORDER BY u.full_name ASC
        """

        return StudentModel.fetch_all(query)

    @staticmethod
    def get_recent_students(limit=5):
        """
        Fetch most recently registered students.
        """

        query = """
        SELECT
            u.user_id,
            u.full_name,
            u.email,
            u.phone,
            u.is_active,
            u.created_at,
            s.student_id,
            s.roll_no,
            s.department,
            s.year_of_study
        FROM users u
        INNER JOIN students s
            ON u.user_id = s.user_id
        WHERE u.role = 'Student'
        ORDER BY u.created_at DESC
        LIMIT %s
        """

        return StudentModel.fetch_all(query, (limit,))

    @staticmethod
    def get_student_profile(student_id):
        """
        Fetch complete student profile
        by joining users and students tables.
        """

        query = """
        SELECT
            u.user_id,
            u.full_name,
            u.email,
            u.phone,
            u.role,
            s.student_id,
            s.roll_no,
            s.department,
            s.year_of_study,
            s.gender,
            s.date_of_birth,
            s.address
        FROM users u
        INNER JOIN students s
            ON u.user_id = s.user_id
        WHERE s.student_id = %s
        """

        return StudentModel.fetch_one(
            query,
            (student_id,)
        )