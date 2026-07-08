"""
----------------------------------------------------------
AI-Based Dropout Prediction and Counselling System
File: recommendation_service.py
Purpose: AI Counselling Recommendation Service
----------------------------------------------------------
"""


class RecommendationService:
    """
    Generates counselling recommendations
    based on student's AI prediction.
    """

    @staticmethod
    def get_recommendation(prediction):
        """
        Return counselling recommendation
        using prediction result.
        """

        risk = prediction.get("risk_level", "Low")

        if risk == "High":

            return {
                "title": "Immediate Counselling Required",
                "priority": "High",
                "color": "danger",
                "actions": [

                    "Schedule counselling session immediately.",

                    "Meet parents or guardians.",

                    "Monitor attendance every week.",

                    "Provide one-to-one mentoring.",

                    "Review academic performance regularly.",

                    "Offer psychological and motivational support.",

                    "Create an academic recovery plan."

                ]
            }

        elif risk == "Medium":

            return {
                "title": "Regular Monitoring Required",
                "priority": "Medium",
                "color": "warning",
                "actions": [

                    "Conduct monthly counselling sessions.",

                    "Monitor attendance regularly.",

                    "Track internal assessment marks.",

                    "Encourage participation in academic activities.",

                    "Provide study planning support.",

                    "Identify subjects needing improvement."

                ]
            }

        return {
            "title": "Student Performing Well",
            "priority": "Low",
            "color": "success",
            "actions": [

                "Continue current academic progress.",

                "Encourage participation in extracurricular activities.",

                "Recognize consistent performance.",

                "Maintain healthy study habits.",

                "Provide career guidance when needed."

            ]
        }

    @staticmethod
    def get_short_message(prediction):
        """
        Short recommendation message.
        """

        risk = prediction.get("risk_level", "Low")

        if risk == "High":
            return "Immediate intervention is recommended."

        if risk == "Medium":
            return "Student should be monitored periodically."

        return "Student is academically stable."

    @staticmethod
    def get_priority(risk_level):
        """
        Return recommendation priority.
        """

        if risk_level == "High":
            return "Critical"

        if risk_level == "Medium":
            return "Normal"

        return "Low"

    @staticmethod
    def get_badge_color(risk_level):
        """
        Bootstrap badge color.
        """

        if risk_level == "High":
            return "danger"

        if risk_level == "Medium":
            return "warning"

        return "success"