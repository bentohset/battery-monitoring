import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/login.css'
import { useAuth } from '../hooks/auth';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useAuth()

  const navigate = useNavigate();

  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !password) {
      return 
    }
    const res = await login({email, password})

    if (res === "Success") {
      navigate('/')
    } 

  }

  return (
    <div className='container'>
      <div style={{ backgroundColor:'white', flexDirection:'column', display: 'flex', borderRadius:'10px', padding:'0px', justifyContent:'center', alignItems:'center'}}>
        <form onSubmit={handleSubmit} className='form'>
          <h2 className='h2'>Battery Monitoring Dashboard</h2>
          <h2 className='h2' style={{fontSize:20}}>Login</h2>
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
          <button type="submit" className='loginbutton' style={{ fontWeight:'700', cursor:'pointer'}}>Login</button>
          <div style={{ display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center'}}>
            <p style={{fontSize:15, textAlign:'center'}}>Don't have an account? <span onClick={() => navigate('register-page')} style={{fontWeight:700, cursor:'pointer'}}>Register here</span></p>
            <p onClick={() => navigate('forgot-password')} style={{marginTop:'0px', cursor:'pointer'}}>Forgot password</p>
          </div>
          
        </form>
      </div>
      
    </div>

  );
};

export default LoginPage;
