import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import './App.css';

import Home from './components/Home/Home';
import Sidebar from './components/Sidebar/Sidebar';
import FileManager from './components/FileManager/FileManager';
import Gallery from './components/Gallery/Gallery';
import TheOracleGPT from './components/TheOracleGPT/TheOracleGPT';
import DarkTheme from './config/darktheme';

function App() {
  const [open, setOpen] = React.useState(false);

  return (
    <ThemeProvider theme={ DarkTheme }>
      <CssBaseline />
      <Router>
        <div style={{ display: 'fixed', width: '100%' }}>
          <Sidebar open={open} setOpen={setOpen} />
          <div style={{ marginLeft: '60px' }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/file-manager" element={<FileManager />} />
              <Route path="/gallery" element={<Gallery />} />
              <Route path="/the-oracle-gpt" element={<TheOracleGPT />} />
            </Routes>
          </div>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
