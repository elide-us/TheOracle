import React from 'react';
import axios from 'axios';

const FileManager = () => {
  const [files, setFiles] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    axios.get('/api/files').then(response => {
      setFiles(response.data);
      setLoading(false);
    });
  }, []);

  if (loading) return <p>Loading files...</p>;

  return (
    <ul>
      {files.map(file => (
        <li key={file}>{file}</li>
      ))}
    </ul>
  );
}

export default FileManager;
