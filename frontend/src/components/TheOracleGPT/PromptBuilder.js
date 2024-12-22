import React from "react";

const PromptBuilder = ({ selectedTemplate }) => {
  return (
    <div className="prompt-builder">
      <h1>{selectedTemplate}</h1>
      <p>Here goes the template prompting system for {selectedTemplate}.</p>
      {/* Add complexity bar, input bar, etc. */}
    </div>
  );
};

export default PromptBuilder;