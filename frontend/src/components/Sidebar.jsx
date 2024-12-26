import { Drawer, Box, IconButton, Tooltip, List, ListItem, ListItemText } from '@mui/material';
import { Menu as MenuIcon, Login as LoginIcon } from '@mui/icons-material';
import { Link } from 'react-router-dom';
import Routes from '../config/routes';

function Sidebar({ open, setOpen }) {
	return (
		<Drawer variant='permanent' open={open}
			sx={{ width: open ? 240 : 40, position: 'fixed', zIndex: 1300, transition: 'width 0.3s', '&.MuiDrawer-paper': { width: open ? 240 : 30 }, }}>
			<Box sx={{ padding: '12px', }}>
				<Tooltip title='Toggle Menu'>
					<IconButton onClick={() => setOpen(!open)}>
						<MenuIcon />
					</IconButton>
				</Tooltip>
			</Box>
			<List>
				{Routes.map((route, index) => (
					<ListItem button component={Link} to={route.path} key={index}>
						<Tooltip title={route.name}>
							<route.icon />                 
						</Tooltip>
						{ open && <ListItemText primary={route.name} sx={{ marginLeft: '8px' }} /> }
					</ListItem>
				))}
			</List>
			<Box sx={{ padding: '12px', marginTop: 'auto', display: 'flex', }}>
				<Tooltip title='Login with Microsoft'>
					<IconButton>
						<LoginIcon />
					</IconButton>
				</Tooltip>
				{ open && <ListItemText primary='Login' sx={{ marginLeft: '8px', }} /> }
			</Box>
		</Drawer>
	);
}

export default Sidebar;