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
              position: "relative",
              padding: "24px", // Space around the image
              border: "1px solid #ccc",
              borderRadius: "8px",
              cursor: "pointer",
              overflow: "hidden",
              "&:hover": {
                backgroundColor: "#f0f0f0",
              },
            }}
          >
            {/* Image filling the entire tile, with no rounded corners */}
            <Box
              component="img"
              src={template.imageUrl}
              alt={template.title}
              sx={{
                position: "absolute",
                top: "24px",
                left: "24px",
                right: "24px",
                bottom: "24px",
                width: "calc(100% - 48px)", // Ensures the 24px margin
                height: "calc(100% - 48px)",
                objectFit: "cover",
                borderRadius: "0", // No rounded corners
              }}
            />

            {/* Overlayed text with a banner box */}
            <Box
              sx={{
                position: "absolute",
                bottom: "24px",
                left: "24px",
                right: "24px",
                background: "linear-gradient(to right, rgba(204, 204, 204, 0) 0%, #fff 12px, #fff calc(100% - 12px), rgba(204, 204, 204, 0) 100%)",
                borderTop: "1px solid #ccc",
                borderBottom: "1px solid #ccc",
                textAlign: "center",
                padding: "4px 0",
              }}
            >
              {template.title}
            </Box>
          </Box>
        ))}
      </Box>
    </div>
  );
};

export default CategoryBox;
