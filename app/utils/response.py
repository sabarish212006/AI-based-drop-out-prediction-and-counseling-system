"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: response.py
Purpose: Standard JSON Response Helper
----------------------------------------------------------
"""

from flask import jsonify


def success_response(
    message="Success",
    data=None,
    status_code=200
):
    """
    Standard success response.

    Example:
    {
        "success": true,
        "message": "Student created successfully.",
        "data": {...}
    }
    """

    response = {
        "success": True,
        "message": message,
        "data": data if data is not None else {}
    }

    return jsonify(response), status_code


def error_response(
    message="Something went wrong.",
    status_code=400,
    errors=None
):
    """
    Standard error response.

    Example:
    {
        "success": false,
        "message": "...",
        "errors": {...}
    }
    """

    response = {
        "success": False,
        "message": message,
        "errors": errors if errors is not None else {}
    }

    return jsonify(response), status_code


def validation_error_response(errors):
    """
    Shortcut for validation errors.

    Example:
    {
        "success": false,
        "message": "Validation failed.",
        "errors": {
            "email": "Invalid email",
            "cgpa": "CGPA must be between 0 and 10"
        }
    }
    """

    return error_response(
        message="Validation failed.",
        status_code=422,
        errors=errors
    )