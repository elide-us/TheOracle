import { Box, Select, MenuItem } from '@mui/material';

const LayerBox = ({ parts, data, selections, setSelections }) => {
	const groupedParts = [];
	let tempGroup = [];

	parts.forEach((part, index) => {
		tempGroup.push({ ...part, key: index });
		if (part.type === 'dropdown') {
			groupedParts.push([...tempGroup]);
			tempGroup = [];
		}
	});

	if (tempGroup.length > 0) {
		groupedParts.push([...tempGroup]);
	}

	return (
		<Box display="flex" flexWrap="wrap" gap={2}>
			{groupedParts.map((group, groupIndex) => (
				<Box key={`group-${groupIndex}`} display="flex" alignItems="center">
					{group.map((part) => {
						if (part.type === 'text') {
							return (
								<span key={`text-${part.key}`} style={{ marginRight: '8px' }}>
									{part.text}
								</span>
							);
						} else if (part.type === 'dropdown') {
							const options = data[part.placeholder] || {};

							return (
								<Select
									key={`select-${part.key}`}
									size='small'
									sx={{ minWidth: 120 }}
									displayEmpty
									autoWidth
									value={selections[part.placeholder] || ''}
									onChange={(e) => {
										const value = e.target.value;
										setSelections((prev) => {
											const updated = { ...prev };
											if (value === "") {
												delete updated[part.placeholder];
											} else {
												updated[part.placeholder] = value;
											}
											return updated;
										});
									}}							
								>
									<MenuItem value="">Select {part.placeholder}</MenuItem>
									{Object.keys(options).map((key) => (
										<MenuItem key={key} value={key}>{key}</MenuItem>
									))}
								</Select>
							);
						}
						return null;
					})}
				</Box>
			))}
		</Box>
	);
};

export default LayerBox;