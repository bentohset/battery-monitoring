import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/login.css'
import { useAuth } from '../hooks/auth';

function RegisterPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { register } = useAuth()
  
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
  
      const res = await register({email, password})
      if (res === "Success") {
        navigate('/')
      }
  
    };
  
    return (
      <div className='container'>
        <div 
          style={{ 
            width:'25%', 
            height:'45%', 
            backgroundColor:'white', 
            flexDirection:'column', 
            display: 'flex', 
            borderRadius:'10px', 
            paddingTop:'20px', 
            justifyContent:'center', 
            alignItems:'center'
          }}
        >
          <form onSubmit={handleSubmit} className='form'>
            <h2 className='h2'>Register Page</h2>

            <div className='emaillabel' style={{marginBottom: '20px', marginTop:'40px'}}>
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

            <button type="submit" className='loginbutton' style={{ fontWeight:'700', cursor:'pointer'}}>Register</button>

            <div style={{ display:'flex', alignItems:'center', justifyContent:'center'}}>
              <p style={{fontSize:15, textAlign:'center'}}>Alread have an account? <span onClick={() => navigate('/')} style={{fontWeight:700, cursor:'pointer'}}>Sign in here</span></p>
            </div>
            
          </form>
        </div>
      </div>
    );
  };

export default RegisterPage