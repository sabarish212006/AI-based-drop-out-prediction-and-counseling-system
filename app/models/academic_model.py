"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: academic_model.py
Purpose: Academic Database Operations
----------------------------------------------------------
"""

from app.models.base import BaseModel


class AcademicModel(BaseModel):
    """
    Handles all database operations related to academic records.
    """

    @staticmethod
    def create_academic_record(
        student_id,
        semester,
        cgpa,
        attendance,
        internal_marks,
        backlog_count,
        study_hours
    ):
        """
        Insert a new academic record.
        """

        query = """
        INSERT INTO academic_records
        (
            student_id,
            semester,
            cgpa,
            attendance,
            internal_marks,
            backlog_count,
            study_hours
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
            student_id,
            semester,
            cgpa,
            attendance,
            internal_marks,
            backlog_count,
            study_hours
        )

        return AcademicModel.execute_query(query, params)

    @staticmethod
    def get_record_by_id(record_id):
        """
        Fetch academic record using academic_id.
        """

        query = """
        SELECT *
        FROM academic_records
        WHERE academic_id = %s
        LIMIT 1
        """

        return AcademicModel.fetch_one(query, (record_id,))

    @staticmethod
    def get_records_by_student(student_id):
        """
        Fetch all academic records of a student.
        """

        query = """
        SELECT *
        FROM academic_records
        WHERE student_id = %s
        ORDER BY semester ASC
        """

        return AcademicModel.fetch_all(query, (student_id,))

    @staticmethod
    def get_latest_record(student_id):
        """
        Fetch latest semester academic record.
        """

        query = """
        SELECT *
        FROM academic_records
        WHERE student_id = %s
        ORDER BY semester DESC
        LIMIT 1
        """

        return AcademicModel.fetch_one(query, (student_id,))

    @staticmethod
    def update_academic_record(
        academic_id,
        semester,
        cgpa,
        attendance,
        internal_marks,
        backlog_count,
        study_hours
    ):
        """
        Update an academic record.
        """

        query = """
        UPDATE academic_records
        SET
            semester=%s,
            cgpa=%s,
            attendance=%s,
            internal_marks=%s,
            backlog_count=%s,
            study_hours=%s
        WHERE academic_id=%s
        """

        params = (
            semester,
            cgpa,
            attendance,
            internal_marks,
            backlog_count,
            study_hours,
            academic_id
        )

        return AcademicModel.execute_query(query, params)

    @staticmethod
    def delete_academic_record(academic_id):
        """
        Delete an academic record.
        """

        query = """
        DELETE FROM academic_records
        WHERE academic_id=%s
        """

        return AcademicModel.execute_query(query, (academic_id,))

    @staticmethod
    def academic_record_exists(academic_id):
        """
        Check whether academic record exists.
        """

        query = """
        SELECT academic_id
        FROM academic_records
        WHERE academic_id=%s
        LIMIT 1
        """

        record = AcademicModel.fetch_one(query, (academic_id,))

        return record is not None

    @staticmethod
    def get_all_records():
        """
        Fetch all academic records.
        """

        query = """
        SELECT *
        FROM academic_records
        ORDER BY student_id, semester
        """

        return AcademicModel.fetch_all(query)

    @staticmethod
    def get_student_academic_summary(student_id):
        """
        Fetch student profile with latest academic details.
        Used by prediction service.
        """

        query = """
        SELECT
            s.student_id,
            s.roll_no,
            s.department,
            s.year_of_study,
            a.semester,
            a.cgpa,
            a.attendance,
            a.internal_marks,
            a.backlog_count,
            a.study_hours
        FROM students s
        INNER JOIN academic_records a
            ON s.student_id = a.student_id
        WHERE s.student_id = %s
        ORDER BY a.semester DESC
        LIMIT 1
        """

        return AcademicModel.fetch_one(query, (student_id,))

    @staticmethod
    def get_record_by_student_semester(student_id, semester):
        """
        Fetch academic record for a specific student and semester.
        Used to detect duplicate semester entries before insert.

        Returns:
            dict with record data if found, None otherwise
        """

        query = """
        SELECT academic_id, student_id, semester, cgpa, attendance,
               internal_marks, backlog_count, study_hours
        FROM academic_records
        WHERE student_id = %s AND semester = %s
        LIMIT 1
        """

        return AcademicModel.fetch_one(query, (student_id, semester))