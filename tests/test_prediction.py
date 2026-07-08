from app.models.base import BaseModel
from app.services.prediction_service import dropout_predictionservice


def test_predict_dropout_returns_complete_prediction(monkeypatch):
    monkeypatch.setattr(
        "app.services.prediction_service.AcademicModel.get_student_academic_summary",
        lambda student_id: {
            "student_id": student_id,
            "roll_no": "23CSE001",
            "department": "Computer Science",
            "semester": 6,
            "cgpa": 8.5,
            "attendance": 91.0,
            "internal_marks": 88.0,
            "backlog_count": 0,
            "study_hours": 4.5,
        },
    )
    monkeypatch.setattr(
        "app.services.prediction_service.MLModelService.predict",
        lambda student_data: {
            "prediction": 1,
            "score": 92.5,
            "risk_level": "High",
        },
    )

    result = dropout_predictionservice.predict_dropout(1)

    assert result["risk_level"] == "High"
    assert result["probability"] == 92.5
    assert result["confidence_score"] == 92.5
    assert result["recommendation"]
    assert result["message"]
    assert result["prediction_date"]


def test_normalize_prediction_record_fills_missing_values():
    record = {
        "prediction_id": 10,
        "risk_level": None,
        "dropout_probability": None,
        "explanation": None,
        "predicted_on": None,
    }

    normalized = dropout_predictionservice.normalize_prediction_record(record)

    assert normalized["risk_level"] == "Low"
    assert normalized["probability"] == 0.0
    assert normalized["confidence_score"] == 0.0
    assert normalized["recommendation"]
    assert normalized["message"]
    assert normalized["prediction_date"]


def test_execute_query_handles_rollback_errors(monkeypatch):
    class DummyCursor:
        def execute(self, query, params=None):
            raise RuntimeError("db down")

        def close(self):
            return None

    class DummyConnection:
        def cursor(self, *args, **kwargs):
            return DummyCursor()

        def rollback(self):
            raise RuntimeError("rollback failed")

        def close(self):
            return None

    monkeypatch.setattr("app.models.base.get_db_connection", lambda: DummyConnection())

    assert BaseModel.execute_query("INSERT INTO test VALUES (1)") is None
