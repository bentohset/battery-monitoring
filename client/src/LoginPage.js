import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

const LoginPage = ({ onLogin }) => {
  const history = useHistory();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // Perform authentication logic
    // Here, you can make an API request to your backend for authentication

    // Simulating successful authentication
    const userData = {
      email: email,
      // Include other user data if needed
    };

    // Call the onLogin function to update the login status and store user data
    onLogin(userData);

    // Redirect to the home page
    history.push('/');
  };

  return (
    <div>
      <h2>Login Page</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="text"
            id="email"
            value={email}
            onChange={handleEmailChange}
          />
        </div>
        <div>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={handlePasswordChange}
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;
