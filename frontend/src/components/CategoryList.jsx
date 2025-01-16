import { Box, Tooltip, Typography } from "@mui/material";
import { PageTitle } from './shared/PageTitle';

const Tile = ({ template, onTileClick }) => {
	return (
		<Box
			key={template.title}
			className="tile"
			onClick={() => onTileClick(template)}
			sx={{
				border: '1px solid #ccc',
				borderRadius: 2,
				padding: 2,
				cursor: 'pointer',
				transition: 'transform 0.2s, box-shadow 0.2s, background-color 0.2s',
				backgroundColor: '#000', // Default background
				'&:hover': {
					transform: 'scale(1.03)', // Slightly enlarge on hover
					boxShadow: 3, // Elevation shadow on hover
					backgroundColor: '#1e1e1e', // Light gray background on hover
				},
			}}
		>
            <Tooltip title={template.description}>
                <Typography variant="subtitle1">{template.title}</Typography>
                <Box
                    component="img"
                    src={template.imageUrl}
                    alt={template.title}
                    sx={{ width: '100%', height: 'auto', marginTop: 1 }}
                />
            </Tooltip>
		</Box>
	);
};

const TileGrid = ({ templates, onTileClick }) => {
	return (
		<Box
			sx={{
				display: 'grid',
				gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))',
				gap: 2,
				marginTop: 2,
				border: '1px solid #CCC',
				padding: '12px',
				background: '#000',
			}}
		>
			{templates.map((template, index) => (
			<Tile
				key={index}
				template={template}
				onTileClick={onTileClick}
			/>
			))}
		</Box>
	);
};

const CategoryBox = ({ categoryName, templates, onTileClick }) => {
	return (
		<Box sx={{
			marginBottom: 4,
			marginLeft: 4,
			marginRight: 4,
			border: '1px solid #ccc',
			borderRadius:'12px',
			padding:'12px',
			background: '#333',
		}}>
			<Typography variant="h6" gutterBottom>
				{categoryName}
			</Typography>
			<TileGrid templates={templates} onTileClick={onTileClick} />
		</Box>
	);
};

const CategoryList = ({ categories, onTileClick }) => {
	return (
		<Box>
            <PageTitle title='Template Selector' />
			{Object.entries(categories).map(([categoryName, templates]) => (
				<CategoryBox
					key={categoryName}
					categoryName={categoryName}
					templates={templates}
					onTileClick={onTileClick}
				/>
			))}
		</Box>
	);
};

export default CategoryList;