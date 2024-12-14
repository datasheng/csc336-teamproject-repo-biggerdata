import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Browse from '../Browse/Browse';
import Schedule from "../Schedule/Schedule";
import "./Homepage.css";

const Homepage = ({ setIsLoggedIn }) => {
  const [isActive, setIsActive] = useState("main");
  const navigate = useNavigate();

  // Manages multiple dropdowns
  const [dropdowns, setDropdowns] = useState({
    personal: false,
    university: false,
  });

  const handleLogout = () => {
    if (window.confirm("Are you sure you want to log out?")) {
      setIsLoggedIn(false);
    }
  };

  // Handles active tab
  // Navigate to respective when the 'browse' or 'schedule' tab is active
  const handleClick = (tab) => {
    setIsActive(tab);
    if (tab === "browse") navigate("/browse");
    if (tab === "schedule") navigate("/schedule_build");
  };

  // Toggles the specific dropdown
  const handleDropdownToggle = (dropdown) => {
    setDropdowns((prevState) => ({
      ...prevState,
      [dropdown]: !prevState[dropdown],
    }));
  };

  return (
    <div className="course-registration-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2>Navigation</h2>
        <ul>
          <li onClick={() => handleClick("main")}
              style={{ backgroundColor: isActive === "main" ? "#1b4199" : "transparent" }}>
            Home Page
          </li>
          <li onClick={() => handleClick("browse")}>Browse Courses</li> {/* Can view courses here */}
          
          <li onClick={() => handleClick("schedule")}>View Schedule</li> {/* Schedule view + cart here */}
          
          <li onClick={() => handleClick("profile")}
              style={{ backgroundColor: isActive === "profile" ? "#1b4199" : "transparent" }}>
            Profile
          </li> {/* Student info here */}
          
          <li onClick={handleLogout}>Logout</li>
        </ul>
      </aside>

      {/* Main Content */}
      <main className="content">
        <div className="content-section">
          {/* Conditional rendering for the 'main' tab */}
          {isActive === 'main' && (
            <>
              <h1>Welcome to CourseFlow's Course Registration Portal!</h1>
              <h2>My Enrollments</h2>
              <ul>
                <li>Database Systems</li>
              </ul>
            </>
          )}

          {/* Conditional rendering for the 'browse' tab */}
          {isActive === 'browse' && <Browse />}

          {/* Conditional rendering for the 'schedule' tab */}
          {isActive === 'schedule' && <Schedule />}

          {/* Conditional rendering for the 'profile' tab */}
          {isActive === 'profile' && (
            <div className="profile-section">
              <h1>My Profile</h1>
              <h2><i>Welcome to your profile, User</i></h2>  {/* fetch */}

              {/* Personal Details Dropdown */}
              {/* fetch */ }
              <h3
                onClick={() => handleDropdownToggle("personal")}
                className="personal-dropdown-toggle"
              >
                {dropdowns.personal ? "▲" : "▼"}
                Personal Details
              </h3>
              {dropdowns.personal && (
                <ul className="personal-dropdown-menu">
                  <li><b>Student ID:</b> test </li>
                  <li><b>Username:</b> test </li>
                  <li><b>Email:</b> test </li>
                </ul>
              )}

              {/* University Details Dropdown */}
              {/* fetch */ }
              <h3
                onClick={() => handleDropdownToggle("university")}
                className="university-dropdown-toggle"
              >
                {dropdowns.university ? "▲" : "▼"}
                University Details
              </h3>
              {dropdowns.university && (
                <ul className="university-dropdown-menu">
                  <li><b>University ID:</b> Delete maybe? </li>
                  <li><b>University Name:</b> The City College of New York </li>
                </ul>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Homepage;
