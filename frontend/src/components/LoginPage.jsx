import { useContext, useState } from 'react';
import { Container, Paper, Typography, Button, Stack } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { PublicClientApplication } from '@azure/msal-browser';
import { msalConfig, loginRequest } from '../config/msal'; // adjust import path as needed
import UserContext from './shared/UserContextProvider';
import Notification from './shared/Notification';

const pca = new PublicClientApplication(msalConfig);

function LoginPage() {
  const { setUserData } = useContext(UserContext);
  const [notification, setNotification] = useState({
    open: false,
    severity: 'info',
    message: ''
  });
  const navigate = useNavigate();

  const handleNotificationClose = () => {
    setNotification((prev) => ({ ...prev, open: false }));
  };

  const handleMicrosoftLogin = async () => {
    try {
      // Initialize and perform Microsoft login via popup
      await pca.initialize();
      const loginResponse = await pca.loginPopup(loginRequest);
      const { idToken, accessToken } = loginResponse;

      // Send tokens to your backend for verification and to retrieve user details
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idToken, accessToken })
      });

      if (!response.ok) {
        throw new Error('API Response failure.');
      }

      const data = await response.json();
      const profilePictureBase64 = `data:image/png;base64,${data.profilePicture}`;

      // Save user details in context
      setUserData({
        token: data.bearerToken,
        username: data.username,
        email: data.email,
        profilePicture: profilePictureBase64,
        credits: data.credits
      });

      setNotification({
        open: true,
        severity: 'success',
        message: 'Login successful!'
      });

      // Navigate back to home page after a successful login
      navigate('/');
    } catch (error) {
      setNotification({
        open: true,
        severity: 'error',
        message: `Login failed: ${error.message}`
      });
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Paper elevation={3} sx={{ marginTop: 8, padding: 4 }}>
        <Typography component="h1" variant="h5" align="center">
          Sign in
        </Typography>
        <Typography variant="body2" align="center" sx={{ mt: 2 }}>
          Only OAuth providers are supported. Please sign in using one of the following services:
          <br />
          Microsoft, Discord, Google, or Apple.
          <br />
          <strong>Note:</strong> Email-only login is not available.
        </Typography>
        <Stack spacing={2} sx={{ mt: 4 }}>
          <Button variant="contained" fullWidth onClick={handleMicrosoftLogin}>
            Sign in with Microsoft
          </Button>
          <Button variant="outlined" fullWidth disabled>
            Sign in with Discord (Coming Soon)
          </Button>
          <Button variant="outlined" fullWidth disabled>
            Sign in with Google (Coming Soon)
          </Button>
          <Button variant="outlined" fullWidth disabled>
            Sign in with Apple (Coming Soon)
          </Button>
        </Stack>
      </Paper>
      <Notification
        open={notification.open}
        handleClose={handleNotificationClose}
        severity={notification.severity}
        message={notification.message}
      />
    </Container>
  );
}

export default LoginPage;
