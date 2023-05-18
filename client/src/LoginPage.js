import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './login.css'

const LoginPage = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const navigate = useNavigate();

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

    fetch("http://127.0.0.1:5000/auth/login", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody)
    }).then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Login failed');
      }
    }).then(data => {
      onLogin(data.token);
    }).catch(error => {
      console.error(error);
    });

    // Redirect to the home page
    
  };

  return (
    <div className='container'>
      
      <form onSubmit={handleSubmit} className='form'>
        <h2 className='h2'>Login Page</h2>
        <div className='emaillabel'>
          <label htmlFor="email">Email:</label>
          <input
            type="text"
            id="email"
            value={email}
            onChange={handleEmailChange}
            className='input'
          />
        </div>
        <div className='emaillabel'>
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={handlePasswordChange}
          />
        </div>
        <button type="submit" className='loginbutton'>Login</button>
        <div className="otherbuttons">
          <button onClick={() => navigate('register-page')}>
            RegisterPage
          </button>
          <button onClick={() => navigate('forgot-password')}>
            Forgot Password
          </button>
        </div>
        
      </form>
      
    </div>
  );
};

export default LoginPage;
