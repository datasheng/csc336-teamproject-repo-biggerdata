import "bootstrap/dist/css/bootstrap.min.css"

import { BrowserRouter, Route, Routes } from "react-router-dom";
import Login from './Components/Login/Login';
import Reset from './Components/Reset/Reset';
import Dashboard from './Components/Homepage/Homepage';

function App() {
  return (
    <div>
    <>
      <BrowserRouter>
        <Routes>
          <Route index element={<Login />} />
          <Route path = "/resetpassword" element={<Reset />} />
          <Route path="/homepage" element={<Homepage />} />
        </Routes>
      </BrowserRouter>
    </>
    </div>
  );
}

export default App;
