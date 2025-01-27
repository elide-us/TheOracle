import { msalConfig, loginRequest } from '../../config/msal';
import Notification from './Notification';
import UserContext from "./UserContextProvider";
import { PublicClientApplication } from '@azure/msal-browser';
import { useState, useContext } from 'react';
import { Login as LoginIcon } from '@mui/icons-material';
import { Typography, Box, Tooltip, IconButton, ListItemText } from '@mui/material'

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
				token: data.bearerToken,
				username: data.username,
				email: data.email,
				profilePicture: profilePictureBase64,
				credits: data.credits,
			});
			setNotification({ open: true, severity: "success", message: "Login successful!" });
		} catch (error) {
			setNotification({ open: true, severity: "error", message: `Login failed: ${error.message}` });
		}
    };

	const handleLogout = async () => {
		await pca.logoutPopup();
		clearUserData();
		setNotification({ open: true, severity: "info", message: "Logged out successfully."	});
	}

	return (
		<Box sx={{ display: 'flex' }} >
			{userData ? (
				<Tooltip title="Logout">
					{/* <TestAuthEndpoint /> */}
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
				<ListItemText primary={userData ? (<Box>
					<Typography component="span" variant="body1" sx={{ fontWeight: "bold", color: "gray" }}>
						{userData.username}
					</Typography>
					<Typography component="span" variant="body2" sx={{ display: "block", fontSize: "0.9em", color: "gray" }}>
						{new Intl.NumberFormat(navigator.language).format(Number(userData.credits))}
					</Typography>
				  </Box>) : "Login"} sx={{ marginLeft: "8px" }} />
			)}

			<Notification open={notification.open} handleClose={handleNotificationClose} severity={notification.severity} message={notification.message} />
		</Box>
	);		
}

export default Login;