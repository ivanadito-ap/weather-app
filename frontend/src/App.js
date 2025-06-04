import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState(null);
  const [forecast, setForecast] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchWeather = async () => {
    if (!city) return;
    
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:8000/api/weather?city=${city}`);
      if (!response.ok) {
        throw new Error('Failed to fetch weather data');
      }
      const data = await response.json();
      setWeather(data.current);
      setForecast(data.forecast);
      fetchHistory();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/history');
      if (!response.ok) {
        throw new Error('Failed to fetch history');
      }
      const data = await response.json();
      setHistory(data);
    } catch (err) {
      console.error('Error fetching history:', err);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  return (
    <div className="App">
      <h1>Weather Dashboard</h1>
      <div className="search-container">
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter city name"
          onKeyPress={(e) => e.key === 'Enter' && fetchWeather()}
        />
        <button onClick={fetchWeather} disabled={loading || !city}>
          {loading ? 'Loading...' : 'Get Weather'}
        </button>
      </div>

      {loading && <p className="loading">Loading weather data...</p>}
      {error && <p className="error">Error: {error}</p>}

      {weather && (
        <div className="weather-container">
          <h2>Current Weather in {weather.city}</h2>
          <div className="weather-details">
            <p>Temperature: {weather.temp}°C</p>
            <p>Humidity: {weather.humidity}%</p>
            <p>Conditions: {weather.conditions}</p>
          </div>
        </div>
      )}

      {forecast.length > 0 && (
        <div className="forecast-container">
          <h3>5-Day Forecast</h3>
          <div className="forecast-items">
            {forecast.map((day, index) => (
              <div key={index} className="forecast-item">
                <p><strong>{day.date}</strong></p>
                <p>{day.temp}°C</p>
                <p>{day.conditions}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {history.length > 0 && (
        <div className="history-container">
          <h3>Search History</h3>
          <ul>
            {history.map((item, index) => (
              <li key={index}>
                {item.city} - {new Date(item.timestamp).toLocaleString()}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
