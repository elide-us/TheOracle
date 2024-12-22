import React, { useState } from 'react';
import CategoryList from "./CategoryList";
import PromptBuilder from "./PromptBuilder";
import data from "./templates.json";
import './index.css'

const TheOracleGPT = () => {
    const [selectedTemplate, setSelectedTemplate] = useState(null);
    const handleTileClick = (template) => {
        setSelectedTemplate(template);
    };

    if (selectedTemplate) {
        return <PromptBuilder selectedTemplate={selectedTemplate} />;
    }

    return (
        <div style={{
            display: 'flex', 
            flexDirection: 'column', 
            width: '100%' }}>
            <div style={{
                position: 'fixed',
                left: 0,
                top: 0,
                bottom: 0,
                width: '30px',
                backgroundColor: 'transparent'
            }} />
            <div className="the-oracle-gpt">
                <CategoryList categories={data} onTileClick={handleTileClick} />
            </div>
        </div>
    );
};

export default TheOracleGPT;