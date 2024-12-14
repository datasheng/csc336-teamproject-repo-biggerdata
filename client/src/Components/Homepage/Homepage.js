import React, { useEffect, useState } from "react";
import "./Homepage.css";

const Homepage = () => {
  const [account, setAccount] = useState(null);
  const [message, setMessage] = useState('');

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
          <li>Browse Courses</li> {/* Can view courses here */}
          <li>Schedule Builder</li> {/* Schedule view + cart here */}
          <li>Profile</li> {/* Student info here */}
          <li onClick={handleLogout}>Logout</li>
        </ul>
      </aside>

      {/* Main Content */}
      <main className="content">
        <h1>Welcome to CourseFlow's Course Registration Portal, {account.firstName}!</h1>
        <div className="content-section">
          <h2>My Enrollments</h2>
          <ul>
            <li>Database Systems</li>
          </ul>
        </div>
      </main>
    </div>
	): (<p>Loading...</p>)}
    {message.length > 0 && <p>{message}</p>}
	</div>
  );
};

export default Homepage;
