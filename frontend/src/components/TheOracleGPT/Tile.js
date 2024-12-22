import React from "react";
import './index.css'

const Tile = ({ label, onClick }) => {
  return (
    <div className="tile" onClick={onClick}>
      {label}
    </div>
  );
};

export default Tile;


