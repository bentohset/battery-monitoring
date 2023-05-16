import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function RegisterPage({ onLogin }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
  
    const navigate = useNavigate();
    const token = "secret_key"
  
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
      const requestBody = {
        email: email,
        password: password
      };
  
      fetch("http://127.0.0.1:5000/auth/register", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestBody)
      }).then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Registration failed');
        }
      }).then(data => {
        onLogin(token);
        navigate('/')
      }).catch(error => {
        console.error(error);
      });
  
      // Call the onLogin function to update the login status and store user data
  
      // Redirect to the home page
    };
  
    return (
      <div>
        <h2>Register Page</h2>
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
          <button type="submit">register</button>
        </form>
        <button className="btn" onClick={() => navigate('/')}>
            Back
        </button>
      </div>
    );
  };

export default RegisterPage