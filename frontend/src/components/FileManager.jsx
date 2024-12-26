import { useState, useEffect } from 'react';
import axios from 'axios';
import LinkIcon from '@mui/icons-material/Link';

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

  if (loading) return <p>Loading files...</p>;

  return (
    <ul>
      {files.map(file => (
        <li key={file.name}>
        	{file.name} <a href={file.url} target="_blank" rel="noopener noreferrer">
        	<LinkIcon />
        </a>
      </li>
      ))}
    </ul>
  );
}

export default FileManager;
