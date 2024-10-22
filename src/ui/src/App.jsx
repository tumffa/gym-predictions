import React, { useState } from 'react';
import DateLocationForm from './components/DateLocationForm';
import Graph from './components/Graph';
import './App.css';

// Function to get the next day's date in YYYY-MM-DD format
const getNextDayDate = () => {
  const today = new Date();
  const nextDay = new Date(today);
  nextDay.setDate(today.getDate() + 1);
  return nextDay.toISOString().split('T')[0];
};

// Function to check if a date is in the past
const isPastDate = (date) => {
  const today = new Date();
  today.setHours(0, 0, 0, 0); // Reset today's time to midnight
  const selectedDate = new Date(date);
  selectedDate.setHours(0, 0, 0, 0); // Reset selected date's time to midnight
  return selectedDate < today;
};

const App = () => {
  const [date, setDate] = useState(getNextDayDate());
  const [location, setLocation] = useState('Paloheinä');
  const [graphEntries, setGraphEntries] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFormSubmit = async (e) => {
    e.preventDefault();
  
    // if (isPastDate(date)) {
    //   alert('Date must be today or later.');
    //   return;
    // }
  
    setLoading(true);
  
    try {
      const response = await fetch('/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ date, area: location }),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Unknown error');
      }
  
      const responseText = await response.text();
      if (!responseText) {
        throw new Error('Empty response from server');
      }
  
      const data = JSON.parse(responseText);
  
      const labels = Array.from({ length: 24 }, (_, i) => `${i}:00`);
      const usageMinutes = data.usage_minutes;
      const rainfall = data.precipitation;
      const forecast_hours = Array.from({ length: 24 }, (_, i) => i); // Assuming all hours are forecasted
  
      const newEntry = {
        data: {
          labels,
          usageMinutes,
          rainfall,
        },
        area: location,
        forecast_hours,
      };
  
      console.log('New Entry:', newEntry); // Debugging log
  
      setGraphEntries([newEntry]);
    } catch (error) {
      console.error('Error fetching data:', error);
      alert(`Failed to fetch data: ${error.message}`);
      setGraphEntries([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
        <DateLocationForm
          date={date}
          setDate={setDate}
          location={location}
          setLocation={setLocation}
          onSubmit={handleFormSubmit}
          style={{ width: '80%', maxWidth: '400px', fontSize: '1.5em' }}
        />
      </div>
      <div style={{ flex: 1, display: 'flex', justifyContent: 'flex-start', paddingLeft: '5%', marginRight: '10%' }}>
        {loading ? (
          <div className="spinner-container">
            <div className="spinner"></div>
            <div className="spinner-text">Downloading forecast...</div>
          </div>
        ) : (
          graphEntries.map((entry, index) => (
            <Graph key={index} data={entry.data} area={entry.area} style={{ width: '100%', maxWidth: '1200px' }} />
          ))
        )}
      </div>
    </div>
  );
};

export default App;