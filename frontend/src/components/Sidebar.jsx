import { Drawer, Box, IconButton, Tooltip, List, ListItem, ListItemText, ListItemButton } from '@mui/material';
import { Menu as MenuIcon, Login as LoginIcon } from '@mui/icons-material';
import { PublicClientApplication } from '@azure/msal-browser';
import { Link } from 'react-router-dom';
import Routes from '../config/routes';
import { msalConfig, loginRequest } from '../config/msal';

const pca = new PublicClientApplication(msalConfig);

function Login({open}) {
    const handleLogin = async () => {
        try {
			await pca.initialize();

            const loginResponse = await pca.loginPopup(loginRequest);
            const { idToken, account } = loginResponse;

            // Send the ID token to your FastAPI backend
            const response = await fetch("/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ idToken }),
            });

            const data = await response.json();
            console.log("Login successful, received token:", data.token);
        } catch (error) {
            console.error("Login failed:", error);
        }
    };

	return (
		<Box>
			<Tooltip title='Login with Microsoft'>
				<IconButton onClick={handleLogin}>
					<LoginIcon />
				</IconButton>
			</Tooltip>
			{open && <ListItemText primary='Login' sx={{ marginLeft: '8px', }} />}
		</Box>
	);		
}

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