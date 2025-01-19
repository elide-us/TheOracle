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
	const { user, setUser, logoutUser } = useContext(UserContext);
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

            const { idToken, accessToken } = loginResponse;
			localStorage.setItem("accessToken", accessToken);

            const response = await fetch("/api/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ idToken, accessToken }),
            });

			if (!response.ok) {
				throw new Error("API Response failure.");
			}

            const data = await response.json();
			localStorage.setItem("internalToken", data.bearer_token);

			const profilePictureBase64 = `data:image/jpeg;base64,${data.profilePicture}`;

			setUser({ email: data.email, username: data.username, profilePicture: profilePictureBase64 });
			setNotification({
				open: true,
				severity: "success",
				message: "Login successful!",
			});
		} catch (error) {
			setNotification({
				open: true,
				severity: "error",
				message: `Login failed: ${error.message}`,
			})
		}
    };

	const handleLogout = () => {
		logoutUser();
		setNotification({
			open: true,
			severity: "info",
			message: "Logged out successfully."
		});
	}

	return (
		<Box>
			{user ? (
				<Tooltip title="Logout">
					<IconButton onClick={handleLogout}>
						<img src={user.profilePicture} alt={user.username} style={{ width: "32px", height: "32px", borderRadius: "50%" }} />
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
				<ListItemText primary={user ? "Logout" : "Login"} sx={{ marginLeft: "8px" }} />
			)}

			<Notification
				open={notification.open}
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