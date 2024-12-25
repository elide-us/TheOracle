import { useState, useEffect } from 'react';
import { Typography, List, ListItem, ListItemText, Link as LinkIcon } from '@mui/material';
import { Link } from 'react-router-dom';
import axios from 'axios';

function FileManager() {
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios.get('/api/files').then(response => {
            if (response.data && Array.isArray(response.data.files)) {
                setFiles(response.data.files);
            } else {
                setFiles([]);
            }
            setLoading(false);
        }).catch(error => {
            setLoading(false);
        });
    }, []);

    if (loading) return <Typography>Loading files...</Typography>;

    return (
        <List>
            {files.map(file => (
                <ListItem button component={Link} to={file.url} key={file.name}>
                    <ListItemText primary={file.name} />
                    <LinkIcon />
                </ListItem>
            ))}
        </List>
    );
}

export default FileManager;
