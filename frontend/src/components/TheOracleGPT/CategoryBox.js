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
              width: "200px",
              height: "130px",
              margin: "20px",
              border: "1px solid #ccc",
              borderRadius: "12px",
              cursor: "pointer",
              "&:hover": {
                backgroundColor: "#f0f0f0",
              },
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              innerWidth: "160px",
              innerHeight: "90px",
              textAlign: "center",
            }}
          >
          <Box sx={{
            bgcolor: 'background.paper',
            borderTop: '1px solid #ccc',
            borderBottom: '1px solid #ccc',
            position: 'relative',
            '&::before, &::after': { content: '""', position: 'absolute', top: 2, bottom: 0, width: '12px', background: 'linear-gradient(to right, background.paper 0%, transparent 100%)', zIndex: 1 },
            '&::before': { left: 0 },
            '&::after': { right: 0, transform: 'rotate(180deg)' } }}>{template.title}</Box>
            <Box
              component="img"
              src={template.imageUrl}
              alt={template.title}
              sx={{ width: "160px", height: "90px", objectFit: "cover" }}
            />
          </Box>
        ))}
      </Box>
    </div>
  );
};

export default CategoryBox;
