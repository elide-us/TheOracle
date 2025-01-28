import { useState, useEffect } from 'react';
import { Box, Typography } from '@mui/material';
import LayerBox from './LayerBox'

const OptionSelector = ({ selectedTemplate, selections, setSelections }) => {
    const [dataLayer1, setDataLayer1] = useState({})
    const [dataLayer2, setDataLayer2] = useState({})
    const [dataLayer3, setDataLayer3] = useState({})
    const [dataLayer4, setDataLayer4] = useState({})

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

	useEffect(() => {
		fetch('/api/imagen/1')
			.then((res) => res.json())
			.then((layerData) => setDataLayer1(layerData))
			.catch(console.error);
		fetch('/api/imagen/2')
			.then((res) => res.json())
			.then((layerData) => setDataLayer2(layerData))
			.catch(console.error);
		fetch('/api/imagen/3')
			.then((res) => res.json())
			.then((layerData) => setDataLayer3(layerData))
			.catch(console.error);
		fetch('/api/imagen/4')
			.then((res) => res.json())
			.then((layerData) => setDataLayer4(layerData))
			.catch(console.error);
	}, []);
  
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

export default OptionSelector;