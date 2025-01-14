import { Box, Typography } from '@mui/material';

const PageTitle = ({title}) => {
    return (
        <Box sx={{ padding: 1, margin: 1, border: '3px solid #ccc', borderRadius: 4 }}>
            <Typography variant="h3">{title}</Typography>
        </Box>
    );
}

export { PageTitle };