import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Browse from '../Browse/Browse';
import Schedule from "../Schedule/Schedule";
import "./Homepage.css";

const Homepage = () => {
  const [account, setAccount] = useState(null);
  const [message, setMessage] = useState('');
  const [isActive, setIsActive] = useState("main");
  const navigate = useNavigate();

  // Manages multiple dropdowns
  const [dropdowns, setDropdowns] = useState({
    personal: false,
    university: false,
  });

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

  useEffect(() => {
    const fetchHomepage = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/homepage', {
          method: 'GET',
          credentials: 'include',
        });
        if (response.ok) {
          const data = await response.json();
          setAccount(data);
        }
    	else {
          window.location.href = '/'
        }
      }
      catch (error) {
        setMessage('Homepage error');
        window.location.href = '/';
      }
    };
    fetchHomepage();
  }, []);

  const handleLogout = async (e) => {
    e.preventDefault(); 
      try {
        const response = await fetch('http://127.0.0.1:5000/api/logout', {
          method: 'POST',
          credentials: 'include',
        });
        const data = await response.json();
        if (response.ok) {
          setMessage('Logout successful');
          window.location.href = '/';
        }
        else {
          setMessage(data.error);
        }
      }
      catch (error) {
        setMessage('Logout error');
    }
  };

  return (
    <div>
      {account ? (
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
                <h2><i>Welcome to your profile, {account.firstName}</i></h2>  {/* fetch */}

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
                    <li><b>Student ID:</b> {account.id} </li>
                    <li><b>Username:</b> {account.firstName} {account.lastName} </li>
                    <li><b>Email:</b> {account.email} </li>
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
                    <li><b>University ID:</b> 1 </li>
                    <li><b>University Name:</b> The City College of New York </li>
                  </ul>
                )}
              </div>
            )}
          </div>
        </main>
      </div>
      ) : (<p>Loading...</p>)}
      {message.length > 0 && <p>{message}</p>}
    </div>
  );
};

export default Homepage;
