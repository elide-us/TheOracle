import { Drawer, Box, IconButton, Tooltip, List, ListItemText, ListItemButton } from '@mui/material';
import { Menu as MenuIcon, Login as LoginIcon } from '@mui/icons-material';
import { PublicClientApplication } from '@azure/msal-browser';
import { Link } from 'react-router-dom';
import Routes from '../config/routes';
import { msalConfig, loginRequest } from '../config/msal';
import Notification from './shared/Notification';
import { useState } from 'react';

const pca = new PublicClientApplication(msalConfig);

function Login({open}) {
	const [notification, setNotification] = useState({
		open: false,
		severity: "info",
		message: "",
	});

	const handleNotificationClose = () => {
		setNotification((prev) => ({ ...prev, open: false }));
	};

    const handleLogin = async () => {
        try {
			await pca.initialize();

            const loginResponse = await pca.loginPopup(loginRequest);
            //const { idToken, account } = loginResponse;
            const { idToken } = loginResponse;
			console.log("ID Token:", idToken);

            const response = await fetch("/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ idToken }),
            });

			if (!response.ok) {
				throw new Error("Login failed");
			}

            const data = await response.json();
			localStorage.setItem("accessToken", data.token);

			setNotification({
				open: true,
				severity: "success",
				message: "Login successful! Token stored.",
			});
		} catch (error) {
			setNotification({
				open: true,
				severity: "error",
				message: `Login failed: ${error.message}`,
			})
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
			<Notification open={notification.open}
				handleClose={handleNotificationClose}
				severity={notification.severity}
				message={notification.message}
			/>
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