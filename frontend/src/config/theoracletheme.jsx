import { createTheme } from '@mui/material/styles';

const TheOracleTheme = createTheme({
	palette: {
		mode: 'dark',
		primary: { main: '#90caf9' },
		secondary: { main: '#f48fb1' },
		background: { default: '#121212', paper: '#1e1e1e' },
		text: { primary: '#ffffff', secondary: '#b0b0c5' }
	},
	typography: {
		fontFamily: 'Roboto, Arial, sans-serif',
		h1: { fontSize: '2rem', fontWeight: 500 },
		h2: { fontSize: '1.75rem', fontWeight: 500 },
		body1: { fontSize: '1rem', lineHeight: 1.5 },
		button: { textTransform: 'none' }
	},
	components: {
		MuiIconButton: {
			styleOverrides: {
				root: {
					color: 'lightgrey !important',
					'&:hover': {
						color: 'white !important',
					}
				}
			}
		},
		MuiListItem: {
			styleOverrides: {
				root: {
					color: 'lightgrey !important',
					'& .MuiListItemText-root': {
						color: 'lightgrey !important',
					},
					'&:hover': {
						color: 'white !important',
							'& .MuiListItemText-root': {
							color: 'white !important',
						}
					}
				}
			}
		}
    }
});

export default TheOracleTheme;
