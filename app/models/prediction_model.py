"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: prediction_model.py
Purpose: Prediction Database Operations
----------------------------------------------------------
"""

from app.models.base import BaseModel


class PredictionModel(BaseModel):
    """
    Handles all database operations related to
    AI prediction results.
    """

    @staticmethod
    def create_prediction(
        student_id,
        prediction_result,
        dropout_probability,
        risk_level,
        explanation,
        model_version
    ):
        """
        Save a new AI prediction.

        Note: The actual database table has columns:
        prediction_id, student_id, model_version, risk_level, probability, predicted_on
        prediction_result and explanation are accepted as parameters for API consistency
        but are not stored in the current schema.
        """

        query = """
        INSERT INTO dropout_predictions
        (
            student_id,
            probability,
            risk_level,
            model_version
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
            student_id,
            dropout_probability,
            risk_level,
            model_version
        )

        return PredictionModel.execute_query(query, params)

    @staticmethod
    def get_prediction_by_id(prediction_id):
        """
        Fetch prediction by prediction ID.
        """

        query = """
        SELECT *
        FROM dropout_predictions
        WHERE prediction_id=%s
        LIMIT 1
        """

        return PredictionModel.fetch_one(query, (prediction_id,))

    @staticmethod
    def get_dropout_predictions_by_student(student_id):
        """
        Fetch all dropout_predictions of a student.
        """

        query = """
        SELECT *
        FROM dropout_predictions
        WHERE student_id=%s
        ORDER BY predicted_on DESC
        """

        return PredictionModel.fetch_all(query, (student_id,))

    @staticmethod
    def get_latest_prediction(student_id):
        """
        Fetch latest prediction of a student.
        """

        query = """
        SELECT *
        FROM dropout_predictions
        WHERE student_id=%s
        ORDER BY predicted_on DESC
        LIMIT 1
        """

        return PredictionModel.fetch_one(query, (student_id,))

    @staticmethod
    def update_prediction(
        prediction_id,
        prediction_result,
        dropout_probability,
        risk_level,
        explanation,
        model_version
    ):
        """
        Update prediction details.
        """

        query = """
        UPDATE dropout_predictions
        SET
            probability=%s,
            risk_level=%s,
            model_version=%s
        WHERE prediction_id=%s
        """

        params = (
            dropout_probability,
            risk_level,
            model_version,
            prediction_id
        )

        return PredictionModel.execute_query(query, params)

    @staticmethod
    def delete_prediction(prediction_id):
        """
        Delete prediction record.
        """

        query = """
        DELETE FROM dropout_predictions
        WHERE prediction_id=%s
        """

        return PredictionModel.execute_query(query, (prediction_id,))

    @staticmethod
    def prediction_exists(prediction_id):
        """
        Check whether prediction exists.
        """

        query = """
        SELECT prediction_id
        FROM dropout_predictions
        WHERE prediction_id=%s
        LIMIT 1
        """

        prediction = PredictionModel.fetch_one(query, (prediction_id,))

        return prediction is not None

    @staticmethod
    def get_all_dropout_predictions():
        """
        Fetch all prediction records.
        """

        query = """
        SELECT dp.*
        FROM dropout_predictions dp
        INNER JOIN students s ON dp.student_id = s.student_id
        ORDER BY dp.predicted_on DESC
        """

        return PredictionModel.fetch_all(query)

    @staticmethod
    def get_prediction_dashboard():
        """
        Fetch prediction summary for admin dashboard.
        """

        query = """
        SELECT
            dp.prediction_id,
            dp.student_id,
            dp.probability,
            dp.risk_level,
            dp.predicted_on
        FROM dropout_predictions dp
        INNER JOIN students s ON dp.student_id = s.student_id
        ORDER BY dp.predicted_on DESC
        """

        return PredictionModel.fetch_all(query)