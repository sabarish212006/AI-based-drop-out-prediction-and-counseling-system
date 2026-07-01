import React, { useState } from "react";
import { Outlet, NavLink, useNavigate } from "react-router-dom";
import {
  FaGraduationCap,
  FaTachometerAlt,
  FaChartLine,
  FaSignOutAlt,
  FaBars,
  FaTimes
} from "react-icons/fa";
import "./Layout.css";

function Layout() {
  const navigate = useNavigate();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const username = localStorage.getItem("username") || "User";

  const handleLogout = () => {
    localStorage.removeItem("isLoggedIn");
    localStorage.removeItem("username");
    navigate("/login");
  };

  const closeSidebar = () => setSidebarOpen(false);

  return (
    <div className="layout">
      {sidebarOpen && <div className="sidebar-overlay" onClick={closeSidebar} />}

      <aside className={`sidebar ${sidebarOpen ? "open" : ""}`}>
        <div className="sidebar-brand">
          <div className="brand-icon">
            <FaGraduationCap />
          </div>
          <span>Dropout AI</span>
        </div>

        <nav className="sidebar-nav">
          <NavLink
            to="/dashboard"
            onClick={closeSidebar}
            className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
          >
            <FaTachometerAlt className="nav-icon" />
            <span>Dashboard</span>
          </NavLink>

          <NavLink
            to="/prediction"
            onClick={closeSidebar}
            className={({ isActive }) => `nav-item ${isActive ? "active" : ""}`}
          >
            <FaChartLine className="nav-icon" />
            <span>Prediction</span>
          </NavLink>
        </nav>

        <button className="logout-btn" onClick={handleLogout}>
          <FaSignOutAlt />
          <span>Logout</span>
        </button>
      </aside>

      <div className="main-area">
        <header className="topbar">
          <button className="menu-toggle" onClick={() => setSidebarOpen(!sidebarOpen)}>
            {sidebarOpen ? <FaTimes /> : <FaBars />}
          </button>
          <div className="topbar-title">Student Dropout Prediction &amp; Counselling</div>
          <div className="topbar-user">
            <div className="avatar">{username.charAt(0).toUpperCase()}</div>
            <span className="username">{username}</span>
          </div>
        </header>

        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default Layout;