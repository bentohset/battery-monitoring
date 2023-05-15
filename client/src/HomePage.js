import React from 'react';
import { useHistory } from 'react-router-dom';

const HomePage = ({ onLogout }) => {
  const history = useHistory();

  const handleLogout = () => {
    // Perform logout logic
    // Here, you can clear any authentication tokens or user data

    // Call the onLogout function to update the login status
    onLogout();

    // Redirect to the login page
    history.push('/login');
  };

  return (
    <div>
      <h2>Welcome to the Home Page!</h2>
      <p>You are now logged in.</p>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default HomePage;
