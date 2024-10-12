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
  const selectedDate = new Date(date);
  return selectedDate < today;
};

const App = () => {
  const [date, setDate] = useState(getNextDayDate());
  const [location, setLocation] = useState('Paloheinä');
  const [graphEntries, setGraphEntries] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFormSubmit = (e) => {
    e.preventDefault();

    if (isPastDate(date)) {
      alert('Date must be today or later.');
      return;
    }

    setLoading(true);

    // Simulate data fetching
    setTimeout(() => {
      // Generate data for 24 hours
      const labels = Array.from({ length: 24 }, (_, i) => `${i}:00`);
      const usageMinutes = Array.from({ length: 24 }, () => Math.floor(Math.random() * 60));
      const rainfall = Array.from({ length: 24 }, () => Math.random() * 10);

      const newEntry = {
        data: {
          labels,
          usageMinutes,
          rainfall,
        },
        area: location,
      };

      console.log('New Entry:', newEntry); // Debugging log

      setGraphEntries([newEntry]);
      setLoading(false);
    }, 2000); // Simulate a 2-second delay for data fetching
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
          </div>
        ) : (
          graphEntries.map((entry, index) => (
            <Graph key={index} data={entry.data} legend={entry.legend} area={entry.area} style={{ width: '100%', maxWidth: '1200px' }} />
          ))
        )}
      </div>
    </div>
  );
};

export default App;