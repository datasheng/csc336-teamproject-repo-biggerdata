import "bootstrap/dist/css/bootstrap.min.css"

import { BrowserRouter, Route, Routes } from "react-router-dom";
import Login from './Components/Login/Login';
import Reset from './Components/Reset/Reset';
import Homepage from './Components/Homepage/Homepage';
import Browse from './Components/Browse/Browse';
import Schedule from "./Components/Schedule/Schedule";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(true); // User starts logged in for testing

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
        <Route 
          path="/resetpassword"
          element={<Reset />} 
        />

        {/* Browse Route */}
        <Route
          path="/browse"
          element={<Browse />}
        />

        {/* Schedule Route */}
        <Route
          path="/schedule_build"
          element={<Schedule />}
        />
      </Routes>
    </Router>
  );
}

export default App;