import { Box, Typography } from '@mui/material';

const InputBar = ({ selectedTemplate, inputText, setInputText }) => {
    return (
        <Box>
            <Typography variant="subtitle1" gutterBottom>
                {selectedTemplate.input}
            </Typography>
            <Box
                component="textarea"
                placeholder="Enter your prompt here..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                sx={{
                    width: '100%',
                    minHeight: '100px',
                    padding: 2,
                    border: '1px solid #ccc',
                    borderRadius: 2,
                    resize: 'vertical',
                    fontSize: '1rem',
                    fontFamily: 'Roboto, sans-serif',
                }}
            />
        </Box>
    );
};

export default InputBar;