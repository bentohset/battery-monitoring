import React, { useState, useEffect } from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';

function Modal({id}) {
  const [data, setData] = useState([])

  const dateFormatter = (date) => {
    const dateObj = new Date(date)
    let day = dateObj.getDate().toString()
    let month = (dateObj.getMonth()+1).toString()
    let year = dateObj.getFullYear().toString()

    return day + "/" + month + "/" + year
  }
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/battery/${id}`);
        const jsonData = await response.json();
        setData(jsonData);
      } catch (error) {
        console.error(error)
      }
    }

    fetchData();
  }, [id]);

  return (
    <div className='modalcontainer' scroll="no">
    {id ? (
      <p className='modaltitle'>Battery ID: {id}</p>
    ):(
      <p className='modaltitle'>Click on details to show graphs</p>
    )}

      <p className='modalp'>Internal Impedance</p>
      <LineChart width={350} height={180} data={data} margin={{ top: 0, right: 20, bottom: 0, left: 0 }}>
        <Line type='monotone' dataKey="internal_impedance" stroke="#8884d8"/>
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis dataKey="timestamp" tickFormatter={dateFormatter}/>
        <YAxis />
        <Tooltip />
      </LineChart>

      <p className='modalp'>Temperature</p>
      <LineChart width={350} height={180} data={data} margin={{ top: 0, right: 20, bottom: 0, left: 0 }}>
        <Line type='monotone' dataKey="temperature" stroke="#8884d8"/>
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis dataKey="timestamp" tickFormatter={dateFormatter}/>
        <YAxis />
        <Tooltip viewBox={ {x: 0, y: 0, width: 100, height: 400 }}/>
      </LineChart>

      <p className='modalp'>Humidity</p>
      <LineChart width={350} height={180} data={data} margin={{ top: 0, right: 20, bottom: 0, left: 0 }}>
        <Line type='monotone' dataKey="humidity" stroke="#8884d8"/>
        <CartesianGrid stroke="#ccc" strokeDasharray="5 5" />
        <XAxis dataKey="timestamp" tickFormatter={dateFormatter}/>
        <YAxis />
        <Tooltip />
      </LineChart>
      
    </div>
  )
}

export default Modal