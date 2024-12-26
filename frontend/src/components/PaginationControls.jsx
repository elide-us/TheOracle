import { IconButton, Select, MenuItem, FormControl, Box, Typography } from '@mui/material';
import { NavigateNext, NavigateBefore } from '@mui/icons-material';

function PaginationControls(page, setPage, totalPages, itemsPerPage, setItemsPerPage) {
    return (
        <Box sx={{ 
            position: 'fixed',
            bottom: 0,
            left: 0,
            right: 0,
            height: '40px',
            backgroundColor: 'background.paper',
            borderTop: '1px solid #ccc',
            display: 'flex',
            alignItems: 'center',
            px: 2,
            zIndex: 1200
        }}>
            <Box sx={{ flex: 1, display: 'flex', justifyContent: 'center', gap: 1 }}>
                <IconButton 
                    onClick={() => setPage(p => Math.max(0, p - 1))}
                    disabled={page === 0}
                    size="small"
                >
                    <NavigateBefore fontSize="small" />
                </IconButton>
                <Typography>Page {page + 1} of {Math.max(1, totalPages)}</Typography>
                <IconButton 
                    onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))}
                    disabled={page >= totalPages - 1}
                    size="small"
                >
                    <NavigateNext fontSize="small" />
                </IconButton>
            </Box>

            <FormControl size="small" sx={{ '& .MuiSelect-select': { py: 0 } }}>
                <Select value={itemsPerPage} sx={{ height: '24px' }}
                    onChange={(e) => {
                        setItemsPerPage(e.target.value);
                        setPage(0); // Reset to first page when changing items per page
                    }}
                >
                    {[5, 10, 20, 50, 100].map((value) => (
                        <MenuItem key={value} value={value}>
                            {value} per page
                        </MenuItem>
                    ))}
                </Select>
            </FormControl>
        </Box>
    );
};

export default PaginationControls;