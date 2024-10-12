import React from 'react';
import { Line } from 'react-chartjs-2';
import 'chart.js/auto';

const Graph = ({ data, area, style }) => {
  const chartData = {
    labels: data.labels,
    datasets: [
      {
        label: `Usage Minutes`,
        data: data.usageMinutes,
        fill: false,
        backgroundColor: 'rgba(75,192,192,0.4)',
        borderColor: 'rgba(75,192,192,1)',
      },
      {
        label: `Rainfall`,
        data: data.rainfall,
        fill: false,
        backgroundColor: 'rgba(153,102,255,0.4)',
        borderColor: 'rgba(153,102,255,1)',
      },
    ],
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