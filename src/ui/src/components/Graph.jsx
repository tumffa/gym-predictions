import React from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

const Graph = ({ data, area, style }) => {
  // Find the index of the first NaN value in the rainfall data
  const firstNaNIndex = data.rainfall.findIndex(value => isNaN(value));

  // If there are no NaN values, set firstNaNIndex to the length of the data
  const validEndIndex = firstNaNIndex === -1 ? data.rainfall.length : firstNaNIndex;

  // Filter the data up to the first NaN index
  const filteredLabels = data.labels.slice(0, validEndIndex);
  const filteredUsageMinutes = data.usageMinutes.slice(0, validEndIndex);
  const filteredRainfall = data.rainfall.slice(0, validEndIndex);

  // Create missing forecast data starting from the first NaN index
  const missingForecastLabels = data.labels.slice(validEndIndex);
  const missingForecastData = data.rainfall.slice(validEndIndex).map(() => 0);

  const datasets = [
    {
      label: `Usage Minutes`,
      data: data.usageMinutes,
      fill: false,
      backgroundColor: 'rgba(75,192,192,0.4)',
      borderColor: 'rgba(75,192,192,1)',
    },
    {
      label: `Rainfall`,
      data: filteredRainfall,
      fill: false,
      backgroundColor: 'rgba(153,102,255,0.4)',
      borderColor: 'rgba(153,102,255,1)',
    },
  ];

  // Conditionally add the "Missing Forecast" dataset if there are missing forecasts
  if (missingForecastData.length > 0) {
    datasets.push({
      label: `Missing Forecast`,
      data: Array(validEndIndex).fill(null).concat(missingForecastData),
      fill: false,
      backgroundColor: 'rgba(255,0,0,0.4)',
      borderColor: 'rgba(255,0,0,1)',
      pointBackgroundColor: 'rgba(255,0,0,1)',
      pointBorderColor: 'rgba(255,0,0,1)',
      pointRadius: 5,
      showLine: false,
    });
  }

  const chartData = {
    labels: data.labels,
    datasets: datasets,
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: `Predicted usage and rainfall in ${area}`,
        font: {
          size: 48,
        },
      },
    },
  };

  console.log('Chart Data:', chartData); // Debugging log

  return (
    <div style={{ ...style, position: 'relative', height: '800px', width: '1200px' }}>
      <Line data={chartData} options={options} />
    </div>
  );
};

export default Graph;