// frontend/src/components/ForecastChart.jsx
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import api from '../services/api';

export default function ForecastChart() {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.get('/api/forecast/future')
      .then(res => {
        const forecast = res.data;
        const labels = forecast.map(f => f.date);
        const prices = forecast.map(f => f.price);

        setChartData({
          labels,
          datasets: [{
            label: 'TSLA Forecast',
             prices,
            borderColor: 'green',
            fill: false,
            tension: 0.2
          }]
        });
      })
      .catch(err => {
        console.error("Failed to load forecast ", err);
        setError("Failed to load TSLA forecast. Is the backend running?");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) return <div>🔍 Loading TSLA forecast...</div>;
  if (error) return <div style={{ color: 'red' }}>❌ {error}</div>;
  if (!chartData || !chartData.datasets) return <div>No forecast data available.</div>;

  return <Line data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />;
}