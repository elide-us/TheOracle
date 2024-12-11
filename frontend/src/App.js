import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { Drawer, List, ListItem, ListItemText, IconButton, Tooltip } from '@mui/material';
import { Home as HomeIcon, Folder as FolderIcon, Login as LoginIcon, Menu as MenuIcon } from '@mui/icons-material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import './App.css';
import logo from './assets/elideus_group_green.png';
import links from './links';
import axios from 'axios';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#90caf9' },
    secondary: { main: '#f48fb1' },
  },
  components: {
    MuiIconButton: {
      styleOverrides: {
        root: {
          color: 'lightgrey',
          '&:hover': {
            color: 'white',
          },
        },
      },
    },
    MuiListItem: {
      styleOverrides: {
        root: {
          '&.MuiListItem-root': {
            color: 'lightgrey !important',
            textDecoration: 'none',
            '&:hover': {
              color: 'white !important',
              '& .MuiSvgIcon-root': {
                color: 'white !important',
              },
              '& .MuiListItemText-root': {
                color: 'white !important',
              },
            },
            '& .MuiSvgIcon-root': {
              color: 'lightgrey !important',
            },
            '& .MuiListItemText-root': {
              color: 'lightgrey !important',
              '& .MuiTypography-root': {
                color: 'lightgrey !important',
              },
            },
          },
        },
      },
    },
  }
});

function Sidebar({ open, setOpen }) {
  return (
    <ThemeProvider theme={darkTheme}>
      <Drawer variant="permanent" open={open}
        sx={{ width: open ? 240 : 30, position: 'fixed', zIndex: 1300, transition: 'width 0.3s', '&.MuiDrawer-paper': { width: open ? 240 : 30 } }}>
        <div style={{ display: 'flex', alignItems: 'center', padding: '8px' }}>
          <Tooltip title="Toggle Menu">
            <IconButton onClick={() => setOpen(!open)}>
              <MenuIcon />
            </IconButton>
          </Tooltip>
        </div>
        <List>
          <ListItem button component={Link} to="/">
            {open ? <HomeIcon fontSize="small" /> : <Tooltip title="Home"><HomeIcon fontSize="small" /></Tooltip>}
            {open && <ListItemText primary="Home" />}
          </ListItem>
          <ListItem button component={Link} to="/file-manager">
            {open ? <FolderIcon fontSize="small" /> : <Tooltip title="File Manager"><FolderIcon fontSize="small" /></Tooltip>}
            {open && <ListItemText primary="File Manager" />}
          </ListItem>
        </List>
        <div style={{ marginTop: 'auto', padding: '8px', display: 'flex', alignItems: 'center' }}>
          <Tooltip title="Login with Microsoft">
            <IconButton>
              <LoginIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          {open && <ListItemText primary="Login" style={{ marginLeft: '8px' }} />}
        </div>
      </Drawer>
    </ThemeProvider>
  );
}

function Home() {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      backgroundColor: '#000',
      color: '#fff'
    }}>
      <img src={logo} alt="Elideus Group" className="logo" style={{ width: '60%' }} />
      <p>AI Engineering and Consulting Services</p>
      <div style={{ marginTop: '20px', width: '300px', textAlign: 'center' }}>
        {links.map(link => (
          <a
            key={link.title}
            href={link.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              display: 'block',
              padding: '15px',
              margin: '10px 0',
              backgroundColor: '#111',
              color: '#fff',
              textDecoration: 'none',
              borderRadius: '5px',
              transition: 'background 0.3s'
            }}
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#222'}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#111'}
          >
            {link.title}
          </a>
        ))}
      </div>
      <p style={{ marginTop: '20px' }}>Contact us at: <a href="mailto:contact@elideusgroup.com" style={{ color: '#fff' }}>contact@elideusgroup.com</a></p>
    </div>
  );
}

function FileManager() {
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

function App() {
  const [open, setOpen] = React.useState(true);

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Router>
        <div style={{ display: 'flex' }}>
          <Sidebar open={open} setOpen={setOpen} />
          <div style={{ flexGrow: 1, padding: '16px' }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/file-manager" element={<FileManager />} />
            </Routes>
          </div>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
