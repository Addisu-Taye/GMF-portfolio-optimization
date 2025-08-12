// frontend/src/components/PortfolioAllocation.jsx
import React, { useEffect, useState } from 'react';
import { Doughnut } from 'react-chartjs-2';
import api from '../services/api';

export default function PortfolioAllocation() {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.get('/api/portfolio/optimal')
      .then(res => {
        const weights = res.data.weights;
        const labels = weights.map(w => w.asset);
        const data = weights.map(w => w.weight * 100); // Convert to percentage

        setChartData({
          labels,
          datasets: [{
            data,
            backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            hoverOffset: 10
          }]
        });
      })
      .catch(err => {
        console.error("Failed to load portfolio allocation:", err);
        setError("Failed to load optimal portfolio. Check backend.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) return <div>📊 Calculating optimal allocation...</div>;
  if (error) return <div style={{ color: 'red' }}>❌ {error}</div>;
  if (!chartData || !chartData.datasets) return <div>No portfolio data available.</div>;

  return <Doughnut data={chartData} options={{ responsive: true }} />;
}