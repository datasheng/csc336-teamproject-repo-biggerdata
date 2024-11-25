import "bootstrap/dist/css/bootstrap.min.css"

import { BrowserRouter, Route, Routes } from "react-router-dom";
import Login from './Components/Login/Login';
import Reset from './Components/Reset/Reset';


function App() {
  return (
    <div>
    <>
      <BrowserRouter>
        <Routes>
          <Route index element={<Login />} />
          <Route path = "/resetpassword" element={<Reset />} />
        </Routes>
      </BrowserRouter>
      </>

    </div>
  );

}

export default App;