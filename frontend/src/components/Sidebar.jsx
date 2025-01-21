import { Link } from 'react-router-dom';
import { Drawer, Box, IconButton, Tooltip, List, ListItemText, ListItemButton } from '@mui/material';
import { Menu as MenuIcon } from '@mui/icons-material';
import Routes from '../config/routes';
import Login from './shared/Login';

function Sidebar({ open, setOpen }) {
	return (
		<Drawer variant='permanent' open={open}
			sx={{ width: open ? 240 : 60, position: 'fixed', zIndex: 1300, transition: 'width 0.3s', '& .MuiDrawer-paper': { width: open ? 240 : 60 }, }}>
			<Box sx={{ padding: '12px', }}>
				<Tooltip title='Toggle Menu'>
					<IconButton onClick={() => setOpen(!open)}>
						<MenuIcon />
					</IconButton>
				</Tooltip>
			</Box>
			<List>
				{Routes.map((route, index) => (
					<ListItemButton component={Link} to={route.path} key={index}>
						<Tooltip title={route.name}>
							<route.icon />
						</Tooltip>
						{ open && <ListItemText primary={route.name} sx={{ marginLeft: '8px' }} /> }
					</ListItemButton>
				))}
			</List>
			<Box sx={{ padding: '12px', marginTop: 'auto', display: 'flex', }}>
				<Login open={open}/>
			</Box>
		</Drawer>
	);
}

export default Sidebar;