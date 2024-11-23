import React from "react";

function Reset() {
  return (
    <div className="reset-container">
        <div className="reset-box">
            <h1>Reset Your Password</h1>
            <form>
              <input type="email" placeholder="Enter your email" required />
              <button type="submit">Send Reset Link</button>
            </form>
        </div>
    </div>
  );
}

export default Reset;
