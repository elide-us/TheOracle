import React from "react";

const Tile = ({ label, onClick }) => {
  return (
    <div className="tile" onClick={onClick}>
      {label}
    </div>
  );
};

export default Tile;
