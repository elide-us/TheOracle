// import { useState } from 'react';
import { Box, Select, Typography, MenuItem } from "@mui/material";

import dataLayer1 from './data_layer1.json';
import dataLayer2 from './data_layer2.json';
import dataLayer3 from './data_layer3.json';
import dataLayer4 from './data_layer4.json';

const LayerBox = ({ parts, data }) => {
	// const [selectedValues, setSelectedValues] = useState({});
	// const handleSelectChange = (groupIndex, event) => {
	// 	const { value } = event.target;
	// 	setSelectedValues((prev) => ({
	// 		...prev,
	// 		[groupIndex]: value,
	// 	}));
	// };

	const groupedParts = [];
	let tempGroup = [];

	parts.forEach((part, index) => {
		tempGroup.push({ ...part, key: index });
		if (part.type === 'dropdown') {
			groupedParts.push([...tempGroup]);
			tempGroup = [];
		}
	});

	if (tempGroup.length > 0) {
		groupedParts.push([...tempGroup]);
	}

	return (
		<Box display="flex" flexWrap="wrap" gap={2}>
			{groupedParts.map((group, groupIndex) => (
				<Box
					key={`group-${groupIndex}`}
					display="flex"
					alignItems="center"
				>
					{group.map((part) => {
						if (part.type === 'text') {
							return (
							<span key={`text-${part.key}`} style={{ marginRight: '8px' }}>
								{part.text}
							</span>
							);
						} else if (part.type === 'dropdown') {
							const options = data[part.placeholder] || {};
							return (
								<Select
									key={`select-${part.key}`}
									size="small"
									sx={{ minWidth: 120 }}
									autoWidth
									defaultValue=""
								>
									{Object.keys(options).map((key) => (
										<MenuItem key={key} value={key}>
											{key}
										</MenuItem>
									))}
								</Select>
							);
						}
						return null;
					})}
				</Box>
			))}
		</Box>
	);
};

// const LayerBox2 = ({ parts, data }) => {
// 	const [selectedValues, setSelectedValues] = useState({});
// 	const handleSelectChange = (groupIndex, event) => {
// 		const { value } = event.target;
// 		setSelectedValues((prev) => ({
// 			...prev,
// 			[groupIndex]: value,
// 		}));
// 	};
// 	const groupedParts = [];
// 	let tempGroup = [];
// 	parts.forEach((part, index) => {
// 		tempGroup.push({ ...part, key: index });
// 		if (part.type === 'dropdown') {
// 			groupedParts.push([...tempGroup]);
// 			tempGroup = [];
// 		}
// 	});
// 	if (tempGroup.length > 0) {
// 		groupedParts.push([...tempGroup]);
// 	}
// 	return (
// 		<Box display="flex" flexDirection="column" gap={2}>
// 			{groupedParts.map((group, groupIndex) => {
// 				const dropdownPart = group.find((part) => part.type === 'dropdown');
// 				const placeholder = dropdownPart ? dropdownPart.placeholder : null;
// 				return (
// 					<Box
// 						key={`group-${groupIndex}`}
// 						display="flex"
// 						flexDirection="column"
// 					>
// 						<Box display="flex" alignItems="center" gap={1}>
// 							{group.map((part) => {
// 								if (part.type === 'text') {
// 									return (
// 									<Typography
// 										key={`text-${part.key}`}
// 										variant="body1"
// 										style={{ marginRight: '8px' }}
// 									>
// 										{part.text}
// 									</Typography>
// 									);
// 								} else if (part.type === 'dropdown') {
// 									const options = data[part.placeholder] || {};
// 									return (
// 									<Select
// 										key={`select-${part.key}`}
// 										size="small"
// 										sx={{ minWidth: 120 }}
// 										value={selectedValues[groupIndex] || ''}
// 										onChange={(event) => handleSelectChange(groupIndex, event)}
// 										displayEmpty
// 									>
// 										<MenuItem value="" disabled>Select</MenuItem>
// 										{Object.keys(options).map((key) => (
// 										<MenuItem key={key} value={key}>
// 											{key}
// 										</MenuItem>
// 										))}
// 									</Select>
// 									);
// 								}
// 								return null;
// 							})}
// 						</Box>
// 						{selectedValues[groupIndex] && (
// 							<Box sx={{
// 								marginTop:2,
// 								padding:2,
// 								border:'1px solid #ccc',
// 								backgroundColor:'#000',
// 							}}>
// 								<Typography variant="body2">
// 									{data[placeholder]?.[selectedValues[groupIndex]] || 'No description available.'}
// 								</Typography>
// 							</Box>
// 						)}
// 					</Box>
// 				)}
// 			)}
// 		</Box>
// 	  );
// };

