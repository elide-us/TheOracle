import React from 'react';
import { IconButton, Tooltip } from '@mui/material';
import { FileCopy as FileCopyIcon } from '@mui/icons-material';

const images = [
  { filename: 'dove_key0.jpg', url: 'https://theoraclesa.blob.core.windows.net/lumaai/dove_key0.jpg' },
  { filename: 'dove_key1.jpg', url: 'https://theoraclesa.blob.core.windows.net/lumaai/dove_key1.jpg' },
  // Add more images as needed
];

const Gallery = () => {
  const copyToClipboard = (url) => {
    navigator.clipboard.writeText(url).then(() => {
      alert('URL copied to clipboard!');
    }).catch(err => {
      console.error('Failed to copy: ', err);
    });
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {images.map((image, index) => (
        <div key={index} style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{ flex: '0 0 19%', aspectRatio: '19 / 6', overflow: 'hidden' }}>
            <img src={image.url} alt={image.filename} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          </div>
          <div style={{ flex: '1', paddingLeft: '16px', display: 'flex', alignItems: 'center' }}>
            <span style={{ flex: '1' }}>{image.filename}</span>
            <Tooltip title="Copy URL">
              <IconButton onClick={() => copyToClipboard(image.url)}>
                <FileCopyIcon />
              </IconButton>
            </Tooltip>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Gallery;