import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/login.css'

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
      <div className='container'>
        <form onSubmit={handleSubmit} className='form'>
          <h2 className='h2'>Register Page</h2>
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
              className='input'
            />
          </div>
          <button type="submit" className='loginbutton'>Register</button>
          <div className="otherbuttons">
            <button className="btn" onClick={() => navigate('/')}>
              Back
            </button>
          </div>
          
        </form>
        
      </div>
    );
  };

export default RegisterPage