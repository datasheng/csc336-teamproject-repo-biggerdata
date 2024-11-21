import "bootstrap/dist/css/bootstrap.min.css"
import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Login from './Components/Login/Login';
import Register from './Components/Register/Register';

function App() {
  return (
    <div>
    <>
      <BrowserRouter>
        <Routes>
          <Route index element={<Login />} />
          <Route path = "/register" element={<Register />} />
          <Route path = "/login" element={<Login />} />
        </Routes>
      </BrowserRouter>
      </>

    </div>
  );

}

export default App;
