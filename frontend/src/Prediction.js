import React, { useState } from "react";
import api from "./api";
import {
  FaChartLine,
  FaCalendarCheck,
  FaBook,
  FaClock,
  FaExclamationCircle,
  FaBrain
} from "react-icons/fa";
import "./Prediction.css";

const initialForm = {
  marks: "",
  attendance: "",
  gpa: "",
  study_hours: "",
  backlogs: ""
};

function Prediction() {
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);

    for (const key in form) {
      if (form[key] === "") {
        setError("Please fill in all fields before predicting.");
        return;
      }
    }

    setLoading(true);
    try {
      const payload = {
        marks: parseFloat(form.marks),
        attendance: parseFloat(form.attendance),
        gpa: parseFloat(form.gpa),
        study_hours: parseFloat(form.study_hours),
        backlogs: parseFloat(form.backlogs)
      };

      const response = await api.post("/predict", payload);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || "Prediction failed. Check backend connection.");
    } finally {
      setLoading(false);
    }
  };

  const riskClass = (risk) => {
    if (risk === "High") return "high";
    if (risk === "Medium") return "medium";
    return "low";
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Dropout Risk Prediction</h1>
          <p className="page-subtitle">
            Enter student metrics to generate an instant AI-based risk assessment
          </p>
        </div>
      </div>

      <div className="prediction-grid">
        <form className="prediction-form" onSubmit={handleSubmit}>
          <div className="form-field">
            <label><FaChartLine className="field-icon" /> Marks (%)</label>
            <input
              type="number"
              name="marks"
              value={form.marks}
              onChange={handleChange}
              placeholder="e.g. 75"
            />
          </div>

          <div className="form-field">
            <label><FaCalendarCheck className="field-icon" /> Attendance (%)</label>
            <input
              type="number"
              name="attendance"
              value={form.attendance}
              onChange={handleChange}
              placeholder="e.g. 80"
            />
          </div>

          <div className="form-field">
            <label><FaBook className="field-icon" /> GPA (0-4)</label>
            <input
              type="number"
              step="0.01"
              name="gpa"
              value={form.gpa}
              onChange={handleChange}
              placeholder="e.g. 3.2"
            />
          </div>

          <div className="form-field">
            <label><FaClock className="field-icon" /> Study Hours (per day)</label>
            <input
              type="number"
              name="study_hours"
              value={form.study_hours}
              onChange={handleChange}
              placeholder="e.g. 3"
            />
          </div>

          <div className="form-field">
            <label><FaExclamationCircle className="field-icon" /> Backlogs</label>
            <input
              type="number"
              name="backlogs"
              value={form.backlogs}
              onChange={handleChange}
              placeholder="e.g. 1"
            />
          </div>

          {error && <div className="form-error">{error}</div>}

          <button type="submit" className="predict-btn" disabled={loading}>
            {loading ? "Predicting..." : "Predict Risk"}
          </button>
        </form>

        <div className="result-panel">
          {!result && !loading && (
            <div className="result-placeholder">
              <FaBrain className="placeholder-icon" />
              <p>Fill the form and click "Predict Risk" to see the AI assessment here.</p>
            </div>
          )}

          {loading && <div className="state-msg">Analyzing student data...</div>}

          {result && !loading && (
            <div className={`result-card ${riskClass(result.risk)}`}>
              <span className="result-tag">{result.risk} Risk</span>
              <div className="result-metrics">
                <div className="metric">
                  <span className="metric-label">Score</span>
                  <span className="metric-value">{result.score}</span>
                </div>
                <div className="metric">
                  <span className="metric-label">Success Probability</span>
                  <span className="metric-value">{result.probability}%</span>
                </div>
              </div>
              <div className="probability-bar">
                <div
                  className="probability-fill"
                  style={{ width: `${result.probability}%` }}
                />
              </div>
              <p className="result-note">
                {result.risk === "High" &&
                  "This student needs immediate counselling and academic support."}
                {result.risk === "Medium" &&
                  "This student should be monitored and offered guidance sessions."}
                {result.risk === "Low" &&
                  "This student is performing well and on track for success."}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Prediction;