import { createTheme } from '@mui/material/styles';

const DarkTheme = createTheme({
	palette: {
	  mode: 'dark',
	  primary: { main: '#90caf9' },
	  secondary: { main: '#f48fb1' },
	},
	components: {
	  MuiIconButton: {
		styleOverrides: {
		  root: {
			color: 'lightgrey',
			'&:hover': {
			  color: 'white',
			},
		  },
		},
	  },
	  MuiListItem: {
		styleOverrides: {
		  root: {
			'&.MuiListItem-root': {
			  color: 'lightgrey !important',
			  textDecoration: 'none',
			  '&:hover': {
				color: 'white !important',
				'& .MuiSvgIcon-root': {
				  color: 'white !important',
				},
				'& .MuiListItemText-root': {
				  color: 'white !important',
				},
			  },
			  '& .MuiSvgIcon-root': {
				color: 'lightgrey !important',
			  },
			  '& .MuiListItemText-root': {
				color: 'lightgrey !important',
				'& .MuiTypography-root': {
				  color: 'lightgrey !important',
				},
			  },
			},
		  },
		},
	  },
	}
  });

  export default DarkTheme;