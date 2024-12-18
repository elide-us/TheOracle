import React from 'react';
import { IconButton, Tooltip, Select, MenuItem, FormControl, Box, Typography } from '@mui/material';
import { FileCopy as FileCopyIcon, NavigateNext, NavigateBefore } from '@mui/icons-material';
import axios from 'axios';

const Gallery = () => {
  const [page, setPage] = React.useState(0);
  const [itemsPerPage, setItemsPerPage] = React.useState(10);
  const [images, setImages] = React.useState([]);
  const [loading, setLoading] = React.useState(true)

  const totalPages = Math.ceil(images.length / itemsPerPage);
  const paginatedImages = images.slice(page * itemsPerPage, (page + 1) * itemsPerPage);

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
    <div style={{
      display: 'flex', 
      flexDirection: 'column', 
      width: '100%', }}>
      <div style={{
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
        width: '30px',
        backgroundColor: 'transparent', // Or any color you prefer
      }}></div>
      {paginatedImages.map((image, index) => (
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


      <Box sx={{ 
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        height: '30px',
        backgroundColor: 'background.paper',
        borderTop: '1px solid #ddd',
        display: 'flex', 
        justifyContent: 'center',
        alignItems: 'center',
        px: 2,
        zIndex: 1200
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <IconButton 
            onClick={() => setPage(p => Math.max(0, p - 1))}
            disabled={page === 0}
            size="small"
          >
            <NavigateBefore fontSize="small" />
          </IconButton>
          
          <Typography>
            Page {page + 1} of {Math.max(1, totalPages)}
          </Typography>

          <IconButton 
            onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))}
            disabled={page >= totalPages - 1}
            size="small"
          >
            <NavigateNext fontSize="small" />
          </IconButton>
        </Box>

        <FormControl size="small" sx={{ position: 'absolute', right: '16px', '& .MuiSelect-select': { py: 0 } }}>
          <Select
            value={itemsPerPage}
            onChange={(e) => {
              setItemsPerPage(e.target.value);
              setPage(0); // Reset to first page when changing items per page
            }}
            sx={{ height: '24px' }}
          >
            {[5, 10, 20, 50, 100].map((value) => (
              <MenuItem key={value} value={value}>
                {value} per page
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
    </div>
  );
};

export default Gallery;