import { Box, Typography } from '@mui/material';
import { useState, useEffect } from 'react';

const LayerEditor = ({layer}) => {
    const [selectedLayer, setSelectedLayer] = useState(layer);

    return (
        <Box sx={{ padding:1, border: '2px solid #ccc', borderRadius: 2, margin: 2, background: '#333'}}>
            <Box sx={{ margin: '1px' }}>
                <Typography variant='body1'>Layer {selectedLayer}</Typography>
            </Box>            
            <Box sx={{ padding: 1, border: '2px solid #000', borderRadius: 1, background: '#1e1e1e' }}>
                <Typography variant='h4'>Layer Editor</Typography>
                {/*
                    Load all the key values for the layer from the DB
                    Create a row component for each row from the DB
                    "Include" check box
                    "Fixed" check box
                    Public Key Description Text
                */}
            </Box>
        </Box>
    )
}

const CategorySelector = () => {
    return (
        <Box sx={{ padding:1, border: '1px solid #ccc', borderRadius: 2, marginLeft: 1 }}>
            <Typography variant='h4'>Category Selector</Typography>
            {/*  */}
        </Box>
    )
}

const TemplateSelector = () => {
    return (
        <Box sx={{ padding:1, border: '1px solid #ccc', borderRadius: 2, marginRight: 2 }}>
            <Typography variant='h4'>Template Selector</Typography>
            {/*  */}
        </Box>
    )
}

const UrlEditBox = () => {
    return (
        <Box sx={{ padding: 1, borderTop: '2px solid #ccc' }}>
            {/*
                This will need to have two options, a version that lets you select, 
                create new (from typed text, unique), or delete a field value.
                The other version needs to also be able to display the selected keys
                from the Layer Editor.
            */}
            <Typography variant='h6'>Image URL Edit Box</Typography>
        </Box>
    );
}

const TooltipEditBox = () => {
    return (
        <Box sx={{ padding: 1, borderTop: '2px solid #ccc' }}>
            {/*
                This will need to have two options, a version that lets you select, 
                create new (from typed text, unique), or delete a field value.
                The other version needs to also be able to display the selected keys
                from the Layer Editor.
            */}
            <Typography variant='h6'>Tooltip Edit Box</Typography>
        </Box>
    );
}

const PromptEditBox = () => {
    return (
        <Box sx={{ padding: 1, borderTop: '2px solid #ccc' }}>
            {/*
                This will need to have two options, a version that lets you select, 
                create new (from typed text, unique), or delete a field value.
                The other version needs to also be able to display the selected keys
                from the Layer Editor.
            */}
            <Typography variant='h6'>Private Prompt Edit Box</Typography> 
        </Box>
    );
}


const CategoryEditor = () => {
    const [selectedCategory, setSelectedCategory] = useState({});
    const [selectedTemplate, setSelectedTemplate] = useState({});

    return (
        <Box sx={{ width: '100%', padding: 1 }}> {/* Outer Abstract Box flex/stack... */}
            <Typography variant='h4'>Category Editor</Typography>
            <Box sx={{ display: 'flex' }}> {/* Top Abstract Box */}
                <Box sx={{ width: '50%', padding: 1 }}> {/* Top Left Box */}
                    <CategorySelector />
                </Box>
                <Box sx={{ width: '50%', padding: 1 }}> {/* Top Right Box */}
                    <TemplateSelector />
                </Box>
            </Box>
            <Box> {/* Abstract - Image URL & Tooltip Editable Field Component */}
                <Box sx={{ padding: 1 }}>
                    <UrlEditBox />
                </Box>
                <Box sx={{ padding: 1 }}>
                    <TooltipEditBox />
                </Box>
            </Box>
            <Box> {/* Layer Element Editor Component */}
                <LayerEditor layer='1: Foundation' />
            </Box>
            <Box> {/* Layer Element Editor Component */}
                <LayerEditor layer='2: Structural' />
            </Box>
            <Box> {/* Layer Element Editor Component */}
                <LayerEditor layer='3: Styling' />
            </Box>
            <Box> {/* Layer Element Editor Component */}
                <LayerEditor layer='4: Details' />
            </Box>
            <Box> {/* Private Prompt Edtior Box */}
                <PromptEditBox />        
            </Box>
        </Box>

    );
}

export default CategoryEditor;
