"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: academic_service.py
Purpose: Academic Business Logic Layer
----------------------------------------------------------
"""

from app.models.academic_model import AcademicModel
from app.models.prediction_model import PredictionModel
from app.services.prediction_service import dropout_predictionservice


class AcademicService:
    """
    Handles academic business logic,
    validation, and processing.
    """

    # ==========================================
    # Validation Helpers
    # ==========================================

    @staticmethod
    def validate_semester_year(semester, year_of_study):
        """
        Validate semester matches the student's year of study.

        Year 1 -> Semesters 1-2
        Year 2 -> Semesters 3-4
        Year 3 -> Semesters 5-6
        Year 4 -> Semesters 7-8

        Returns error string or None if valid.
        """
        valid_ranges = {
            1: (1, 2),
            2: (3, 4),
            3: (5, 6),
            4: (7, 8)
        }

        if year_of_study not in valid_ranges:
            return f"Invalid year of study: {year_of_study}. Must be 1-4."

        min_sem, max_sem = valid_ranges[year_of_study]
        if semester < min_sem or semester > max_sem:
            return (
                f"Semester {semester} does not match Year {year_of_study}. "
                f"Year {year_of_study} allows Semesters {min_sem}-{max_sem} only. "
                f"For example: Year 1 → Sem 1-2, Year 2 → Sem 3-4, "
                f"Year 3 → Sem 5-6, Year 4 → Sem 7-8."
            )
        return None

    @staticmethod
    def derive_year_from_semester(semester):
        """
        Automatically derive the year of study from a given semester.

        Semesters 1-2  -> Year 1
        Semesters 3-4  -> Year 2
        Semesters 5-6  -> Year 3
        Semesters 7-8  -> Year 4

        Returns year (int) or None if semester is invalid (not 1-8).
        """
        if 1 <= semester <= 2:
            return 1
        elif 3 <= semester <= 4:
            return 2
        elif 5 <= semester <= 6:
            return 3
        elif 7 <= semester <= 8:
            return 4
        return None

    @staticmethod
    def validate_academic_data(
        cgpa,
        attendance,
        internal_marks,
        backlog_count,
        study_hours
    ):
        """
        Validate academic input values.
        """

        errors = []

        if cgpa < 0 or cgpa > 10:
            errors.append("CGPA must be between 0 and 10.")

        if attendance < 0 or attendance > 100:
            errors.append("Attendance must be between 0 and 100.")

        if internal_marks < 0 or internal_marks > 100:
            errors.append("Internal marks must be between 0 and 100.")

        if backlog_count < 0:
            errors.append("Backlog count cannot be negative.")

        if study_hours < 0 or study_hours > 24:
            errors.append("Study hours must be between 0 and 24.")

        return errors

    # ==========================================
    # CRUD Operations
    # ==========================================

    @staticmethod
    def add_academic_record(
        student_id,
        semester,
        cgpa,
        attendance,
        internal_marks,
        backlog_count,
        study_hours,
        year_of_study=None
    ):
        """
        Add academic record after validation.

        If a record for the same student and semester already exists,
        it will be updated instead of inserting a duplicate.

        If year_of_study is provided, validates semester matches the year.
        If not provided, the student's year_of_study will be auto-derived
        from the semester if possible.
        """

        errors = AcademicService.validate_academic_data(
            cgpa,
            attendance,
            internal_marks,
            backlog_count,
            study_hours
        )

        if errors:
            return {
                "success": False,
                "message": "Validation failed.",
                "errors": errors
            }

        # Validate or auto-derive year from semester
        if year_of_study is not None:
            year_error = AcademicService.validate_semester_year(semester, year_of_study)
            if year_error:
                return {
                    "success": False,
                    "message": year_error,
                    "errors": [year_error]
                }
        else:
            # Auto-derive year from semester and update student record
            from app.models.student_model import StudentModel
            student = StudentModel.get_student_by_id(student_id)
            if student:
                derived_year = AcademicService.derive_year_from_semester(semester)
                if derived_year and student.get("year_of_study") != derived_year:
                    # Update the student's year of study to match the semester
                    StudentModel.update_student(
                        student_id=student_id,
                        department=student.get("department"),
                        year_of_study=derived_year,
                        gender=student.get("gender"),
                        date_of_birth=student.get("date_of_birth"),
                        address=student.get("address")
                    )

        # Check if a record already exists for this student and semester
        existing = AcademicModel.get_record_by_student_semester(
            student_id, semester
        )

        if existing:
            # Update the existing record instead of inserting a duplicate
            AcademicModel.update_academic_record(
                academic_id=existing["academic_id"],
                semester=semester,
                cgpa=cgpa,
                attendance=attendance,
                internal_marks=internal_marks,
                backlog_count=backlog_count,
                study_hours=study_hours
            )

            # Generate prediction using existing prediction service
            try:
                prediction = dropout_predictionservice.predict_dropout(student_id)
                if isinstance(prediction, dict):
                    prediction_result = prediction.get("prediction")
                    probability = prediction.get("score")
                    risk_level = prediction.get("risk_level")
                    explanation = (
                        (prediction.get("message") or "") + " | " +
                        (prediction.get("recommendation") or "")
                    )
                    model_version = prediction.get("model_version", "v1")

                    PredictionModel.create_prediction(
                        student_id=student_id,
                        prediction_result=prediction_result,
                        dropout_probability=probability,
                        risk_level=risk_level,
                        explanation=explanation,
                        model_version=model_version
                    )
            except Exception:
                # Do not fail academic update if prediction saving fails
                pass

            return {
                "success": True,
                "message": "Academic record updated successfully."
            }

        # No existing record - insert new one
        inserted_id = AcademicModel.create_academic_record(
            student_id,
            semester,
            cgpa,
            attendance,
            internal_marks,
            backlog_count,
            study_hours
        )

        if not inserted_id:
            return {
                "success": False,
                "message": "Failed to save academic record."
            }

        # Generate prediction using existing prediction service (reuse logic)
        try:
            prediction = dropout_predictionservice.predict_dropout(student_id)

            if isinstance(prediction, dict):
                risk_level = prediction.get("risk_level")
                probability = prediction.get("score")
                explanation = prediction.get("suggestion")
                prediction_result = prediction.get("prediction")

                # Persist prediction to DB
                PredictionModel.create_prediction(
                    student_id=student_id,
                    prediction_result=prediction_result,
                    dropout_probability=probability,
                    risk_level=risk_level,
                    explanation=(
                        (prediction.get("message") or "") + " | " +
                        (prediction.get("recommendation") or "")
                    ),
                    model_version=prediction.get("model_version", "v1")
                )
        except Exception:
            # Do not fail academic insert if prediction saving fails; log via model layer
            pass

        return {
            "success": True,
            "message": "Academic record created successfully."
        }

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
        Update academic record after validation.
        """

        if not AcademicModel.academic_record_exists(academic_id):
            return {
                "success": False,
                "message": "Academic record not found."
            }

        errors = AcademicService.validate_academic_data(
            cgpa,
            attendance,
            internal_marks,
            backlog_count,
            study_hours
        )

        if errors:
            return {
                "success": False,
                "message": "Validation failed.",
                "errors": errors
            }

        # Fetch the record to get student_id for year-semester validation
        record = AcademicModel.get_record_by_id(academic_id)
        if record:
            from app.models.student_model import StudentModel
            student = StudentModel.get_student_by_id(record["student_id"])
            if student and student.get("year_of_study"):
                year_error = AcademicService.validate_semester_year(
                    semester, student["year_of_study"]
                )
                if year_error:
                    return {
                        "success": False,
                        "message": year_error,
                        "errors": [year_error]
                    }
                # Also auto-derive and update year if needed
                derived_year = AcademicService.derive_year_from_semester(semester)
                if derived_year and student.get("year_of_study") != derived_year:
                    StudentModel.update_student(
                        student_id=record["student_id"],
                        department=student.get("department"),
                        year_of_study=derived_year,
                        gender=student.get("gender"),
                        date_of_birth=student.get("date_of_birth"),
                        address=student.get("address")
                    )

        AcademicModel.update_academic_record(
            academic_id,
            semester,
            cgpa,
            attendance,
            internal_marks,
            backlog_count,
            study_hours
        )

        return {
            "success": True,
            "message": "Academic record updated successfully."
        }

    @staticmethod
    def delete_academic_record(academic_id):
        """
        Delete academic record safely.
        """

        if not AcademicModel.academic_record_exists(academic_id):
            return {
                "success": False,
                "message": "Academic record not found."
            }

        AcademicModel.delete_academic_record(academic_id)

        return {
            "success": True,
            "message": "Academic record deleted successfully."
        }

    # ==========================================
    # Data Retrieval
    # ==========================================

    @staticmethod
    def get_student_records(student_id):
        """
        Get all academic records for a student.
        """

        return AcademicModel.get_records_by_student(student_id)

    @staticmethod
    def get_latest_record(student_id):
        """
        Get latest academic record for prediction.
        """

        return AcademicModel.get_latest_record(student_id)

    @staticmethod
    def get_student_summary(student_id):
        """
        Get student academic summary for ML prediction.
        """

        return AcademicModel.get_student_academic_summary(student_id)

    @staticmethod
    def get_all_records():
        """
        Get all academic records (admin use).
        """

        return AcademicModel.get_all_records()