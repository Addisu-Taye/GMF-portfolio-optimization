// frontend/src/components/BacktestChart.jsx
import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import api from '../services/api';

export default function BacktestChart() {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.get('/api/portfolio/backtest')
      .then(res => {
        const results = res.data;
        const labels = ['Strategy', 'Benchmark'];
        const returns = [results.strategy_return, results.benchmark_return];
        const sharpe = [results.strategy_sharpe.toFixed(3), results.benchmark_sharpe.toFixed(3)];

        setChartData({
          labels,
          datasets: [
            {
              label: 'Total Return (%)',
               returns,
              backgroundColor: ['rgba(54, 162, 235, 0.6)', 'rgba(255, 99, 132, 0.6)'],
              borderColor: ['rgba(54, 162, 235, 1)', 'rgba(255, 99, 132, 1)'],
              borderWidth: 1
            }
          ]
        });

        // Optional: Log Sharpe Ratios
        console.log("Backtest Sharpe Ratios:", sharpe);
      })
      .catch(err => {
        console.error("Backtest API error:", err);
        setError("Failed to load backtest results. Check backend.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) return <div>📈 Running backtest simulation...</div>;
  if (error) return <div style={{ color: 'red' }}>❌ {error}</div>;
  if (!chartData || !chartData.datasets) return <div>No backtest data available.</div>;

  return <Bar data={chartData} options={{ responsive: true, scales: { y: { beginAtZero: true } } }} />;
}