import { Link } from "react-router-dom";
import './Register.css';

const Register = () => {
  return (
      <section className='background'>
          <div className='wrapper'>
              <form action=''>
                  <h1>Register</h1>
                  <div className='input-box'>
                    <input type='text' placeholder='Username' required/>
                  </div>

                  <div className='input-box'>
                    <input type='text' placeholder='Password' required/>
                  </div>

                  <div className="input-box">
                    <input type='text' placeholder='Confirm Password' required/>
                  </div>

                  <button type='submit'>Register</button>

                  <div className='register-user'>
                    <p>Already Registered? <Link to="/login">Log In!</Link></p>
                  </div>
              </form>   
          </div>
      </section>
  );
};

export default Register;