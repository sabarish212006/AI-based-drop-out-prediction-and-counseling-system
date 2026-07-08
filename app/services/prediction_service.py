"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: prediction_service.py
Purpose: Student Dropout Prediction Business Logic
----------------------------------------------------------
"""

from datetime import datetime

from app.models.academic_model import AcademicModel
from app.models.student_model import StudentModel
from app.services.ml_model_service import MLModelService
from app.models.prediction_model import PredictionModel
from app.utils.logger import get_logger

logger = get_logger(__name__)


class dropout_predictionservice:
    """
    AI-based dropout prediction service.
    Coordinates between the ML model and the database.
    """

    # ----------------------------------------------------------
    # PRIVATE HELPERS
    # ----------------------------------------------------------

    @staticmethod
    def _safe_float(value, default=0.0):
        try:
            return round(float(value), 2)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _safe_int(value, default=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _safe_risk_level(value):
        risk = str(value or "").strip().title()
        if risk in {"High", "Medium", "Low"}:
            return risk
        return "Low"

    @staticmethod
    def _build_recommendation(risk_level, attendance, backlog_count, study_hours, cgpa=None):
        """Build contextual recommendation text based on risk factors."""
        attendance    = dropout_predictionservice._safe_float(attendance)
        backlog_count = dropout_predictionservice._safe_int(backlog_count)
        study_hours   = dropout_predictionservice._safe_float(study_hours)
        cgpa          = dropout_predictionservice._safe_float(cgpa)

        if risk_level == "High":
            parts = ["🚨 Immediate counselling session is required."]
            if attendance < 65:
                parts.append(f"Attendance is critically low ({attendance:.1f}%) — target above 80%.")
            if backlog_count >= 4:
                parts.append(f"Clear {backlog_count} pending backlogs with faculty support.")
            if cgpa and cgpa < 5.5:
                parts.append(f"CGPA of {cgpa:.1f} is very low — enroll in remedial classes.")
            if study_hours < 2:
                parts.append("Increase daily study hours to at least 3-4 hours.")
            parts.append("Regular faculty mentoring and attendance tracking are essential.")
            return " ".join(parts)

        if risk_level == "Medium":
            parts = ["⚠️ Performance needs improvement."]
            if attendance < 75:
                parts.append(f"Attendance ({attendance:.1f}%) is below recommended 75%.")
            if backlog_count > 0:
                parts.append(f"Work to clear {backlog_count} backlog(s) in the next semester.")
            if study_hours < 2.5:
                parts.append("Increase study time and participate in peer study groups.")
            parts.append("Meet your counsellor for an academic progress review.")
            return " ".join(parts)

        # Low risk
        parts = ["✅ Keep up the excellent work!"]
        if cgpa and cgpa >= 8.0:
            parts.append("Outstanding CGPA — consider academic leadership opportunities.")
        parts.append("Maintain current attendance and study habits.")
        parts.append("Continue participating in extracurricular activities.")
        return " ".join(parts)

    @staticmethod
    def _build_message(risk_level):
        """Build short summary message for risk level."""
        if risk_level == "High":
            return "Student is at HIGH risk of dropout. Immediate intervention is recommended."
        if risk_level == "Medium":
            return "Student shows MEDIUM risk indicators. Monitoring and support recommended."
        return "Student is at LOW risk. Academic performance is satisfactory."

    # ----------------------------------------------------------
    # NORMALIZE A DB PREDICTION RECORD
    # ----------------------------------------------------------

    @staticmethod
    def normalize_prediction_record(record):
        """
        Normalize a raw database prediction row into a consistent dict
        that all templates can use without worrying about field name differences.
        """

        if not record:
            return None

        risk_level   = dropout_predictionservice._safe_risk_level(record.get("risk_level"))
        probability  = dropout_predictionservice._safe_float(
            record.get("probability") or record.get("dropout_probability") or record.get("score") or 0
        )
        recommendation = (
            record.get("recommendation")
            or record.get("explanation")
            or dropout_predictionservice._build_recommendation(risk_level, None, None, None)
        )
        message = record.get("message") or dropout_predictionservice._build_message(risk_level)
        prediction_date = (
            record.get("predicted_on")
            or record.get("prediction_date")
            or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        # Convert datetime objects to strings
        if hasattr(prediction_date, "strftime"):
            prediction_date = prediction_date.strftime("%Y-%m-%d %H:%M:%S")

        return {
            "prediction_id":    record.get("prediction_id"),
            "student_id":       record.get("student_id"),
            "risk_level":       risk_level,
            "probability":      probability,
            "dropout_probability": probability,   # alias for template compatibility
            "score":            probability,
            "confidence_score": probability,
            "recommendation":   recommendation,
            "explanation":      recommendation,
            "suggestion":       recommendation,
            "message":          message,
            "prediction_date":  prediction_date,
            "predicted_on":     prediction_date,
            "model_version":    record.get("model_version", "v1"),
        }

    # ----------------------------------------------------------
    # LIVE PREDICTION (calls ML model)
    # ----------------------------------------------------------

    @staticmethod
    def predict_dropout(student_id):
        """
        Run live ML prediction for a student using their latest academic record.
        Does NOT write to database — use save_prediction() for that.
        """

        data = AcademicModel.get_student_academic_summary(student_id)

        if not data:
            logger.warning("No academic data found for student_id=%s", student_id)
            return {
                "student_id":      student_id,
                "prediction":      0,
                "risk_level":      "Low",
                "score":           0.0,
                "probability":     0.0,
                "dropout_probability": 0.0,
                "confidence_score": 0.0,
                "message":         "No academic data found. Please add academic records first.",
                "suggestion":      "Please add academic records to get a prediction.",
                "recommendation":  "Please add academic records to get a prediction.",
                "explanation":     "Please add academic records to get a prediction.",
                "prediction_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "predicted_on":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "model_version":   "v1",
            }

        student_features = {
            "cgpa":             float(data["cgpa"]),
            "attendance":       float(data["attendance"]),
            "internal_marks":   float(data["internal_marks"]),
            "backlog_count":    int(data["backlog_count"]),
            "study_hours":      float(data["study_hours"]),
            "family_income":    50000,
            "parent_education": 2,
            "internet_access":  1
        }

        result = MLModelService.predict(student_features)

        probability  = dropout_predictionservice._safe_float(result.get("probability") or result.get("score") or 0)
        risk_level   = dropout_predictionservice._safe_risk_level(result.get("risk_level"))
        recommendation = dropout_predictionservice._build_recommendation(
            risk_level,
            data.get("attendance"),
            data.get("backlog_count"),
            data.get("study_hours"),
            data.get("cgpa")
        )
        message          = dropout_predictionservice._build_message(risk_level)
        prediction_date  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "student_id":      int(data["student_id"]),
            "roll_no":         data.get("roll_no"),
            "department":      data.get("department"),
            "semester":        data.get("semester"),
            "cgpa":            float(data["cgpa"]),
            "attendance":      float(data["attendance"]),
            "prediction":      int(result.get("prediction") or 0),
            "risk_level":      risk_level,
            "probability":     probability,
            "dropout_probability": probability,
            "score":           probability,
            "confidence_score": probability,
            "message":         message,
            "suggestion":      recommendation,
            "recommendation":  recommendation,
            "explanation":     recommendation,
            "prediction_date": prediction_date,
            "predicted_on":    prediction_date,
            "model_version":   "v1",
        }

    # ----------------------------------------------------------
    # SAVE PREDICTION TO DATABASE
    # ----------------------------------------------------------

    @staticmethod
    def save_prediction(student_id):
        """
        Run ML prediction and save result to database.
        Returns the saved prediction dict.
        """

        prediction = dropout_predictionservice.predict_dropout(student_id)

        PredictionModel.create_prediction(
            student_id=student_id,
            prediction_result=prediction.get("prediction"),
            dropout_probability=prediction.get("probability"),
            risk_level=prediction.get("risk_level"),
            explanation=prediction.get("recommendation"),
            model_version=prediction.get("model_version", "v1")
        )

        logger.info(
            "Prediction saved: student_id=%s risk=%s prob=%.2f",
            student_id, prediction.get("risk_level"), prediction.get("probability")
        )

        return prediction

    # ----------------------------------------------------------
    # GET LATEST PREDICTION FROM DB
    # ----------------------------------------------------------

    @staticmethod
    def get_latest_prediction_db(student_id):
        """
        Fetch the latest saved prediction from the database.
        Returns normalized dict or None.
        """
        record = PredictionModel.get_latest_prediction(student_id)
        if not record:
            return None
        return dropout_predictionservice.normalize_prediction_record(record)

    # ----------------------------------------------------------
    # GET PREDICTION HISTORY FROM DB
    # ----------------------------------------------------------

    @staticmethod
    def get_prediction_history(student_id):
        """
        Fetch all saved predictions for a student from the database.
        Returns list of normalized prediction dicts.
        """
        records = PredictionModel.get_dropout_predictions_by_student(student_id)
        return [
            dropout_predictionservice.normalize_prediction_record(r)
            for r in records
            if r
        ]

    # ----------------------------------------------------------
    # GET PREDICTION BY STUDENT (live)
    # ----------------------------------------------------------

    @staticmethod
    def get_prediction_by_student(student_id):
        """
        Live ML prediction for a single student.
        Used by counsellor and admin detail views.
        """
        return dropout_predictionservice.predict_dropout(student_id)

    # ----------------------------------------------------------
    # GET ALL PREDICTIONS (live, for dashboard)
    # ----------------------------------------------------------

    @staticmethod
    def get_all_dropout_predictions():
        """
        Generate live ML predictions for every student.
        Used by counsellor dashboard and risk summary.
        """

        predictions = []
        students = StudentModel.get_all_students()

        for student in students:
            try:
                prediction = dropout_predictionservice.predict_dropout(
                    student["student_id"]
                )
                predictions.append(prediction)
            except Exception as err:
                logger.exception(
                    "Failed prediction for student_id=%s: %s",
                    student.get("student_id"), err
                )

        return predictions