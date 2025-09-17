import { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline, Container, Box } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { UserContextProvider } from './components/shared/UserContextProvider'
import TheOracleTheme from './config/theoracletheme';
import Sidebar from './components/Sidebar';
import Home from './components/Home';
import TheOracleGPT from './components/TheOracleGPT';
import LoginPage from './components/LoginPage';
import UserPanel from './components/UserPanel';

function App() {
	const [open, setOpen] = useState(false);

	return (
		<ThemeProvider theme={ TheOracleTheme }>
			<CssBaseline />
			<UserContextProvider>
				<Router>
					<Container sx={{ width: '100%', display: 'block' }}>
						<Sidebar open={open} setOpen={setOpen} />
						<Box sx={{ position: 'relative', left: '40px' }}>
							<Routes>
								<Route path='/' element={<Home />} />
                                                                <Route path='/the-oracle-gpt' element={ <TheOracleGPT /> } />
                                                                <Route path='/login' element={<LoginPage />} />
                                                                <Route path='/userpanel' element={<UserPanel />} />
							</Routes>
						</Box>
					</Container>
				</Router>
			</UserContextProvider>
		</ThemeProvider>
	);
}

export default App;
