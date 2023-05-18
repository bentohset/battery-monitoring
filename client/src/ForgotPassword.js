import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function ForgotPassword() {
    const [email, setEmail] = useState('');
    const [emailSent, setEmailSent] = useState(false)

    const navigate = useNavigate();

    const handleEmailChange = (e) => {
        setEmail(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
    
        // Perform authentication logic
        // Here, you can make an API request to your backend for authentication
        const requestBody = {
          email: email,
        };
    
        fetch("http://127.0.0.1:5000/auth/forgot", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestBody)
        }).then(response => {
          if (response.ok) {
            setEmailSent(true)
            return response.json();
          } else {
            throw new Error('Verify failed');
          }
        }).catch(error => {
          console.error(error);
        });
    
        // Redirect to the home page
        
      };

  return (
    <div className='container'>
        <form onSubmit={handleSubmit} className='form'>
            <div className='emaillabel'>
              <label htmlFor="email">Verify Email:</label>
              <input
                  type="text"
                  id="email"
                  value={email}
                  onChange={handleEmailChange}
                  className='input'
              />
            </div>
            <button type="submit" className='loginbutton'>Verify</button>
            <button className="backbtn" onClick={() => navigate('/')}>
              Back
            </button>
            {emailSent ? (
                <p className='h2'>Email sent</p>
            ): (<></>)}
            
      </form>
    </div>
  )
}

export default ForgotPassword