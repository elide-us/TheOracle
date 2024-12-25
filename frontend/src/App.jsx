import React, { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Container, Box } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TheOracleTheme from './config/theoracletheme';
import Home from './components/Home';
import Sidebar from './components/Sidebar';


function App() {
    const [open, setOpen] = useState(false);

    return (
        <ThemeProvider theme={ TheOracleTheme }>
            <CssBaseline />
            <Router>
                <Container sx={{ width: '100%', display: 'block' }}>
                    <Sidebar open={open} setOpen={setOpen} />
                    <Box sx={{ position: 'relative', left: '30px' }}>
                        <Routes>
                            <Route path='/' element={<Home />} />
                        </Routes>
                    </Box>
                </Container>
            </Router>
        </ThemeProvider>
    );
}

export default App
