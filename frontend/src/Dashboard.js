import React, { useEffect, useState } from "react";
import api from "./api";
import { FaUserGraduate, FaExclamationTriangle, FaTrophy, FaSyncAlt } from "react-icons/fa";
import "./Dashboard.css";

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await api.get("/stats");
      setStats(response.data);
    } catch (err) {
      setError("Failed to load stats. Make sure the backend is running on port 5000.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Dashboard</h1>
          <p className="page-subtitle">Overview of student performance and risk levels</p>
        </div>
        <button className="refresh-btn" onClick={fetchStats}>
          <FaSyncAlt className={loading ? "spin" : ""} /> Refresh
        </button>
      </div>

      {loading && <div className="state-msg">Loading dashboard...</div>}
      {error && <div className="state-msg error">{error}</div>}

      {!loading && !error && stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon students">
              <FaUserGraduate />
            </div>
            <div className="stat-info">
              <span className="stat-label">Total Students</span>
              <span className="stat-value">{stats.students}</span>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon at-risk">
              <FaExclamationTriangle />
            </div>
            <div className="stat-info">
              <span className="stat-label">At Risk</span>
              <span className="stat-value">{stats.at_risk}</span>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon success">
              <FaTrophy />
            </div>
            <div className="stat-info">
              <span className="stat-label">Success Rate</span>
              <span className="stat-value">{stats.success_rate}%</span>
            </div>
          </div>
        </div>
      )}

      <div className="info-panel">
        <h3>About This System</h3>
        <p>
          This dashboard gives a live snapshot of student engagement across the institution.
          Use the Prediction page to assess an individual student's dropout risk based on
          academic marks, attendance, GPA, study habits, and backlog history, then follow up
          with targeted counselling for students flagged as Medium or High risk.
        </p>
      </div>
    </div>
  );
}

export default Dashboard;