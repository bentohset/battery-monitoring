import React, { useState, useEffect } from 'react';

function Modal({id}) {
  const [data, setData] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/data/${id}`);
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error(error)
      }
    }

    fetchData();
  }, [id]);

  return (
    <div className='modalcontainer'>
      <p className='modalp'>Modal</p>
      {data.map((item) => (
        <div>
          <p>Timestamp: {item.timestamp}</p>
          <li>BLE UUID: {item.ble_uuid}</li>
          <li>Humidity: {item.humidity}</li>
          <li>Temperature: {item.temperature}</li>
          <li>ISR: {item.internal_series_resistance}</li>
          <li>Impedance: {item.internal_impedance}</li>
        </div>
      ))}
    </div>
  )
}

export default Modal