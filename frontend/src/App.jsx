import { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Container, Box } from '@mui/material';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TheOracleTheme from './config/theoracletheme';
import Sidebar from './components/Sidebar';
import Home from './components/Home';
import FileManager from './components/FileManager';
import Gallery from './components/Gallery';
import TheOracleGPT from './components/TheOracleGPT';
import Prism from './components/Prism';
import CategoryEditor from './components/CategoryEditor';
import KeyEditor from './components/KeyEditor';

function App() {
	const [open, setOpen] = useState(false);

	return (
		<ThemeProvider theme={ TheOracleTheme }>
			<CssBaseline />
			<Router>
				<Container sx={{ width: '100%', display: 'block' }}>
					<Sidebar open={open} setOpen={setOpen} />
					<Box sx={{ position: 'relative', left: '40px' }}>
						<Routes>
							<Route path='/' element={<Home />} />
							<Route path='/file-manager' element={<FileManager />} />
							<Route path='/gallery' element={ <Gallery /> } />
							<Route path='/the-oracle-gpt' element={ <TheOracleGPT /> } />
							<Route path='/prism' element={ <Prism /> } />
							<Route path='/cat-edit' element={ <CategoryEditor /> } />
							<Route path='/key-edit' element={ <KeyEditor /> } />
						</Routes>
					</Box>
				</Container>
			</Router>
		</ThemeProvider>
	);
}

export default App;
