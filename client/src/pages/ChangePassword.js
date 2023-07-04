import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

function ChangePassword() {
    const [password, setPassword] = useState('');
    const [passwordChanged, setPasswordChanged] = useState(false);
    const token = useParams().token;

    const navigate = useNavigate();

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        // Perform authentication logic
        // Here, you can make an API request to your backend for authentication
        const requestBody = {
            new_password: password
        };

        fetch(`http://127.0.0.1:5000/auth/reset/${token}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        }).then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Change failed');
            }
        }).then(data => {
            setPasswordChanged(true)
        }).catch(error => {
            console.error(error);
        });
    
    };
  return (
    <div>
        <h2>Change Password</h2>
        <form onSubmit={handleSubmit}>
            <div>
            <label htmlFor="password">Password:</label>
            <input
                type="text"
                id="password"
                value={password}
                onChange={handlePasswordChange}
            />
            </div>
        <button type="submit">Change</button>
        </form>
        <button className='btn' onClick={() => navigate('/')}>
            Back to Login
        </button>
        {passwordChanged ? (
            <p>Password changed</p>
        ): (<></>)}
    </div>
  )
}

export default ChangePassword