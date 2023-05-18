import React, { useState, useEffect } from 'react';
import Popup from 'reactjs-popup';
import './home.css'
import Modal from './Modal';

const HomePage = ({ onLogout }) => {
  const [data, setData] = useState([])
  const [modal, setModal] = useState(false)

  const handleLogout = () => {
    // Perform logout logic
    // Here, you can clear any authentication tokens or user data

    // Call the onLogout function to update the login status
    onLogout();

    // Redirect to the login page
  };

  const showModal = () => {
    setModal(true);
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/data/table");
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error(error)
      }
    }

    fetchData();
  }, []);

  return (
    <div className='tcontainer'>
      <Modal show={modal}></Modal>
      <div className='titles'>
        <h2>Battery Monitor</h2>
        <button onClick={handleLogout} className='logoutbutton'>Logout</button>
      </div>
      
      <div className='tablecontainer'> 
        <table >
          <thead className='header'>
            <tr>
              <th>Battery ID</th>
              <th>Shelf</th>
              <th>Container</th>
              <th>Timestamp</th>
              <th>Humidity</th>
              <th>Temperature</th>
              <th>Voltage Open Circuit</th>
              <th>Internal Series Resistance</th>
              <th>Internal Impedance</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item) => (
              <tr key={item.battery_id} className='bodyrow'>
                <td>{item.battery_id}</td>
                <td>SHELF {item.shelf}</td>
                <td>CONTAINER {item.container}</td>
                <td>{item.timestamp}</td>
                <td>{item.humidity}</td>
                <td>{item.temperature}</td>
                <td>{item.voltage_open_circuit}</td>
                <td>{item.internal_series_resistance}</td>
                <td>{item.internal_impedance}</td>
                <td><button onClick={showModal}>Click</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HomePage;



//   tablerow: {
//     borderBottom: "1px solid #ddd"

//   },
//   tablerow:hover
// }