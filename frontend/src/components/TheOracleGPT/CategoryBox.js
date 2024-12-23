import React from "react";
import Box from "@mui/material/Box";
import './index.css'

const CategoryBox = ({ categoryName, templates, onTileClick }) => {
  return (
    <div className="category-box">
      <div className="category-title">{categoryName}</div>
      <Box className="category-inner-box" sx={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))",
        gap: 2,
      }}>
        {templates.map((template) => (
          <Box
            key={template}
            className="tile"
            onClick={() => onTileClick(template)}
            sx={{
              padding: 2,
              textAlign: "center",
              border: "1px solid #ccc",
              borderRadius: "8px",
              cursor: "pointer",
              "&:hover": {
                backgroundColor: "#f0f0f0f",
              }
            }}
          > 
            {template}
          </Box>
        ))}
      </Box>
    </div>
  );
};

export default CategoryBox;
