import React from 'react';
import axios from 'axios';
import LinkIcon from '@mui/icons-material/Link';

const FileManager = () => {
  const [files, setFiles] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    axios.get('/api/files').then(response => {
      if (response.data && Array.isArray(response.data.files)) {
        setFiles(response.data.files);
      } else {
        console.error('Expected an array but got:', response.data);
        setFiles([]);
      }
      setLoading(false);
    }).catch(error => {
      console.error('Error fetching files:', error);
      setLoading(false);
    });
  }, []);

  if (loading) return <p>Loading files...</p>;

  return (
    <ul>
      {files.map(file => (
        <li key={file.name}>
        {file.name} - <a href={file.url} target="_blank" rel="noopener noreferrer">
          <LinkIcon />
        </a>
      </li>
      ))}
    </ul>
  );
}

export default FileManager;
