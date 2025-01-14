import { Box, Typography } from '@mui/material';
import { useState } from 'react';

const KeyEditor = () => {
    const [selectedTemplate, setSelectedTemplate] = useState({});
    return (
        <Box sx={{ padding:1 }}>
            <Typography variant='h3'>KeyEditor</Typography>
        </Box>
    )
}

export default KeyEditor;