import React, { useState } from "react";
import { TbEyeClosed, TbEye } from "react-icons/tb";
import { FaRegUser } from "react-icons/fa";
import "./Login.css";

const Login = () => {
  const [isRightActive, setIsRightActive] = useState(false);
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');

  const [showPassword, setShowPassword] = useState(false);
  
  const pwdToggle = () => {
    setShowPassword(!showPassword);
  }
	
  const handleToggle = () => {
    setIsRightActive(!isRightActive);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setMessage('Passwords do not match');
      return;
    }
    try {
      const response = await fetch('http://127.0.0.1:5000/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          firstName,
          lastName,
          email,
          password,
        }),
        credentials: 'include',
      });
      const data = await response.json();
        if (response.ok) {
          setMessage('User registered');
        }
        else {
          setMessage(data.error);
        }
      }
      catch (error) {
        setMessage('Register error');
      }
  };

  const handleLogin = async (e) => {
    e.preventDefault(); 
    try {
      const response = await fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          password,
        }),
        credentials: 'include',
      });
      const data = await response.json();
        if (response.ok) {
          setMessage('Login successful');
          window.location.href = '/homepage';
        }
	else {
          setMessage(data.error);
        }
      }
    catch (error) {
      setMessage('Login error');
    }
  };

  return (
    <div className={`container ${isRightActive ? "right-active" : ""}`}>
      <div className="main-container">
        <div className="login">
          <form onSubmit={handleLogin}>
            <h1>Login</h1>
            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
	    <FaRegUser className="user-icon"/>
	
            <input type={showPassword ? "text" : "password"} placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            <div className="pwd-icon" onClick={pwdToggle}>
              {showPassword ? <TbEye /> : <TbEyeClosed />}
            </div>
	
	    <a href="/resetpassword">Forgot Password?</a>
            <button type="submit" className="submit">Log in</button>
          </form>
        </div>

        <div className="register">
          <form onSubmit={handleRegister}>
            <h1>Register</h1>
            <input type="text" placeholder="First Name" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
            <input type="text" placeholder="Last Name" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
            <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            <input type="password" placeholder="Confirm Password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
            <button type="submit" className="submit">Register</button>
          </form>
        </div>

      <div className="overlay-container">
        <div className="overlay">
          <div className="left">
            <h2>Welcome to CourseFlow!</h2>
            <p>Already registered?</p>
            <button type="button" className="log-in-button" onClick={handleToggle}>Log In Here!</button>
            {message.length > 0 && <p>{message}</p>}
          </div>
          <div className="right">
            <h2>Welcome Back to CourseFlow!</h2>
            <p>Not a user?</p>
            <button type="button" className="register-button" onClick={handleToggle}>Register Here!</button>
            {message.length > 0 && <p>{message}</p>}
          </div>
        </div>
      </div>
      </div>
    </div>
  );
};

export default Login;
