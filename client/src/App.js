import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
    const [data, setData] = useState({
        name: "",
        date: ""
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://127.0.0.1:5000/");
                const jsonData = await response.json();
                setData({
                    name: jsonData.Name,
                    date: jsonData.Date
                });
            } catch (error) {
                console.log(error);
            }
        }

        fetchData();

    }, []);

    console.log(data);

  return (
    <div className="App">
        <header className="App-header">
            <h1>Test</h1>
            <p>{data.name}</p>
            <p>{data.date}</p>
        </header>
    </div>
  );
}

export default App;
