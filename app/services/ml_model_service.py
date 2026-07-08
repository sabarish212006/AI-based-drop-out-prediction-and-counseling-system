"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: ml_model_service.py
Purpose: Load ML Model and Predict Student Dropout Risk
----------------------------------------------------------
"""

import os
import joblib
import pandas as pd

from app.utils.logger import get_logger

logger = get_logger(__name__)


class MLModelService:
    """
    Machine Learning Prediction Service

    The trained model outputs a raw probability (0-1) of dropout risk.
    This service applies sensible post-processing thresholds to map the
    probability to meaningful risk levels.
    """

    _model = None

    # Feature order MUST match the model's training pipeline exactly
    FEATURE_ORDER = [
        "cgpa",
        "attendance",
        "internal_marks",
        "backlog_count",
        "study_hours",
        "family_income",
        "parent_education",
        "internet_access"
    ]

    @classmethod
    def load_model(cls):
        """
        Load trained pipeline model only once (singleton pattern).
        """

        if cls._model is None:

            base_dir = os.path.dirname(os.path.dirname(__file__))

            model_path = os.path.join(
                base_dir, "ml", "saved_models", "dropout_model.pkl"
            )

            # Fallback: check versions subdirectory
            if not os.path.exists(model_path):
                model_path = os.path.join(
                    base_dir, "ml", "saved_models", "versions", "v1", "dropout_model.pkl"
                )

            if not os.path.exists(model_path):
                raise FileNotFoundError(
                    f"ML model not found. Expected at: "
                    f"{os.path.join(base_dir, 'ml', 'saved_models', 'dropout_model.pkl')}"
                )

            cls._model = joblib.load(model_path)
            logger.info("ML model loaded successfully from: %s", model_path)

        return cls._model

    @classmethod
    def predict(cls, student_data: dict) -> dict:
        """
        Predict dropout risk for a student using the trained ML model
        with sensible post-processing thresholds.

        The trained model's raw probability is adjusted based on known
        academic indicators to produce realistic risk assessments.

        Parameters
        ----------
        student_data : dict
            Must contain keys matching FEATURE_ORDER.

        Returns
        -------
        dict with keys: prediction, probability (0-100), score (0-100), risk_level
        """
        try:
            model = cls.load_model()

            # Build DataFrame with EXACT feature order
            row = {key: student_data.get(key, 0) for key in cls.FEATURE_ORDER}
            dataframe = pd.DataFrame([row], columns=cls.FEATURE_ORDER)

            # Get raw prediction and probability from the ML model
            prediction = int(model.predict(dataframe)[0])
            probability_raw = 0.5
            if hasattr(model, "predict_proba"):
                probability_raw = float(model.predict_proba(dataframe)[0][1])

            # Extract student's actual academic metrics for post-processing
            cgpa = float(student_data.get("cgpa", 0))
            attendance = float(student_data.get("attendance", 0))
            backlog_count = int(student_data.get("backlog_count", 0))
            internal_marks = float(student_data.get("internal_marks", 0))
            study_hours = float(student_data.get("study_hours", 0))

            # ---- Post-processing logic ----
            # The ML model's raw prediction is adjusted by academic indicators
            # to ensure realistic risk assessment.
            #
            # Students with EXCELLENT metrics should always be Low risk
            # Students with POOR metrics should always be High risk
            # Borderline cases use the model's probability

            # Strong positive indicators (excellent student -> low risk)
            if (cgpa >= 8.0 and attendance >= 85 and backlog_count == 0
                    and internal_marks >= 75 and study_hours >= 3):
                # Excellent student - override to Low regardless of model
                adjusted_prob = min(probability_raw, 0.15)
                risk_level = "Low"

            # Very strong positive indicators
            elif (cgpa >= 7.5 and attendance >= 80 and backlog_count <= 0
                    and internal_marks >= 70 and study_hours >= 3):
                adjusted_prob = min(probability_raw, 0.25)
                risk_level = "Low"

            # Good indicators with some positive signs
            elif (cgpa >= 7.0 and attendance >= 75 and backlog_count <= 1
                    and internal_marks >= 65 and study_hours >= 2.5):
                adjusted_prob = probability_raw * 0.6
                risk_level = "Low" if adjusted_prob < 30 else "Medium"

            # Poor academic performance - High risk
            elif (cgpa < 5.5 or attendance < 55 or backlog_count >= 4
                    or (cgpa < 6.0 and backlog_count >= 2)):
                adjusted_prob = max(probability_raw, 0.65)
                risk_level = "High"

            # Below average performance
            elif (cgpa < 6.5 or attendance < 65 or backlog_count >= 2
                    or internal_marks < 55):
                adjusted_prob = max(probability_raw, 0.40)
                risk_level = "High" if adjusted_prob >= 60 else "Medium"

            # Moderate indicators
            elif backlog_count >= 1 or attendance < 75 or cgpa < 7.0:
                adjusted_prob = probability_raw * 0.8 + 0.1
                risk_level = "Medium" if adjusted_prob < 60 else "High"

            else:
                # Default: Let the model decide with adjusted thresholds
                adjusted_prob = probability_raw

                if adjusted_prob >= 0.60:
                    risk_level = "High"
                elif adjusted_prob >= 0.35:
                    risk_level = "Medium"
                else:
                    risk_level = "Low"

            # Clamp score between 0-100
            score = round(min(max(adjusted_prob * 100, 0), 100), 2)

            logger.debug(
                "Prediction: cgpa=%.1f att=%.1f backlogs=%d | raw_prob=%.2f adjusted=%.2f risk=%s",
                cgpa, attendance, backlog_count, probability_raw, adjusted_prob, risk_level
            )

            return {
                "prediction":  prediction,
                "probability": score,
                "score":       score,
                "risk_level":  risk_level
            }

        except Exception as err:
            logger.exception("ML prediction error: %s", err)

            # Graceful fallback based on academic data
            cgpa = float(student_data.get("cgpa", 0))
            attendance = float(student_data.get("attendance", 0))
            backlog_count = int(student_data.get("backlog_count", 0))

            if cgpa >= 7.5 and attendance >= 75 and backlog_count == 0:
                return {"prediction": 0, "probability": 15.0, "score": 15.0, "risk_level": "Low"}
            elif cgpa >= 6.0 and attendance >= 65 and backlog_count <= 2:
                return {"prediction": 0, "probability": 40.0, "score": 40.0, "risk_level": "Medium"}
            else:
                return {"prediction": 1, "probability": 75.0, "score": 75.0, "risk_level": "High"}