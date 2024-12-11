import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { Link } from 'react-router-dom';
import { Drawer, List, ListItem, ListItemText, IconButton, Tooltip } from '@mui/material';
import { Login as LoginIcon, Menu as MenuIcon } from '@mui/icons-material';

import DarkTheme from '../../config/darktheme';
import routes from '../../config/routes';

const Sidebar = ({ open, setOpen }) => {
  return (
    <ThemeProvider theme={ DarkTheme }>
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
          {routes.map((route, index) => (
            <ListItem button component={Link} to={route.path} key={index}>
              {open ? (
                <>
                  <route.icon fontSize="small" />
                  <ListItemText primary={route.name} style={{ marginLeft: '8px' }} /> {/* Added margin */}
                </>
              ) : (
                <Tooltip title={route.name}>
                  <route.icon fontSize="small" />
                </Tooltip>
              )}
            </ListItem>
          ))}
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

export default Sidebar;