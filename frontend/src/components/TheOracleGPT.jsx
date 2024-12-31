import { useState } from 'react';
import { Typography, Box } from "@mui/material";

import CategoryList from './CategoryList';
import data from './templates.json';

const PromptBuilderHeader = ({ selectedTemplate }) => {
	return (
		<Box>
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
		</Box>
	);
};

const PromptBuilderComplexityBar = ({ percentage }) => {
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

const PromptBuilderInputBar = ({ }) => {
	return (
		<Box>
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
	);
};

const PromptBuilderOptionSelector = ({ selectedTemplate }) => {
	return (
		<Box sx={{ flexGrow:1 }}>
			<Box sx={{ marginTop:1 }}>
				<Typography>Template dropdowns here</Typography>
			</Box>
		</Box>
	);
};

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
				border: '2px solid #000',
				borderRadius: '6px',
				backgroundColor: '#212121', // Slightly lighter than #111
				display: 'flex',
				flexDirection: 'column',
				minHeight: 'calc(100vh - 24px)',
			}}>
				<PromptBuilderHeader selectedTemplate={selectedTemplate} />
				<PromptBuilderOptionSelector selectedTemplate={selectedTemplate} />
				<Box>
					<PromptBuilderComplexityBar percentage={'70%'} />
					<PromptBuilderInputBar />
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
