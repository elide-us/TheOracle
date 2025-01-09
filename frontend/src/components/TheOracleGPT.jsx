import { useState, useEffect } from 'react';
import { Box } from "@mui/material";
import PromptBuilder from './PromptBuilder';
import CategoryList from './CategoryList';

function TheOracleGPT() {
    const [selectedTemplate, setSelectedTemplate] = useState(null);
    const [templates, setTemplates] = useState([]);

    const handleTileClick = (template) => {
        setSelectedTemplate(template);
    }

    useEffect(() => {
        fetch('/api/imagen/0')
            .then(res => res.json())
            .then(setTemplates)
            .catch(console.error)
    }, []);

    return (
        <Box>
            {selectedTemplate ? (
                <PromptBuilder selectedTemplate={selectedTemplate} />
            ) : (
                <CategoryList categories={templates} onTileClick={handleTileClick} />
            )}
        </Box>
    );
}

export default TheOracleGPT;
