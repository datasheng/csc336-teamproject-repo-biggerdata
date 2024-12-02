import React from "react";
import { Link } from "react-router-dom";
import "./Homepage.css";

const Homepage = ({ setIsLoggedIn }) => {

  const handleLogout = () => {
    if (window.confirm("Are you sure you want to log out?")) {
      setIsLoggedIn(false);
    }
  };

  return (
    <div className="course-registration-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <h2>Navigation</h2>
        <ul>
          <li>Browse Courses</li> {/* Can view courses here */}
          <li>Schedule Builder</li> {/* Schedule view + cart here */}
          <li>Profile</li> {/* Student info here */}
          <li onClick={handleLogout}>Logout</li>
        </ul>
      </aside>

      {/* Main Content */}
      <main className="content">
        <h1>Welcome to CourseFlow's Course Registration Portal!</h1>
        <div className="content-section">
          <h2>My Enrollments</h2>
          <ul>
            <li>Database Systems</li>
          </ul>
        </div>
      </main>
    </div>
  );
};

export default Homepage;