const PromptBuilderOptionSelector = ({ selectedTemplate }) => {
    const parseTemplate = (text) => {
        const pattern = /{([^}]+)}/g;
        const parts = [];
    
        let lastIndex = 0;
        let match;
    
        while ((match = pattern.exec(text)) !== null) {
            if (match.index > lastIndex) {
                parts.push({ type: "text", text: text.slice(lastIndex, match.index) });
            }
            parts.push({ type: "dropdown", placeholder: match[1] });
            lastIndex = pattern.lastIndex;
        }
    
        if (lastIndex < text.length) {
            parts.push({ type: "text", text: text.slice(lastIndex) });
        }
      
        return parts;
    };
  
    const layers = [
        { label: 'Foundational Layers', parts: parseTemplate(selectedTemplate.layer1 || ''), data: dataLayer1 },
        { label: 'Structural Layers', parts: parseTemplate(selectedTemplate.layer2 || ''), data: dataLayer2 },
        { label: 'Styling Layers', parts: parseTemplate(selectedTemplate.layer3 || ''), data: dataLayer3 },
        { label: 'Narrative Layers', parts: parseTemplate(selectedTemplate.layer4 || ''), data: dataLayer4 }
    ];
  
    return (
        <Box sx={{ flexGrow: 1 }}>
            {layers.map((layer, index) => (
                <Box key={index} sx={{
                    marginTop: 2,
                    padding: 2,
                    border: '2px solid #000',
                    borderRadius: '6px',
                }}>
                    <Typography variant="h6" sx={{ marginLeft:1 }} gutterBottom>
                        {layer.label}
                    </Typography>
                    <LayerBox parts={layer.parts} data={layer.data} />
                </Box>
            ))}
        </Box>
    );
};

const PromptBuilderHeader = ({ selectedTemplate }) => {
	return (
		<Box>
			<Typography variant="h4" component="h1" gutterBottom>
				{selectedTemplate.title}
			</Typography>
			<Typography variant="body1" gutterBottom>
				{selectedTemplate.description}
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

const PromptBuilderInputBar = ({ selectedTemplate }) => {
	return (
		<Box>
			<Typography variant="subtitle1" gutterBottom>
				{selectedTemplate.input}
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

const PromptBuilder = ({ selectedTemplate }) => {
	return ( selectedTemplate ? (
		<Box sx={{ padding: 2, backgroundColor: '#333', }}>
			<Box
				sx={{
					padding: 2,
					border: '2px solid #000',
					borderRadius: '6px',
					backgroundColor: '#212121', // Slightly lighter than #111
					display: 'flex',
					flexDirection: 'column',
					minHeight: 'calc(100vh - 24px)',
				}}
			>
				<PromptBuilderHeader selectedTemplate={selectedTemplate} />
				<PromptBuilderOptionSelector selectedTemplate={selectedTemplate} />
				<Box>
					<PromptBuilderComplexityBar percentage={'70%'} />
					<PromptBuilderInputBar selectedTemplate={selectedTemplate} />
				</Box>
			</Box>
		</Box>
	) : (
		<Box sx={{ padding: 4, textAlign: 'center', }}>
			<Typography variant="h6" color="textSecondary">
				Please select a template to get started.
			</Typography>
		</Box>
	));
};

export default PromptBuilder;
