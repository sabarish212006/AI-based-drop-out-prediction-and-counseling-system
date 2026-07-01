import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaGraduationCap, FaUser, FaLock } from "react-icons/fa";
import "./Login.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    if (username.trim() === "" || password.trim() === "") {
      setError("Please enter both username and password");
      return;
    }

    localStorage.setItem("isLoggedIn", "true");
    localStorage.setItem("username", username);
    navigate("/dashboard");
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-brand">
          <div className="login-logo">
            <FaGraduationCap />
          </div>
          <h1>Dropout AI</h1>
          <p>Student Dropout Prediction &amp; Counselling System</p>
        </div>

        <form onSubmit={handleLogin} className="login-form">
          {error && <div className="login-error">{error}</div>}

          <div className="input-group">
            <FaUser className="input-icon" />
            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div className="input-group">
            <FaLock className="input-icon" />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button type="submit" className="login-btn">
            Sign In
          </button>
        </form>

        <p className="login-footer">Enter any credentials to continue &mdash; demo mode</p>
      </div>
    </div>
  );
}

export default Login;