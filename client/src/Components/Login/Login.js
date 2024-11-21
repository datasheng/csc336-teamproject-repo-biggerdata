import React from 'react';
import './Login.css';
import { Link } from "react-router-dom";
import { FaUser, FaLock } from "react-icons/fa";

const Login = () => {
    return (
        <section className='background'>
            <div className='wrapper'>
                <form action=''>
                    <h1>Login</h1>
                    <div className='input-box'>
                        <input type='text' placeholder='Username' required/>
                        <FaUser className='icon'/>
                    </div>

                    <div className='input-box'>
                        <input type='text' placeholder='Password' required/>
                        <FaLock className='icon'/>
                    </div>

                    <div className='forgot-pw'>
                        <a href='/resetpassword'>Forgot Password?</a>
                    </div>

                    <button type='submit'>Login</button>

                    <div className='register-user'>
                        <p>New? <Link to="/register">Register Here!</Link></p>
                    </div>
                </form>   
            </div>
        </section>
    );
};

export default Login; 