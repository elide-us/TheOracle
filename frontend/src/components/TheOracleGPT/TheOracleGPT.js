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
        <div className="the-oracle-gpt">
            <CategoryList categories={data} onTileClick={handleTileClick} />
        </div>
    );
};

export default TheOracleGPT;