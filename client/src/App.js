import "bootstrap/dist/css/bootstrap.min.css"

import { BrowserRouter, Route, Routes } from "react-router-dom";
import Login from './Components/Login/Login';
import Reset from './Components/Reset/Reset';
import Homepage from './Components/Homepage/Homepage';
import Browse from './Components/Browse/Browse';
import Schedule from "./Components/Schedule/Schedule";

function App() {
  return (
    <div>
    <>
      <BrowserRouter>
        <Routes>
          <Route index element={<Login />} />
        {/* Reset Password Route */}
          <Route path="/resetpassword" element={<Reset />} />
        {/* Browse Route */}
          <Route path="/browse" element={<Browse />} />
        {/* Schedule Route */}
          <Route path="/schedule_build" element={<Schedule />} />
        {/* Homepage Route */}
          <Route path="/homepage" element={<Homepage />} />
        </Routes>
      </BrowserRouter>
    </>
    </div>
  );
}

export default App;
