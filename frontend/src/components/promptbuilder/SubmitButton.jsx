import { Box, Button } from '@mui/material';

const SubmitButton = ({ onClick, disabled }) => {
	return (
		<Box sx={{ display:'flex', justifyContent:'flex-end', marginTop:2 }}>
			<Button variant="contained" color="primary" onClick={onClick} disabled={disabled}>
				Submit
			</Button>
		</Box>
	);
};

export default SubmitButton;