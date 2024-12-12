import React from 'react';
import { IconButton, Tooltip } from '@mui/material';
import { FileCopy as FileCopyIcon } from '@mui/icons-material';
import axios from 'axios';

const Gallery = () => {
  const [images, setImages] = React.useState([]);
  const [loading, setLoading] = React.useState(true)

  const copyToClipboard = (url) => {
    navigator.clipboard.writeText(url).then(() => {
      alert('URL copied to clipboard!');
    }).catch(err => {
      console.error('Failed to copy: ', err);
    });
  };

  React.useEffect(() => {
    axios.get('/api/files').then(response => {
      if (response.data && Array.isArray(response.data.files)) {
        setImages(response.data.files);
      } else {
        console.error('Expected an array but got:', response.data);
        setImages([]);
      }
      setLoading(false);
    }).catch(error => {
      console.error('Error fetching files:', error);
      setLoading(false);
    });
  }, []);

  if (loading) return <p>Loading files...</p>

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {images.map((image, index) => (
        <div key={index} style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{ flex: '0 0 19%', aspectRatio: '19 / 6', overflow: 'hidden' }}>
            <img src={image.url} alt={image.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          </div>
          <div style={{ flex: '1', paddingLeft: '16px', display: 'flex', alignItems: 'center' }}>
            <span style={{ flex: '1' }}>{image.name}</span>
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