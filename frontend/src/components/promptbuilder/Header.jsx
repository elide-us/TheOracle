import { Box, Typography, CircularProgress } from '@mui/material';

const Header = ({ selectedTemplate, currentImageUrl, isLoading }) => {
	return (
		<Box>
			<Typography variant="h4" component="h1" gutterBottom>
				{selectedTemplate.title}
			</Typography>
			<Typography variant="body1" gutterBottom>
				{selectedTemplate.description}
			</Typography>
			{currentImageUrl && (
				<Box sx={{ position: "relative", marginTop: 2, width: "100%", maxWidth: "600px" }}>
					<Box
						component="img"
						src={currentImageUrl}
						alt={`${selectedTemplate.title} preview`}
						sx={{
							width: "100%",
							maxWidth: "600px",
							borderRadius: 2,
							display: "block",
						}}
					/>
					{isLoading && (
						<Box
							sx={{
								position: "absolute",
								top: 0,
								left: 0,
								width: "100%",
								height: "100%",
								backgroundColor: "rgba(0, 0, 0, 0.5)",
								display: "flex",
								alignItems: "center",
								justifyContent: "center",
								borderRadius: 2,
							}}
						>
							<CircularProgress color="inherit" />
						</Box>
					)}
				</Box>
			)}
		</Box>
	);
};

export default Header;