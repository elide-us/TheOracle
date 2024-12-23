import React from "react";

const PromptBuilder = ({ selectedTemplate }) => {
  return (
    <div className="prompt-builder">
      <h1>{selectedTemplate.title}</h1>
      <p>Here goes the template prompting system for {selectedTemplate.title}.</p>
      {selectedTemplate.imageUrl && (
        <img
          src={selectedTemplate.imageUrl}
          alt={`${selectedTemplate.title} preview`}
          style={{ maxWidth: "100%", borderRadius: "8px", marginTop: "10px" }}
        />
      )}
      {/* Add complexity bar, input bar, etc. */}
    </div>
  );
};

export default PromptBuilder;