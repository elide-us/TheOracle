import React from 'react';
import { Drawer, Box, IconButton, Tooltip } from '@mui/material';
import { Menu as MenuIcon } from '@mui/icons-material';

function Sidebar({ open, setOpen }) {
    return (
        <Drawer variant='permanent' open={open}
            sx={{ width: open ? 240 : 40, position: 'fixed', zIndex: 1300, transition: 'width 0.3s', }}>
            <Box style={{ padding: '12px' }}>
                <Tooltip title="Toggle Menu">
                    <IconButton onClick={() => setOpen(!open)}>
                        <MenuIcon />
                    </IconButton>
                </Tooltip>
            </Box>
        </Drawer>
    );
}

export default Sidebar;