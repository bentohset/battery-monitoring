import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Redirect } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import RegisterPage from './pages/RegisterPage';
import ForgotPassword from './pages/ForgotPassword';
import ChangePassword from './pages/ChangePassword';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [token, setToken] = useState(null);

  const handleLogin = (userData) => {
    setIsLoggedIn(true);
    setToken(token);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setToken(null);
  };

  return (
    <>
    <Routes>
      {isLoggedIn ? (
        <>
          <Route path="/" element={<HomePage onLogout={handleLogout}/>} />
        </>
      ) : (
        <>
          <Route path="/" element={<LoginPage onLogin={handleLogin}/>} />
          <Route path="/register-page" element={<RegisterPage onLogin={handleLogin}/>} />
          <Route path="/forgot-password" element={<ForgotPassword/>}/>
          <Route path="/auth/reset/:token" element={<ChangePassword/>}/>
        </>
      )}
    </Routes>
 </>
  );
};

export default App;
