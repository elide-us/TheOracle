import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link as LinkIcon } from '@mui/icons-material';
import { List, ListItem, Typography, Link, Box } from '@mui/material';
import PaginationControls from './PaginationControls';

function FileManager() {
	const [page, setPage] = useState(0);
    const [itemsPerPage, setItemsPerPage] = useState(10);
	const [files, setFiles] = useState([]);
	const [loading, setLoading] = useState(true);


	const totalPages = Math.ceil(files.length / itemsPerPage);
    const paginatedFiles = files.slice(page * itemsPerPage, (page + 1) * itemsPerPage);

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
		<Box>
			<List>
				{paginatedFiles.map((file, index) => (
					<ListItem key={index} sx={{ padding: '12px', }}>
						<Typography variant='p'>{file.name}</Typography>
						<Box sx={{
							marginLeft: '10px',
							padding: '5px 8px 0 8px',
							border: '1px solid #ccc',
							borderRadius: '5px',
						}}>
							<Link href={file.url} target="_blank" rel="noopener noreferrer"><LinkIcon /></Link>
						</Box>
					</ListItem>
				))}
			</List>
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

export default FileManager;
