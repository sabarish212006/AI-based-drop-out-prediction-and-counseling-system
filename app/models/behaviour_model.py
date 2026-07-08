"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: behaviour_model.py
Purpose: Behaviour & Socio-Economic Database Operations
----------------------------------------------------------
"""

from app.models.base import BaseModel


class BehaviourModel(BaseModel):
    """
    Handles all database operations related to
    student behaviour and socio-economic factors.
    """

    @staticmethod
    def create_behaviour_record(
        student_id,
        family_income,
        parent_education,
        parent_occupation,
        internet_access,
        extracurricular_activity,
        health_issue,
        stress_level,
        counselling_history
    ):
        """
        Insert a new behaviour record.
        """

        query = """
        INSERT INTO behaviour_records
        (
            student_id,
            family_income,
            parent_education,
            parent_occupation,
            internet_access,
            extracurricular_activity,
            health_issue,
            stress_level,
            counselling_history
        )
        VALUES
        (
            %s,
            %s,
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
            family_income,
            parent_education,
            parent_occupation,
            internet_access,
            extracurricular_activity,
            health_issue,
            stress_level,
            counselling_history
        )

        return BehaviourModel.execute_query(query, params)

    @staticmethod
    def get_record_by_id(behaviour_id):
        """
        Fetch behaviour record by ID.
        """

        query = """
        SELECT *
        FROM behaviour_records
        WHERE behaviour_id=%s
        LIMIT 1
        """

        return BehaviourModel.fetch_one(query, (behaviour_id,))

    @staticmethod
    def get_record_by_student(student_id):
        """
        Fetch behaviour record using student ID.
        """

        query = """
        SELECT *
        FROM behaviour_records
        WHERE student_id=%s
        LIMIT 1
        """

        return BehaviourModel.fetch_one(query, (student_id,))

    @staticmethod
    def update_behaviour_record(
        behaviour_id,
        family_income,
        parent_education,
        parent_occupation,
        internet_access,
        extracurricular_activity,
        health_issue,
        stress_level,
        counselling_history
    ):
        """
        Update behaviour record.
        """

        query = """
        UPDATE behaviour_records
        SET
            family_income=%s,
            parent_education=%s,
            parent_occupation=%s,
            internet_access=%s,
            extracurricular_activity=%s,
            health_issue=%s,
            stress_level=%s,
            counselling_history=%s
        WHERE behaviour_id=%s
        """

        params = (
            family_income,
            parent_education,
            parent_occupation,
            internet_access,
            extracurricular_activity,
            health_issue,
            stress_level,
            counselling_history,
            behaviour_id
        )

        return BehaviourModel.execute_query(query, params)

    @staticmethod
    def delete_behaviour_record(behaviour_id):
        """
        Delete behaviour record.
        """

        query = """
        DELETE FROM behaviour_records
        WHERE behaviour_id=%s
        """

        return BehaviourModel.execute_query(query, (behaviour_id,))

    @staticmethod
    def behaviour_record_exists(behaviour_id):
        """
        Check whether behaviour record exists.
        """

        query = """
        SELECT behaviour_id
        FROM behaviour_records
        WHERE behaviour_id=%s
        LIMIT 1
        """

        record = BehaviourModel.fetch_one(query, (behaviour_id,))

        return record is not None

    @staticmethod
    def get_all_behaviour_records():
        """
        Fetch all behaviour records.
        """

        query = """
        SELECT *
        FROM behaviour_records
        ORDER BY student_id
        """

        return BehaviourModel.fetch_all(query)

    @staticmethod
    def get_student_behaviour_summary(student_id):
        """
        Fetch behaviour summary used for AI prediction.
        """

        query = """
        SELECT
            student_id,
            family_income,
            parent_education,
            parent_occupation,
            internet_access,
            extracurricular_activity,
            health_issue,
            stress_level,
            counselling_history
        FROM behaviour_records
        WHERE student_id=%s
        LIMIT 1
        """

        return BehaviourModel.fetch_one(query, (student_id,))