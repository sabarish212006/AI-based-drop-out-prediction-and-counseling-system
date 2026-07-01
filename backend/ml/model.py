"""
Dropout risk scoring logic.
Structured so it can be swapped for a trained model (e.g. joblib .pkl)
without changing app.py — just replace predict_dropout_risk() internals.
"""

# import joblib
# model = joblib.load("ml/dropout_model.pkl")


def calculate_score(marks, attendance, gpa, study_hours, backlogs):
    score = (
        (marks * 0.3)
        + (attendance * 0.4)
        + (gpa * 25)
        + (study_hours * 2)
        - (backlogs * 5)
    )
    return round(score, 2)


def determine_risk(score):
    if score < 50:
        return "High"
    elif score < 100:
        return "Medium"
    return "Low"


def calculate_probability(score):
    max_score = 150
    probability = max(0, min(100, (score / max_score) * 100))
    return round(probability, 2)


def predict_dropout_risk(marks, attendance, gpa, study_hours, backlogs):
    score = calculate_score(marks, attendance, gpa, study_hours, backlogs)
    risk = determine_risk(score)
    probability = calculate_probability(score)

    return {
        "risk": risk,
        "score": score,
        "probability": probability
    }