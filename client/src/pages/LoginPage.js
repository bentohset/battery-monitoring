import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/login.css'

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
      <div style={{ backgroundColor:'white', display: 'flex', borderRadius:'10px', width: '25%', height: '50%', padding:'20px', justifyContent:'center', alignItems:''}}>
        <form onSubmit={handleSubmit} className='form'>
          <h2 className='h2'>Login</h2>
          <div className='emaillabel' style={{marginBottom: '20px', marginTop:'40px'}}>
            <label htmlFor="email">Email:</label>
            <input
              type="text"
              id="email"
              value={email}
              onChange={handleEmailChange}
              className='input'
              autoComplete='off'
            />
          </div>
          <div className='emaillabel'>
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              className='input'
              onChange={handlePasswordChange}
              autoComplete='off'
              
            />
          </div>
          <button type="submit" className='loginbutton' style={{ fontWeight:'700'}}>Login</button>
          <div className="otherbuttons">
            <button onClick={() => navigate('register-page')} className='smallbutton'>
              Register
            </button>
            <button onClick={() => navigate('forgot-password')} className='smallbutton'>
              Forgot Password
            </button>
          </div>
          
        </form>
      </div>
      
    </div>

  );
};

export default LoginPage;
