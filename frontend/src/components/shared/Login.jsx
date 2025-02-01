import { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Login as LoginIcon } from '@mui/icons-material';
import { Typography, Box, Tooltip, IconButton, ListItemText } from '@mui/material';
import { PublicClientApplication } from '@azure/msal-browser';
import { msalConfig } from '../../config/msal';
import Notification from './Notification';
import UserContext from './UserContextProvider';

const pca = new PublicClientApplication(msalConfig);

function Login({ open }) {
  const { userData, clearUserData } = useContext(UserContext);
  const [notification, setNotification] = useState({
    open: false,
    severity: "info",
    message: ""
  });
  const navigate = useNavigate();

  const handleNotificationClose = () => {
    setNotification((prev) => ({ ...prev, open: false }));
  };

  // When not logged in, navigate to the dedicated login page.
  const handleLoginNavigation = () => {
    navigate('/login');
  };

  // When logged in, clicking on the icon logs the user out.
  const handleLogout = async () => {
    try {
	  await pca.initialize();
      await pca.logoutPopup();
      clearUserData();
      setNotification({
        open: true,
        severity: "info",
        message: "Logged out successfully."
      });
    } catch (error) {
      setNotification({
        open: true,
        severity: "error",
        message: `Logout failed: ${error.message}`
      });
    }
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'center' }}>
      {userData ? (
        <Tooltip title="Logout">
          <IconButton onClick={handleLogout}>
            <img
              src={userData.profilePicture}
              alt={userData.username}
              style={{
                width: "28px",
                height: "28px",
                borderRadius: "50%",
                border: "1px solid #000"
              }}
            />
          </IconButton>
        </Tooltip>
      ) : (
        <Tooltip title="Login">
          <IconButton onClick={handleLoginNavigation}>
            <LoginIcon />
          </IconButton>
        </Tooltip>
      )}

      {open && (
        <ListItemText
          primary={
            userData ? (
              <Box>
                <Typography
                  component="span"
                  variant="body1"
                  sx={{ fontWeight: "bold", color: "gray" }}
                >
                  {userData.username}
                </Typography>
                <Typography
                  component="span"
                  variant="body2"
                  sx={{ display: "block", fontSize: "0.9em", color: "gray" }}
                >
                  {new Intl.NumberFormat(navigator.language).format(Number(userData.credits))}
                </Typography>
              </Box>
            ) : "Login"
          }
          sx={{ marginLeft: "8px" }}
        />
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

export default Login;
