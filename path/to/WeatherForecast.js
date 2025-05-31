import React, { useState, useEffect } from 'react';
import axios from 'axios';

const WeatherForecast = () => {
    const [forecastData, setForecastData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const result = await axios(
                'http://api.openweathermap.org/data/2.5/forecast?appid=<Your_API_Key>&units=metric&q=<Your_City_Name>',
            );
            setForecastData(result.data.list);
        };
        fetchData();
    }, []);

    return (
        <div>
            <h1>5-Day Weather Forecast</h1>
            {forecastData.map((item, index) => (
                <div key={index}>
                    <h2>{item.dt_txt}</h2>
                    <p>Temperature: {item.main.temp} °C</p>
                    <p>Precipitation: {item.rain ? item.rain['3h'] : 0} mm</p>
                </div>
            ))}
        </div>
    );
};

export default WeatherForecast;