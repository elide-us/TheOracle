import { useState } from 'react';
import { Typography, Box } from "@mui/material";

import CategoryList from './CategoryList';
import data from './templates.json';

const PromptBuilder = ({ selectedTemplate }) => {
	if (!selectedTemplate) {
		return (
			<Box
				sx={{
					padding: 4,
					textAlign: 'center',
				}}
			>
				<Typography variant="h6" color="textSecondary">
					Please select a template to get started.
				</Typography>
			</Box>
		);
	}

  	return (
		<Box sx={{
			padding: 2,
			backgroundColor: '#333',
		}}>
			<Box sx={{
				padding: 2,
				border: '1px solid #000',
				borderRadius: '6px',
				backgroundColor: '#212121', // Slightly lighter than #111
				boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.5)', // Adds depth
				display: 'flex',
				flexDirection: 'column',
				minHeight: 'calc(100vh - 24px)',
			}}>
				<Typography variant="h4" component="h1" gutterBottom>
					{selectedTemplate.title}
				</Typography>
				<Typography variant="body1" gutterBottom>
					Here goes the template prompting system for <strong>{selectedTemplate.title}</strong>.
				</Typography>
				{selectedTemplate.imageUrl && (
					<Box
						component="img"
						src={selectedTemplate.imageUrl}
						alt={`${selectedTemplate.title} preview`}
						sx={{
							width: '100%',
							maxWidth: '600px',
							borderRadius: 2,
							marginTop: 2,
						}}
					/>
				)}

				<Box sx={{
					flexGrow: 1,
				}} />

				{/* Add complexity bar, input bar, etc. */}
				<Box sx={{ marginTop: 4 }}>
					{/* Placeholder for Complexity Bar */}
					<Typography variant="subtitle1" gutterBottom>
						Complexity Level
					</Typography>
					<Box
						sx={{
							height: 10,
							backgroundColor: '#e0e0e0',
							borderRadius: 5,
							position: 'relative',
							marginBottom: 3,
						}}
					>
					<Box
						sx={{
							width: '70%', // Example percentage
							height: '100%',
							backgroundColor: '#3f51b5',
							borderRadius: 5,
						}}
					/>
					</Box>

					{/* Placeholder for Input Bar */}
					<Typography variant="subtitle1" gutterBottom>
						Input
					</Typography>
					<Box
						component="textarea"
						placeholder="Enter your prompt here..."
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
			</Box>
			
		</Box>
 	);
};

function TheOracleGPT() {
    const [selectedTemplate, setSelectedTemplate] = useState(null);
    
    const handleTileClick = (template) => {
        setSelectedTemplate(template);
    };

    if (selectedTemplate) {
        return (
            <Box>
                <PromptBuilder selectedTemplate={selectedTemplate} />
            </Box>
        )
    }

    return (
        <Box>
            <CategoryList categories={data} onTileClick={handleTileClick} />
        </Box>
    )
}

export default TheOracleGPT;
