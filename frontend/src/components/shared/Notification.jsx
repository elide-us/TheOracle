import React from 'react';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

// Create a forwardRef Alert component for use in Snackbar
const Alert = React.forwardRef(function Alert(props, ref) {
	return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

/**
 * Notification Component
 *
 * Props:
 * - open: Boolean indicating if the Snackbar is open
 * - handleClose: Function to handle closing the Snackbar
 * - severity: Severity of the alert ('success', 'error', 'warning', 'info')
 * - message: Message to display inside the alert
 */
const Notification = ({ open, handleClose, severity, message }) => {
	return (
		<Snackbar
			open={open}
			autoHideDuration={6000} // Duration before auto-hide in milliseconds
			onClose={handleClose}
			anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }} // Position of the Snackbar
		>
			<Alert onClose={handleClose} severity={severity} sx={{ width: '100%' }}>
				{message}
			</Alert>
		</Snackbar>
	);
};

export default Notification;