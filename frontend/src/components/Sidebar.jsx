import { useState, useContext } from 'react';
import { Link } from 'react-router-dom';
import { Drawer, Box, IconButton, Tooltip, List, ListItemText, ListItemButton } from '@mui/material';
import { Menu as MenuIcon, Login as LoginIcon } from '@mui/icons-material';
import { PublicClientApplication } from '@azure/msal-browser';
import Routes from '../config/routes';
import { msalConfig, loginRequest } from '../config/msal';
import Notification from './shared/Notification';
import UserContext from "./shared/UserContextProvider";

const pca = new PublicClientApplication(msalConfig);

function Login({open}) {
	const { userData, setUserData, clearUserData } = useContext(UserContext);
	const [notification, setNotification] = useState({ open: false, severity: "info", message: "" });

	const handleNotificationClose = () => {
		setNotification((prev) => ({ ...prev, open: false }));
	};

    const handleLogin = async () => {
        try {
			await pca.initialize();
            const loginResponse = await pca.loginPopup(loginRequest);
            const { idToken, accessToken } = loginResponse;

            const response = await fetch("/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ idToken, accessToken }),
            });

			if (!response.ok) { throw new Error("API Response failure."); }

            const data = await response.json();
			const profilePictureBase64 = `data:image/png;base64,${data.profilePicture}`;

			setUserData({
				token: data.bearer_token,
				username: data.username,
				email: data.email,
				profilePicture: profilePictureBase64,
			});
			setNotification({ open: true, severity: "success", message: "Login successful!" });
		} catch (error) {
			setNotification({ open: true, severity: "error", message: `Login failed: ${error.message}` });
		}
    };

	const handleLogout = async () => {
		await pca.logoutPopup();
		clearUserData();
		localStorage.removeItem("accessToken");
		setNotification({ open: true, severity: "info", message: "Logged out successfully."	});
	}

	return (
		<Box sx={{ display: 'flex' }} >
			{userData ? (
				<Tooltip title="Logout">
					<IconButton onClick={handleLogout}>
						<img src={userData.profilePicture} alt={userData.username} style={{ width: "28px", height: "28px", borderRadius: "50%", border: "1px solid #000" }} />
					</IconButton>
				</Tooltip>
			) : (
				<Tooltip title="Login with Microsoft">
					<IconButton onClick={handleLogin}>
						<LoginIcon />
					</IconButton>
				</Tooltip>
			)}
			{open && (
				<ListItemText primary={userData ? (<span>
					{userData.username}
					<Typography component="span" variant="body2" sx={{ fontSize: "0.8em", marginLeft: "8px", color: "gray" }}>
					  {userData.email}
					</Typography>
				  </span>) : "Login"} sx={{ marginLeft: "8px" }} />
			)}

			<Notification open={notification.open} handleClose={handleNotificationClose} severity={notification.severity} message={notification.message} />
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