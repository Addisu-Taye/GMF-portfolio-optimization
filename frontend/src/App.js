// frontend/src/App.js
import React from 'react';
import { Container, Grid, Paper, Typography } from '@mui/material';
import ErrorBoundary from './components/ErrorBoundary';
import PriceChart from './components/PriceChart';
import ForecastChart from './components/ForecastChart';
import PortfolioAllocation from './components/PortfolioAllocation';
import BacktestChart from './components/BacktestChart';

// 👇 Import Chart.js components
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

// ✅ Register the components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  return (
    <div style={{ backgroundColor: '#f5f5f5', minHeight: '100vh', padding: 20 }}>
      <Container maxWidth="xl">
        <Typography variant="h3" align="center" gutterBottom>
          📊 GMF Portfolio Optimization Dashboard
        </Typography>
        <Typography variant="h6" align="center" color="textSecondary" gutterBottom>
          Data-Driven Investment Strategy | Week 11 Challenge
        </Typography>

        <Grid container spacing={4} style={{ marginTop: 10 }}>
          <Grid item xs={12} md={6}>
            <Paper style={{ padding: 16, height: 400 }}>
              <Typography variant="h6">Historical Prices (Last 100 Days)</Typography>
              <ErrorBoundary>
                <PriceChart />
              </ErrorBoundary>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper style={{ padding: 16, height: 400 }}>
              <Typography variant="h6">TSLA 12-Month Forecast</Typography>
              <ErrorBoundary>
                <ForecastChart />
              </ErrorBoundary>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper style={{ padding: 16, height: 400 }}>
              <Typography variant="h6">Recommended Portfolio Allocation</Typography>
              <ErrorBoundary>
                <PortfolioAllocation />
              </ErrorBoundary>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper style={{ padding: 16, height: 400 }}>
              <Typography variant="h6">Backtest: Strategy vs Benchmark</Typography>
              <ErrorBoundary>
                <BacktestChart />
              </ErrorBoundary>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </div>
  );
}

export default App;