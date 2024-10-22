import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register the necessary components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Graph = ({ data, area, validEndIndex, style }) => {
  // Multiply rainfall data by 10
  const multipliedRainfall = data.rainfall.map(value => value * 10);

  // Identify the indices of NaN values in the rainfall data
  const missingForecastData = data.rainfall.map((value, index) => isNaN(value) ? index : null).filter(index => index !== null);

  const datasets = [
    {
      label: `Usage Minutes`,
      data: data.usageMinutes,
      fill: false,
      backgroundColor: 'rgba(75,192,192,0.4)',
      borderColor: 'rgba(75,192,192,1)',
    },
    {
      label: `Rainfall in mm (x10)`,
      data: multipliedRainfall,
      fill: false,
      backgroundColor: 'rgba(153,102,255,0.4)',
      borderColor: 'rgba(153,102,255,1)',
    },
  ];

  // Conditionally add the "Missing Forecast" dataset if there are missing forecasts
  if (missingForecastData.length > 0) {
    datasets.push({
      label: `Missing Forecast`,
      data: missingForecastData.map(index => ({ x: index, y: 0 })),
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
          size: 50,
        },
      },
      legend: {
        labels: {
          font: {
            size: 20, // Increase the legend text size
          },
        },
      },
      transparentWhiteBackgroundPlugin: {}, // Enable the custom plugin
    },
    scales: {
      x: {
        type: 'category',
        labels: data.labels,
      },
    },
  };

  return (
    <div className="graph-container">
      <Line data={chartData} options={options} style={style} />
    </div>
  );
};

export default Graph;