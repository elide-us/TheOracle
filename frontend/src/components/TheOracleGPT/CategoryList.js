import React from "react";
import CategoryBox from "./CategoryBox";
import './index.css'

const CategoryList = ({ categories, onTileClick }) => {
  return (
    <div className="category-list">
      {Object.entries(categories).map(([categoryName, templates]) => (
        <CategoryBox
          key={categoryName}
          categoryName={categoryName}
          templates={templates}
          onTileClick={onTileClick}
        />
      ))}
    </div>
  );
};

export default CategoryList;
