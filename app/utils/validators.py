"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: validators.py
Purpose: Common Validation Functions
----------------------------------------------------------
"""

import re


class Validator:
    """
    Common validation methods used throughout the project.
    """

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""

        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return bool(re.fullmatch(pattern, email.strip()))

    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Password Rules:
        Minimum 8 characters
        At least one uppercase
        At least one lowercase
        At least one digit
        At least one special character
        """

        pattern = (
            r"^(?=.*[a-z])"
            r"(?=.*[A-Z])"
            r"(?=.*\d)"
            r"(?=.*[@$!%*?&])"
            r"[A-Za-z\d@$!%*?&]{8,}$"
        )

        return bool(re.fullmatch(pattern, password))

    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate Indian mobile number.
        """

        pattern = r"^[6-9]\d{9}$"
        return bool(re.fullmatch(pattern, phone))

    @staticmethod
    def validate_name(name: str) -> bool:
        """
        Allow alphabets and spaces only.
        """

        pattern = r"^[A-Za-z ]{2,100}$"
        return bool(re.fullmatch(pattern, name.strip()))

    @staticmethod
    def validate_age(age) -> bool:
        """
        Valid age between 15 and 100.
        """

        try:
            age = int(age)
            return 15 <= age <= 100
        except (TypeError, ValueError):
            return False

    @staticmethod
    def validate_attendance(attendance) -> bool:
        """
        Attendance percentage (0–100).
        """

        try:
            attendance = float(attendance)
            return 0 <= attendance <= 100
        except (TypeError, ValueError):
            return False

    @staticmethod
    def validate_cgpa(cgpa) -> bool:
        """
        CGPA between 0 and 10.
        """

        try:
            cgpa = float(cgpa)
            return 0 <= cgpa <= 10
        except (TypeError, ValueError):
            return False

    @staticmethod
    def validate_income(income) -> bool:
        """
        Family annual income cannot be negative.
        """

        try:
            income = float(income)
            return income >= 0
        except (TypeError, ValueError):
            return False

    @staticmethod
    def validate_required(value) -> bool:
        """
        Check required field.
        """

        return value is not None and str(value).strip() != ""

    @staticmethod
    def validate_student_rollno(roll_no: str) -> bool:
        """
        Student Roll Number:
        5–20 characters,
        letters, numbers, underscore and hyphen allowed.
        """

        pattern = r"^[A-Za-z0-9_-]{5,20}$"
        return bool(re.fullmatch(pattern, roll_no.strip()))