import { Box, Typography } from '@mui/material';

const ComplexityBar = ({ percentage }) => {
    return (
        <Box>
            <Typography variant="subtitle1" gutterBottom>
                Complexity Level
            </Typography>
            <Box sx={{
                height: 10,
                backgroundColor: '#e0e0e0',
                borderRadius: 5,
                position: 'relative',
                marginBottom: 3,
            }}>
                <Box sx={{
                    width: percentage,
                    height: '100%',
                    backgroundColor: '#3f51b5',
                    borderRadius: 5,
                }} />
            </Box>
        </Box>
    );
};

export default ComplexityBar;