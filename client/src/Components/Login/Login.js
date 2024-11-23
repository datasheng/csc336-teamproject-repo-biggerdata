import React, { useState } from "react";
import "./Login.css";

const Login = () => {
  const [isRightActive, setIsRightActive] = useState(false);

  const handleToggle = () => {
    setIsRightActive(!isRightActive);
  };

  return (
    <div className={`container ${isRightActive ? "right-active" : ""}`}>
      <div className="main-container">
        <div className="login">
          <form>
            <h1>Login</h1>
            <input type="email" placeholder="Email" required />
            <input type="password" placeholder="Password" required />
            <a href="/resetpassword">Forgot Password?</a>
            <button type="submit">Log in</button>
          </form>
        </div>

        <div className="register">
          <form>
            <h1>Register</h1>
            <input type="text" placeholder="First Name" required />
            <input type="text" placeholder="Last Name" required />
            <input type="email" placeholder="Email" required />
            <input type="password" placeholder="Password" required />
            <input type="password" placeholder="Confirm Password" required />
            <button type="submit">Register</button>
          </form>
        </div>

      <div className="overlay-container">
        <div className="overlay">
          <div className="left">
            <h2>Welcome to CourseFlow!</h2>
            <p>Already registered?</p>
            <button type="button" className="log-in-button" onClick={handleToggle}>Log In Here!</button>
          </div>
          <div className="right">
            <h2>Welcome Back to CourseFlow!</h2>
            <p>Not a user?</p>
            <button type="button" className="register-button" onClick={handleToggle}>Register Here!</button>
          </div>
        </div>
      </div>
      </div>
    </div>
  );
};

export default Login;
