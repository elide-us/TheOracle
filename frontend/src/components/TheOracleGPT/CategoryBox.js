import React from "react";
import './index.css'

const CategoryBox = ({ categoryName, templates, onTileClick }) => {
  return (
    <div className="category-box">
      <div className="category-title">{categoryName}</div>
      <div className="category-inner-box">
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
