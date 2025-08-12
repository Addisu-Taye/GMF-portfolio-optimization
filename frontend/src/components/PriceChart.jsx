// frontend/src/components/PriceChart.jsx
import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import api from '../services/api';

export default function PriceChart() {
  const [chartData, setChartData] = useState(null);  // null = not loaded
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.get('/api/data/prices')
      .then(res => {
        const prices = res.data;
        const labels = prices.map(p => p.Date?.slice(0, 10));
        const tsla = prices.map(p => p.TSLA);
        const spy = prices.map(p => p.SPY);
        const bnd = prices.map(p => p.BND);

        setChartData({
          labels: labels.slice(-100),
          datasets: [
            { label: 'TSLA', data: tsla.slice(-100), borderColor: '#FF6384' },
            { label: 'SPY', data: spy.slice(-100), borderColor: '#36A2EB' },
            { label: 'BND', data: bnd.slice(-100), borderColor: '#FFCE56' }
          ]
        });
      })
      .catch(err => {
        console.error("Failed to load price data:", err);
        setError("Failed to load price data. Check if the backend is running.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div style={{ color: 'blue', textAlign: 'center', margin: '20px' }}>
      🔍 Loading price data...
    </div>;
  }

  if (error) {
    return <div style={{ color: 'red', textAlign: 'center', margin: '20px' }}>
      ❌ {error}
    </div>;
  }

  if (!chartData || !chartData.datasets) {
    return <div>No chart data available.</div>;
  }

  return <Line data={chartData} options={{ responsive: true, maintainAspectRatio: false }} />;
}