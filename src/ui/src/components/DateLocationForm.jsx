import React from 'react';

const DateLocationForm = ({ date, setDate, location, setLocation, onSubmit, style }) => {
  return (
    <form onSubmit={onSubmit} style={{ ...style, fontSize: '1.5em' }}>
      <div style={{ marginBottom: '1em' }}>
        <label style={{ marginRight: '1em' }}>Date:</label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          required
          style={{ padding: '0.5em', fontSize: '1em' }}
        />
      </div>
      <div style={{ marginBottom: '1em' }}>
        <label style={{ marginRight: '1em' }}>Location:</label>
        <select
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          required
          style={{ padding: '0.5em', fontSize: '1em' }}
        >
          <option value="Paloheinä">Paloheinä</option>
          <option value="Pirkkola">Pirkkola</option>
          <option value="Hietaniemi">Hietaniemi</option>
        </select>
      </div>
      <button type="submit" style={{ padding: '0.5em 1em', fontSize: '1em' }}>Submit</button>
    </form>
  );
};

export default DateLocationForm;