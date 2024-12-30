import { Typography, Box } from "@mui/material";
import { useState } from 'react';

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
		<Box
			sx={{
				padding: 4,
				border: '1px solid #e0e0e0',
				borderRadius: 2,
				boxShadow: 1,
				backgroundColor: '#fafafa',
			}}
		>
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
 	);
};

const Tile = ({ template, onTileClick }) => {
	return (
		<Box
			key={template.title}
			className="tile"
			onClick={() => onTileClick(template.title)}
			sx={{
				border: '1px solid #ccc',
				borderRadius: 2,
				padding: 2,
				cursor: 'pointer',
			}}
		>
			<Typography variant="subtitle1">{template.title}</Typography>
			<Box
				component="img"
				src={template.imageUrl}
				alt={template.title}
				sx={{ width: '100%', height: 'auto', marginTop: 1 }}
			/>
		</Box>
	);
};

const TileGrid = ({ templates, onTileClick }) => {
	return (
		<Box
			sx={{
				display: 'grid',
				gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
				gap: 2,
				marginTop: 2,
				border: '1px solid #CCC',
				padding: '12px',
				background: '#000',
			}}
		>
			{templates.map((template, index) => (
			<Tile
				key={index}
				template={template}
				onTileClick={onTileClick}
			/>
			))}
		</Box>
	);
};

const CategoryBox = ({ categoryName, templates, onTileClick }) => {
	return (
		<Box sx={{
			marginBottom: 4,
			marginLeft: 4,
			marginRight: 4,
			border: '1px solid #ccc',
			borderRadius:'12px',
			padding:'12px',
			background: '#333',
		}}>
			<Typography variant="h6" gutterBottom>
				{categoryName}
			</Typography>
			<TileGrid templates={templates} onTileClick={onTileClick} />
		</Box>
	);
};

const CategoryList = ({ categories, onTileClick }) => {
	return (
		<Box>
			<Typography variant="h5" gutterBottom>Select Persona:</Typography>
			{Object.entries(categories).map(([categoryName, templates]) => (
				<CategoryBox
					key={categoryName}
					categoryName={categoryName}
					templates={templates}
					onTileClick={onTileClick}
				/>
			))}
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
                <Typography>Selected Template</Typography>
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
