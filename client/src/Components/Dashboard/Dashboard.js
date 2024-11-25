import React, { useEffect, useState } from 'react';

const Dashboard = () => {
  const [account, setAccount] = useState(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/dashboard', {
          method: 'GET',
          credentials: 'include',
        });
        if (response.ok) {
          const data = await response.json();
          setAccount(data);
        }
    	else {
          window.location.href = '/'
        }
      }
      catch (error) {
        setMessage('Dashboard error');
        window.location.href = '/';
      }
    };
    fetchDashboard();
  }, []);

  const handleLogout = async (e) => {
    e.preventDefault(); 
      try {
        const response = await fetch('http://127.0.0.1:5000/api/logout', {
          method: 'POST',
          credentials: 'include',
        });
        const data = await response.json();
        if (response.ok) {
          setMessage('Logout successful');
          window.location.href = '/';
        }
        else {
          setMessage(data.error);
        }
      }
      catch (error) {
        setMessage('Logout error');
    }
  };

  return (
    <div>
      {account ? (
        <div>
          <h1>Hi, {account.firstName}</h1>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <p>Loading...</p>
      )}
	  {message.length > 0 && <p>{message}</p>}
    </div>
  );
};

export default Dashboard;
