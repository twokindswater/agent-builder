import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material';
import AuthenticatedLayout from './layouts/AuthenticatedLayout';
import Dashboard from './pages/Dashboard';
import Studio from './pages/Studio';

// Material UI 테마 설정
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <AuthenticatedLayout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/studio/:id" element={<Studio />} />
            {/* 추가 라우트는 여기에 */}
          </Routes>
        </AuthenticatedLayout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
