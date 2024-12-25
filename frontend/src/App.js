import React, { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Box, Container } from '@mui/material';
import DarkTheme from './config/darktheme';
import Sidebar from './components/Sidebar';
import Home from './pages/Home';
import FileManager from './pages/FileManager';
import Gallery from './pages/Gallery';
import TheOracleGPT from './pages/TheOracleGPT';


function App() {
	const [open, setOpen] = useState(false);

	return (
		<ThemeProvider theme={ DarkTheme }>
            <CssBaseline />
            <Router>
                <Container sx={{ width: '100%', display: 'block' }}>
                    <Sidebar open={open} setOpen={setOpen} />
                    <Box sx={{ position: 'relative', left: '30px' }}>
                        <Routes>
                            <Route path='/' element={<Home />} />
                            <Route path="/file-manager" element={<FileManager />} />
                            <Route path="/gallery" element={<Gallery />} />
                            <Route path="/the-oracle-gpt" element={<TheOracleGPT />} />
                        </Routes>
                    </Box>
                </Container>
            </Router>
		</ThemeProvider>
	);
}

export default App;
