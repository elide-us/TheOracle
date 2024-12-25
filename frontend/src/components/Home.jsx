import React from 'react';
import { Box, Typography, Link, CardMedia } from '@mui/material';
import Links from '../config/links';
import Logo from '../assets/elideus_group_green.png'

function Home() {
	return (
		<Box sx={{
			display: 'flex', flexDirection: 'column',
			alignItems: 'center', justifyContent: 'flex-start', 
			height: '100vh', backgroundColor: '#000',
			paddingTop: '20px'
		}}>
			<CardMedia
				component='img'
				alt='Elideus Group Image' 
				image={Logo}
				sx={{
					maxWidth: '60%',
					marginBottom: '50px',
				}}
			/>
			<Typography variant='p'>AI Engineering and Consulting Services</Typography>
			<Box sx={{ marginTop: '20px', width: '300px', textAlign: 'center' }}>
				{Links.map(link => (
					<Link
						key={link.title}
						href={link.url}
						title={link.title}
						underline='none'
						color='#fff'
						backgroundColor='#111'
						target='_blank'
						rel='noopener noreferrer'
						sx={{
							display: 'block',
							padding: '12px',
							margin: '10px 0',
							borderRadius: '5px',
							transition: 'background 0.3s',
						}}
						onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#222'}
						onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#111'}
					>
						{link.title}
					</Link>
				))}
			</Box>
			<Typography variant='p' sx={{ marginTop: '20px' }}>
				Contact us at: <Link underline='hover' color='#fff' href='mailto:contact@elideusgroup.com'>contact@elideusgroup.com</Link> 
			</Typography>
		</Box>
	)
}

export default Home;
