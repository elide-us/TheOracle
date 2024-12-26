import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link as LinkIcon } from '@mui/icons-material';
import { List, ListItem, Typography, Link } from '@mui/material';

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
				<ListItem key={file.name} sx={{ padding: '12px', }}>
					<Typography variant='p'>{file.name}</Typography> <Link href={file.url} target="_blank" rel="noopener noreferrer"><LinkIcon /></Link>
				</ListItem>
			))}
		</List>
	);
}

export default FileManager;
