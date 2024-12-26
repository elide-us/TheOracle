import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link as LinkIcon } from '@mui/icons-material';
import { List, ListItem, Typography } from '@mui/material';

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
		});
	}, []);

	if (loading) return <Typography variant='p'>Loading files...</Typography>;

	return (
		<List>
			{files.map(file => (
				<ListItem key={file.name}>
					<Typography variant='p'>{file.name}</Typography> <a href={file.url} target="_blank" rel="noopener noreferrer"><LinkIcon /></a>
				</ListItem>
			))}
		</List>
	);
}

export default FileManager;
