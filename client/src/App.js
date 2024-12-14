import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./Components/Login/Login";
import Reset from "./Components/Reset/Reset";
import Homepage from "./Components/Homepage/Homepage";
import FacultyHome from "./Components/FacultyHome/FacultyHome";
import Browse from './Components/Browse/Browse';
import Schedule from "./Components/Schedule/Schedule";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(true); {/* User starts logged in for testing */}
  const [userRole, setUserRole] = useState(""); {/* Tracks role: 'user' or 'faculty' */}

  return (
    <Router>
      <Routes>
        {/* Login Route */}
        <Route
          path="/"
          element={
            isLoggedIn ? (
              userRole === "user" ? (
                <Navigate to="/user-homepage" replace />
              ) : (
                <Navigate to="/faculty-homepage" replace />
              )
            ) : (
              <Login setIsLoggedIn={setIsLoggedIn} setUserRole={setUserRole} />
            )
          }
        />

        {/* User Homepage Route */}
        <Route
          path="/user-homepage"
          element={
            isLoggedIn && userRole === "user" ? (
              <Homepage setIsLoggedIn={setIsLoggedIn} />
            ) : (
              <Navigate to="/" replace />
            )
          }
        />

        {/* Faculty Homepage Route */}
        <Route
          path="/faculty-homepage"
          element={
            isLoggedIn && userRole === "faculty" ? (
              <FacultyHome setIsLoggedIn={setIsLoggedIn} />
            ) : (
              <Navigate to="/" replace />
            )
          }
        />

        {/* Reset Password Route */}
        <Route path="/resetpassword" element={<Reset />} />

        {/* Browse Route */}
        <Route path="/browse" element={<Browse />} />

        {/* Schedule Route */}
        <Route path="/schedule_build" element={<Schedule />} />
      </Routes>
    </Router>
  );
}

export default App;
