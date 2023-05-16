import React, { useState, useEffect } from 'react';

const HomePage = ({ onLogout }) => {
  const [data, setData] = useState([])

  const handleLogout = () => {
    // Perform logout logic
    // Here, you can clear any authentication tokens or user data

    // Call the onLogout function to update the login status
    onLogout();

    // Redirect to the login page
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/data");
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error(error)
      }
    }

    fetchData();
  }, []);

  return (
    <div>
      <h2>Welcome to the Home Page!</h2>
      <p>You are now logged in.</p>
      
      <button onClick={handleLogout}>Logout</button>
      <div>
        <table>
          <thead>
            <tr>
              <th>Battery_id</th>
              <th>Shelf_id</th>
              <th>Container_id</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.shelf}</td>
                <td>{item.container}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HomePage;
