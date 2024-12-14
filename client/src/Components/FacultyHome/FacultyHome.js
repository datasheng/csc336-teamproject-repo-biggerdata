import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./FacultyHome.css";

const FacultyHome = ({ setIsLoggedIn }) => {
  const [isActive, setIsActive] = useState("main");


  const handleLogout = () => {
    if (window.confirm("Are you sure you want to log out?")) {
      setIsLoggedIn(false);
    }
  };

  // Handles active tab
  // Navigate to respective when the 'browse' or 'schedule' tab is active
  const handleClick = (tab) => {
    setIsActive(tab);
  };

  return (
    <div className="course-registration-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2>Navigation</h2>
        <ul>
          <li onClick={() => handleClick("main")}
              style={{ backgroundColor: isActive === "main" ? "#014303" : "transparent" }}>
            Course Overview
          </li>
          <li onClick={() => handleClick("student")}
              style={{ backgroundColor: isActive === "student" ? "#014303" : "transparent" }}>
            Student Enrollment
          </li>
          <li onClick={() => handleClick("schedule")}
              style={{ backgroundColor: isActive === "schedule" ? "#014303" : "transparent" }}>
            Schedule
          </li>
          
          <li onClick={handleLogout}>Logout</li>
        </ul>
      </aside>

      {/* Main Content */}
      <main className="content">
        <div className="content-section">
          {/* Conditional rendering for the 'main' tab */}
          {isActive === 'main' && (
            <>
              <h1>Welcome to CourseFlow's Faculty Portal!</h1>
              <h2>My Courses</h2>
              <ul>
                <li>Database Systems</li>
              </ul>
            </>
          )}
        </div>
      </main>
    </div>
  );
};

export default FacultyHome;
