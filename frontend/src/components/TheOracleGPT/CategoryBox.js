import React from "react";
import Box from "@mui/material/Box";
import './index.css'

const CategoryBox = ({ categoryName, templates, onTileClick }) => {
  return (
    <div className="category-box">
      <div className="category-title">{categoryName}</div>
      <Box className="category-inner-box" sx={{
        display: 'grid',
        gap: '10px', // Spacing between tiles
        justifyContent: 'start',
        gridTemplateColumns: '1fr', // Default: single column
        '@media (min-width: 600px)': {
          gridTemplateColumns: 'repeat(2, 1fr)', // 2 columns for small screens (600px+)
        },
        '@media (min-width: 960px)': {
          gridTemplateColumns: 'repeat(3, 1fr)', // 3 columns for medium screens (960px+)
        },
        width: '100%',
        maxWidth: '600px', // Ensures the grid container doesn't exceed calculated width
        margin: '0 auto', // Centers the container

      }}>
        {templates.map((template) => (
          <Box
            key={template.title}
            className="tile"
            onClick={() => onTileClick(template.title)}
            sx={{
              padding: 2,
              textAlign: "center",
              border: "1px solid #ccc",
              borderRadius: "8px",
              cursor: "pointer",
              "&:hover": {
                backgroundColor: "#f0f0f0",
              },
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Box
              component="img"
              src={template.imageUrl}
              alt={template.title}
              sx={{
                width: "160px",
                height: "90px",
                marginBottom: "12px",
                borderRadius: "8px",
                objectFit: "cover",
              }}
            />
            {template.title}
          </Box>
        ))}
      </Box>
    </div>
  );
};

export default CategoryBox;
