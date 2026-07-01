from flask import Flask, request, jsonify
from flask_cors import CORS
from ml.model import predict_dropout_risk

app = Flask(__name__)
CORS(app)

STATS = {
    "students": 120,
    "at_risk": 25,
    "success_rate": 85
}


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "AI Student Dropout Prediction & Counselling API is running"})


@app.route("/stats", methods=["GET"])
def get_stats():
    return jsonify(STATS), 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)

        required_fields = ["marks", "attendance", "gpa", "study_hours", "backlogs"]
        for field in required_fields:
            if field not in data or data[field] in ("", None):
                return jsonify({"error": f"Missing field: {field}"}), 400

        marks = float(data["marks"])
        attendance = float(data["attendance"])
        gpa = float(data["gpa"])
        study_hours = float(data["study_hours"])
        backlogs = float(data["backlogs"])

        result = predict_dropout_risk(marks, attendance, gpa, study_hours, backlogs)
        return jsonify(result), 200

    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)