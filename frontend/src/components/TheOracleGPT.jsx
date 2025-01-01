import { useState } from 'react';
import { Box } from "@mui/material";
import templates from './templates.json';
import PromptBuilder from './PromptBuilder';
import CategoryList from './CategoryList';

function TheOracleGPT() {
    const [selectedTemplate, setSelectedTemplate] = useState(null);
    
    const handleTileClick = (template) => {
        setSelectedTemplate(template);
    }

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
