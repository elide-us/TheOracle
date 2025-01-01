import { useState, useEffect } from 'react';
import { Box, Button, Select, Typography, MenuItem, CircularProgress } from '@mui/material';

import Notification from './shared/Notification';

import dataLayer1 from './data_layer1.json';
import dataLayer2 from './data_layer2.json';
import dataLayer3 from './data_layer3.json';
import dataLayer4 from './data_layer4.json';

const SubmitButton = ({ onClick }) => {
	return (
		<Box sx={{ display:'flex', justifyContent:'flex-end', marginTop:2 }}>
			<Button variant="contained" color="primary" onClick={onClick}>
				Submit
			</Button>
		</Box>
	);
};

const LayerBox = ({ parts, data, selections, setSelections }) => {
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
				<Box key={`group-${groupIndex}`} display="flex" alignItems="center">
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
									size='small'
									sx={{ minWidth: 120 }}
									displayEmpty
									autoWidth
									value={selections[part.placeholder] || ''}
									onChange={(e) =>
										setSelections((prev) => ({
											...prev,
											[part.placeholder]: e.target.value,
										}))
									  }							
								>
									<MenuItem value="">Select {part.placeholder}</MenuItem>
									{Object.keys(options).map((key) => (
										<MenuItem key={key} value={key}>{key}</MenuItem>
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

const PromptBuilderInputBar = ({ selectedTemplate, inputText, setInputText }) => {
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

const PromptBuilderOptionSelector = ({ selectedTemplate, selections, setSelections }) => {
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
                    <LayerBox parts={layer.parts} data={layer.data} selections={selections} setSelections={setSelections} />
                </Box>
            ))}
        </Box>
    );
};

const PromptBuilderHeader = ({ selectedTemplate, currentImageUrl, isLoading }) => {
	return (
		<Box>
			<Typography variant="h4" component="h1" gutterBottom>
				{selectedTemplate.title}
			</Typography>
			<Typography variant="body1" gutterBottom>
				{selectedTemplate.description}
			</Typography>
			{currentImageUrl && (
				<Box sx={{ position: "relative", marginTop: 2 }}>
					<Box
						component="img"
						src={currentImageUrl}
						alt={`${selectedTemplate.title} preview`}
						sx={{
							width: "100%",
							maxWidth: "600px",
							borderRadius: 2,
							display: "block",
						}}
					/>
					{isLoading && (
						<Box
							sx={{
								position: "absolute",
								top: 0,
								left: 0,
								width: "100%",
								height: "100%",
								backgroundColor: "rgba(0, 0, 0, 0.5)",
								display: "flex",
								alignItems: "center",
								justifyContent: "center",
								borderRadius: 2,
							}}
						>
							<CircularProgress color="inherit" />
						</Box>
					)}
				</Box>
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

const PromptBuilder = ({ selectedTemplate }) => {
  	const [selections, setSelections] = useState({});
  	const [inputText, setInputText] = useState('');

  	const [notification, setNotification] = useState({
    	open: false,
    	message: '',
    	severity: 'success', // 'success' | 'error' | 'warning' | 'info'
  	});

  	const [isLoading, setIsLoading] = useState(false);
  	const [currentImageUrl, setCurrentImageUrl] = useState(
    	selectedTemplate ? selectedTemplate.imageUrl : ''
  	);

  	const handleCloseNotification = (event, reason) => {
    	if (reason === 'clickaway') {
      		return;
    	}
    	setNotification({ ...notification, open: false });
  	};

  	const handleSubmit = async () => {
    	if (!selectedTemplate) {
      		setNotification({
        		open: true,
        		message: 'No template selected.',
        		severity: 'warning',
      		});
      		return;
    	}

		// This is where we set up the JSON that gets sent

    	const payload = {
      		keys: selections,
      		template: selectedTemplate.title,
      		input: inputText,
    	};

    	setIsLoading(true);

    	try {
      		const response = await fetch('/api/imagen', {
        		method: 'POST',
        		headers: {
          			'Content-Type': 'application/json',
        		},
        		body: JSON.stringify(payload),
      		});

    		if (!response.ok) {
        		const errorText = `API error: ${response.statusText}`;
        		setNotification({
          			open: true,
          			message: errorText,
          			severity: 'error',
        		});
			} else {
				const data = await response.json();
				if (data.imageUrl) {
					setCurrentImageUrl(data.newImageUrl);
					setNotification({
						open: true,
						message: 'Image updated successfully.',
						severity: 'success',
					});
					setSelections({});
					setInputText('');
				} else {
					setNotification({
						open: true,
						message: 'Unexpected API response.',
						severity: 'error',
					});
				}
			}
		} catch (error) {
    		const fetchError = `Fetch error: ${error.message}`;
      		setNotification({
        		open: true,
        		message: fetchError,
        		severity: 'error',
      		});
    	} finally {
      		setIsLoading(false);
    	}
	};

	// Use useEffect to watch for changes to selectedTemplate
  	useEffect(() => {
    	if (selectedTemplate) {
      		setCurrentImageUrl(selectedTemplate.imageUrl);
    	}
  	}, [selectedTemplate]);

  	return selectedTemplate ? (
    	<Box sx={{ padding: 2, backgroundColor: '#333' }}>
      		<Box sx={{
          		padding: 2,
          		border: '2px solid #000',
          		borderRadius: '6px',
          		backgroundColor: '#212121',
          		display: 'flex',
          		flexDirection: 'column',
          		minHeight: 'calc(100vh - 24px)',
        	}}>
				<PromptBuilderHeader
					selectedTemplate={selectedTemplate}
					currentImageUrl={currentImageUrl}
					isLoading={isLoading}
				/>
				<PromptBuilderOptionSelector
					selectedTemplate={selectedTemplate}
					selections={selections}
					setSelections={setSelections}
				/>
				<Box>
					<PromptBuilderComplexityBar percentage="70%" />
					<PromptBuilderInputBar
						selectedTemplate={selectedTemplate}
						inputText={inputText}
						setInputText={setInputText}
					/>
					<SubmitButton onClick={handleSubmit} />
				</Box>
			</Box>

			<Notification
				open={notification.open}
				onClose={handleCloseNotification}
				message={notification.message}
				severity={notification.severity}
			/>
		</Box>
	) : (
    	<Box sx={{ padding: 4, textAlign: 'center' }}>
      		<Typography variant="h6" color="textSecondary">
        		Please select a template to get started.
      		</Typography>
    	</Box>
  	);
};

export default PromptBuilder;
