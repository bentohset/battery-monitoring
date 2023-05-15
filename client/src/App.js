import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Redirect } from 'react-router-dom';
import LoginPage from './LoginPage';
import HomePage from './HomePage';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);

  const handleLogin = (userData) => {
    setIsLoggedIn(true);
    setUserData(userData);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserData(null);
  };

  return (
    <Router>
      <Routes>
        <Route path="/login">
          {isLoggedIn ? <Redirect to="/" /> : <LoginPage onLogin={handleLogin} />}
        </Route>
        <Route path="/">
          {isLoggedIn ? (
            <HomePage onLogout={handleLogout} />
          ) : (
            <Redirect to="/login" />
          )}
        </Route>
      </Routes>
    </Router>
  );
};

export default App;
