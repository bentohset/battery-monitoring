import React, { useState, useEffect } from 'react';
import { ArrowLeftOnRectangleIcon, Bars3Icon } from '@heroicons/react/24/solid'
import '../styles/home.css'
import Modal from '../components/Modal';
import { useAuth } from '../hooks/auth';

const HomePage = () => {
  const [data, setData] = useState([])
  const [id, setId] = useState("");
  const { logout } = useAuth()

  const handleLogout = () => {
    // Perform logout logic
    // Here, you can clear any authentication tokens or user data

    // Call the onLogout function to update the login status
    logout()
    // Redirect to the login page
  };

  const showModal = (id) => {
    setId(id)
    console.log(id)
  }


  const convertDate = (time) => {
    const dateObj = new Date(time)
    const date = dateObj.getDate().toString()
    const month = (dateObj.getMonth()+1).toString()
    const year = dateObj.getFullYear().toString()
    const hour = dateObj.getHours().toString()
    let timehour = hour
    if (hour < 10) {
      timehour = "0" + hour
    }
    const minute = dateObj.getMinutes().toString()

    return date + '/' + month + '/' + year + " " + timehour + ":" + minute
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/battery/table");
        const jsonData = await response.json();
        console.log(jsonData)
        setData(jsonData);
      } catch (error) {
        console.error(error)
      }
    }

    fetchData();
  }, []);

  return (
    <div className='main'>
      <nav className='navbar'>
        <div className='titleleft'>
          <h2>Battery Monitor</h2>
        </div>
        
        <button onClick={handleLogout} className='logoutbutton'>
          Logout
        </button>
      </nav>

      <div className='tcontainer'>
        <Modal id={id}/>
        <div className='tablecontainer'> 
          <table >
            <thead className='header'>
              <tr>
                <th>Battery ID</th>
                <th>Shelf</th>
                <th>Container</th>
                <th>Last Measured</th>
                <th>Humidity</th>
                <th>Temperature</th>
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
                  <td>{convertDate(item.timestamp)}</td>
                  <td>{item.humidity.toFixed(4)}</td>
                  <td>{item.temperature.toFixed(4)}</td>
                  <td>{item.internal_impedance.toFixed(4)}</td>
                  <td><button onClick={() => showModal(item.battery_id)}>Click</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
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