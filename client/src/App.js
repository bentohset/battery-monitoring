import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Redirect } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import HomePage from './pages/HomePage';
import RegisterPage from './pages/RegisterPage';
import ForgotPassword from './pages/ForgotPassword';
import ChangePassword from './pages/ChangePassword';
import { useAuth } from './hooks/auth';

const App = () => {
  const { cookies } = useAuth()


  return (
    <>
    <Routes>
      {cookies.token ? (
        <>
          <Route path="/" element={<HomePage/>} />
        </>
      ) : (
        <>
          <Route path="/" element={<LoginPage/>} />
          <Route path="/register-page" element={<RegisterPage/>} />
          <Route path="/forgot-password" element={<ForgotPassword/>}/>
          <Route path="/auth/reset/:token" element={<ChangePassword/>}/>
        </>
      )}
    </Routes>
 </>
  );
};

export default App;
