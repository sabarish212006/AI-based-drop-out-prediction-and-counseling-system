"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: counselling_model.py
Purpose: Counselling Recommendation Database Operations
----------------------------------------------------------
"""

from app.models.base import BaseModel


class CounsellingModel(BaseModel):
    """
    Handles all database operations related to counselling notes.
    """

    VALID_STATUSES = ["Pending", "Scheduled", "In Progress", "Completed", "Missed"]

    @staticmethod
    def get_notes_by_student(student_id):
        """
        Fetch counselling notes for a student.
        """
        query = """
        SELECT
            cr.recommendation_id,
            cr.prediction_id,
            cr.counsellor_id,
            c.full_name AS counsellor_name,
            cr.recommendation,
            cr.follow_up_date,
            cr.status,
            dp.risk_level,
            dp.probability,
            dp.predicted_on
        FROM counselling_recommendations cr
        INNER JOIN dropout_predictions dp
            ON cr.prediction_id = dp.prediction_id
        LEFT JOIN users c
            ON cr.counsellor_id = c.user_id
        WHERE dp.student_id = %s
        ORDER BY cr.follow_up_date DESC
        """

        return CounsellingModel.fetch_all(query, (student_id,))

    @staticmethod
    def get_recent_notes(limit=5):
        """
        Fetch most recent counselling notes.
        """
        query = """
        SELECT
            cr.recommendation_id,
            cr.prediction_id,
            cr.counsellor_id,
            c.full_name AS counsellor_name,
            cr.recommendation,
            cr.follow_up_date,
            cr.status,
            dp.student_id,
            s.roll_no,
            s.department,
            dp.risk_level,
            dp.probability,
            dp.predicted_on
        FROM counselling_recommendations cr
        INNER JOIN dropout_predictions dp
            ON cr.prediction_id = dp.prediction_id
        INNER JOIN students s
            ON dp.student_id = s.student_id
        LEFT JOIN users c
            ON cr.counsellor_id = c.user_id
        ORDER BY cr.follow_up_date DESC
        LIMIT %s
        """

        return CounsellingModel.fetch_all(query, (limit,))

    @staticmethod
    def create_note(
        prediction_id,
        counsellor_id,
        recommendation,
        follow_up_date,
        status="Pending"
    ):
        """
        Create a new counselling recommendation note.
        """
        query = """
        INSERT INTO counselling_recommendations
        (
            prediction_id,
            counsellor_id,
            recommendation,
            follow_up_date,
            status
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
            prediction_id,
            counsellor_id,
            recommendation,
            follow_up_date,
            status
        )

        return CounsellingModel.execute_query(query, params)

    @staticmethod
    def update_note_status(recommendation_id, status):
        """
        Update the status of a counselling note.
        Only accepts valid statuses.
        """
        if status not in CounsellingModel.VALID_STATUSES:
            return None

        query = """
        UPDATE counselling_recommendations
        SET status=%s
        WHERE recommendation_id=%s
        """

        return CounsellingModel.execute_query(
            query,
            (
                status,
                recommendation_id
            )
        )

    @staticmethod
    def get_note_by_id(recommendation_id):
        """
        Fetch a counselling note by its ID.
        """
        query = """
        SELECT
            cr.recommendation_id,
            cr.prediction_id,
            cr.counsellor_id,
            c.full_name AS counsellor_name,
            cr.recommendation,
            cr.follow_up_date,
            cr.status,
            dp.student_id
        FROM counselling_recommendations cr
        LEFT JOIN users c
            ON cr.counsellor_id = c.user_id
        LEFT JOIN dropout_predictions dp
            ON cr.prediction_id = dp.prediction_id
        WHERE cr.recommendation_id = %s
        LIMIT 1
        """

        return CounsellingModel.fetch_one(query, (recommendation_id,))

    @staticmethod
    def auto_update_overdue_notes():
        """
        Automatically mark overdue notes (past follow_up_date and still Pending) as 'Missed'.
        """
        query = """
        UPDATE counselling_recommendations
        SET status = 'Missed'
        WHERE status = 'Pending'
        AND follow_up_date < CURDATE()
        """
        return CounsellingModel.execute_query(query)