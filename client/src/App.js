import "bootstrap/dist/css/bootstrap.min.css"
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./Components/Login/Login";
import Reset from "./Components/Reset/Reset";
import Homepage from "./Components/Homepage/Homepage";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(true); {/* User starts logged in for testing */}

  return (
    <Router>
      <Routes>
        {/* Login Route */}
        <Route
          path="/"
          element={
            isLoggedIn ? (
              <Navigate to="/homepage" replace />
            ) : (
              <Login setIsLoggedIn={setIsLoggedIn} />
            )
          }
        />
        {/* Homepage Route */}
        <Route
          path="/homepage"
          element={
            isLoggedIn ? (
              <Homepage setIsLoggedIn={setIsLoggedIn} />
            ) : (
              <Navigate to="/" replace />
            )
          }
        />
        {/* Reset Password Route */}
        <Route path="/resetpassword" element={<Reset />} />
      </Routes>
    </Router>
  );
}

export default App;
