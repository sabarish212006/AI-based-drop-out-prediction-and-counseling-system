"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: report_service.py
Purpose: Analytics & Reporting Layer
----------------------------------------------------------
"""

from app.models.academic_model import AcademicModel
from app.models.counselling_model import CounsellingModel
from app.models.notification_model import NotificationModel
from app.models.prediction_model import PredictionModel
from app.models.student_model import StudentModel
from app.models.user_model import UserModel
from app.utils.db_helper import get_db_connection


class ReportService:
    """
    Generates reports for Admin Dashboard,
    Counsellor Dashboard and Analytics.
    """

    @staticmethod
    def get_prediction_summary():

        predictions = PredictionModel.get_all_dropout_predictions()

        total = len(predictions)

        high = 0
        medium = 0
        low = 0
        avg_probability = 0.0
        highest_probability = 0.0
        lowest_probability = 0.0
        trend = []

        for p in predictions:

            risk = p.get("risk_level", "Low")
            probability = p.get("probability") or p.get("dropout_probability") or p.get("score") or 0
            avg_probability += float(probability)
            highest_probability = max(highest_probability, float(probability))
            lowest_probability = min(lowest_probability or float(probability), float(probability))
            trend.append(float(probability))

            if risk == "High":
                high += 1

            elif risk == "Medium":
                medium += 1

            else:
                low += 1

        if total:
            avg_probability = round(avg_probability / total, 2)
            lowest_probability = lowest_probability or 0.0
        else:
            avg_probability = 0.0
            highest_probability = 0.0
            lowest_probability = 0.0

        return {

            "total": total,
            "high": high,
            "medium": medium,
            "low": low,
            "average_probability": avg_probability,
            "highest_probability": round(highest_probability, 2),
            "lowest_probability": round(lowest_probability, 2),
            "prediction_trend": trend,
            # Backward compatibility
            "total_dropout_predictions": total,
            "high_risk": high,
            "medium_risk": medium,
            "low_risk": low

        }

    @staticmethod
    def get_academic_summary():

        records = AcademicModel.get_all_records()

        if not records:

            return {

                "total_records": 0,

                "average_cgpa": 0,

                "average_attendance": 0

            }

        total = len(records)

        avg_cgpa = sum(
            float(r.get("cgpa", 0))
            for r in records
        ) / total

        avg_attendance = sum(
            float(r.get("attendance", 0))
            for r in records
        ) / total

        return {

            "total_records": total,

            "average_cgpa": round(avg_cgpa, 2),

            "average_attendance": round(avg_attendance, 2)

        }

    @staticmethod
    def get_risk_distribution():

        summary = ReportService.get_prediction_summary()

        return {

            "High": summary["high"],

            "Medium": summary["medium"],

            "Low": summary["low"]

        }

    @staticmethod
    def get_department_risk_distribution():
        """
        Group risk counts by department for admin charts.
        """

        query = """
        SELECT
            s.department,
            SUM(CASE WHEN p.risk_level = 'High' THEN 1 ELSE 0 END) AS high_count,
            SUM(CASE WHEN p.risk_level = 'Medium' THEN 1 ELSE 0 END) AS medium_count,
            SUM(CASE WHEN p.risk_level = 'Low' THEN 1 ELSE 0 END) AS low_count
        FROM students s
        LEFT JOIN dropout_predictions p
            ON s.student_id = p.student_id
        GROUP BY s.department
        ORDER BY s.department
        """

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception:
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def get_year_student_count():
        """
        Count active students by year.
        """

        query = """
        SELECT
            year_of_study,
            COUNT(*) AS student_count
        FROM students
        GROUP BY year_of_study
        ORDER BY year_of_study
        """

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception:
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def get_average_metrics_by_department():
        """
        Get average CGPA and attendance grouped by department.
        """

        query = """
        SELECT
            s.department,
            ROUND(AVG(a.cgpa), 2) AS average_cgpa,
            ROUND(AVG(a.attendance), 2) AS average_attendance
        FROM students s
        INNER JOIN academic_records a ON s.student_id = a.student_id
        GROUP BY s.department
        ORDER BY s.department
        """

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query)
            return cursor.fetchall()
        except Exception:
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def get_recent_academic_records(limit=5):
        """
        Fetch the latest academic records.
        """

        query = """
        SELECT
            a.academic_id,
            a.student_id,
            s.roll_no,
            s.department,
            s.year_of_study,
            a.semester,
            a.cgpa,
            a.attendance,
            a.internal_marks,
            a.backlog_count,
            a.study_hours,
            a.semester
        FROM academic_records a
        INNER JOIN students s ON a.student_id = s.student_id
        ORDER BY a.semester DESC
        LIMIT %s
        """

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (limit,))
            return cursor.fetchall()
        except Exception:
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def get_recent_predictions(limit=5):
        """
        Fetch the latest saved prediction records.
        """

        query = """
        SELECT
            p.prediction_id,
            p.student_id,
            s.roll_no,
            s.department,
            s.year_of_study,
            p.risk_level,
            p.probability,
            p.predicted_on
        FROM dropout_predictions p
        INNER JOIN students s ON p.student_id = s.student_id
        ORDER BY p.predicted_on DESC
        LIMIT %s
        """

        connection = None
        cursor = None

        try:
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, (limit,))
            return cursor.fetchall()
        except Exception:
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @staticmethod
    def get_dashboard_stats():
        """
        Dashboard statistics used by

        Admin Dashboard

        Counsellor Dashboard

        Reports

        Excel Export

        PDF Export

        APIs
        """

        students = UserModel.get_users_by_role("Student")
        counsellors = UserModel.get_users_by_role("Counsellor")
        prediction = ReportService.get_prediction_summary()
        academic = ReportService.get_academic_summary()

        return {
            # Dashboard Cards
            "total_students": len(students),
            "total_counsellors": len(counsellors),
            "total_predictions": prediction["total"],
            "high_risk_students": prediction["high"],
            "medium_risk_students": prediction["medium"],
            "low_risk_students": prediction["low"],
            "average_cgpa": academic["average_cgpa"],
            "average_attendance": academic["average_attendance"],
            "average_probability": prediction["average_probability"],
            "highest_probability": prediction["highest_probability"],
            "lowest_probability": prediction["lowest_probability"],
            "prediction_trend": prediction["prediction_trend"],
            # Reports
            "prediction_summary": prediction,
            "academic_summary": academic,
            "risk_distribution": {
                "High": prediction["high"],
                "Medium": prediction["medium"],
                "Low": prediction["low"]
            },
            "department_risk_distribution": ReportService.get_department_risk_distribution(),
            "year_student_count": ReportService.get_year_student_count(),
            "average_by_department": ReportService.get_average_metrics_by_department(),
            "recent_students": StudentModel.get_recent_students(5),
            "recent_academic_records": ReportService.get_recent_academic_records(5),
            "recent_predictions": ReportService.get_recent_predictions(5),
            "recent_counselling_notes": CounsellingModel.get_recent_notes(5),
            "recent_notifications": NotificationModel.get_all_notifications()[:5]
        }