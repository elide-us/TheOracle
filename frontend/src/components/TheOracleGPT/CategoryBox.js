import React from "react";

const CategoryBox = ({ categoryName, templates, onTileClick }) => {
  return (
    <div className="category-box">
      <h2>{categoryName}</h2>
      <div className="tile-row">
        {templates.map((template) => (
          <div
            key={template}
            className="tile"
            onClick={() => onTileClick(template)}
          >
            {template}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CategoryBox;
