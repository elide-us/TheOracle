import { useState, useEffect } from 'react';
import { IconButton, Tooltip, Box, Typography } from '@mui/material';
import { FileCopy as FileCopyIcon } from '@mui/icons-material';
import axios from 'axios';
import PaginationControls from './shared/PaginationControls';

function Gallery() {
    const [page, setPage] = useState(0);
    const [itemsPerPage, setItemsPerPage] = useState(10);
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(true);

    const totalPages = Math.ceil(images.length / itemsPerPage);
    const paginatedImages = images.slice(page * itemsPerPage, (page + 1) * itemsPerPage);

    const copyToClipboard = (url) => {
        navigator.clipboard.writeText(url).then(() => {
            alert('URL copied to clipboard!');
        });
    };

    useEffect(() => {
        axios.get('/api/files').then(response => {
            if (response.data && Array.isArray(response.data.files)) {
                setImages(response.data.files);
            } else {
                setImages([]);
            }
            setLoading(false);
        });
    }, []);

    if (loading) return <Typography variant='p'>Loading files...</Typography>;

    return (
        <Box>
            {paginatedImages.map((image, index) => (
                <Box key={index} style={{ display: 'flex', alignItems: 'center' }}>
                    <Box style={{ flex: '0 0 19%', aspectRatio: '19 / 6', overflow: 'hidden' }}>
                        <img src={image.url} alt={image.name} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                    </Box>
                    <Box style={{ flex: '1', paddingLeft: '16px', display: 'flex', alignItems: 'center' }}>
                        <span style={{ flex: '1' }}>{image.name}</span>
                        <Tooltip title="Copy URL">
                            <IconButton sx={{ marginRight: '16px' }} onClick={() => copyToClipboard(image.url)}>
                                <FileCopyIcon />
                            </IconButton>
                        </Tooltip>
                    </Box>
                </Box>
            ))}

            <PaginationControls
                page={page}
                setPage={setPage}
                totalPages={totalPages}
                itemsPerPage={itemsPerPage}
                setItemsPerPage={setItemsPerPage}
            />
        </Box>
    );
}

export default Gallery;
