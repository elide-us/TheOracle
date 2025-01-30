import axios from 'axios';
import { useState, useEffect, useContext } from 'react';
import { Box, Typography } from '@mui/material';
import UserContext from "./shared/UserContextProvider";
import { PageTitle } from './shared/PageTitle';
import Notification from './shared/Notification';
import SubmitButton from './promptbuilder/SubmitButton'
import OptionSelector from './promptbuilder/OptionSelector'
import Header from './promptbuilder/Header'
import InputBar from './promptbuilder/InputBar'
import ComplexityBar from './promptbuilder/ComplexityBar'

const PromptBuilder = ({ selectedTemplate }) => {
  	const [selections, setSelections] = useState({});
  	const [inputText, setInputText] = useState('');
  	const [isLoading, setIsLoading] = useState(false);
	const { userData, setUserData } = useContext(UserContext);

  	const [currentImageUrl, setCurrentImageUrl] = useState(
		selectedTemplate ? selectedTemplate.imageUrl : ''
	);

  	const [notification, setNotification] = useState({
		open: false,
		message: '',
		severity: 'success', // 'success' | 'error' | 'warning' | 'info'
	});


  	const handleCloseNotification = (event, reason) => {
    	if (reason === 'clickaway') {
      		return;
    	}
    	setNotification({ ...notification, open: false });
  	};

  	const handleSubmit = async () => {
    	if (!selectedTemplate) {
      		setNotification({
        		open: true,
        		message: 'No template selected.',
        		severity: 'warning',
      		});
      		return;
    	}

    	const payload = {
      		keys: selections,
      		template: selectedTemplate.title,
      		userinput: inputText,
    	};

    	setIsLoading(true);

		try {
			const response = await axios.post('/api/imagen', payload, {
				headers: {
					Authorization: `Bearer ${userData.token}`,
					'Content-Type': 'application/json',
				},
			});

			if (response.data.imageUrl) {
				setCurrentImageUrl(response.data.imageUrl);
				setNotification({
					open: true,
					message: 'Image updated successfully.',
					severity: 'success',
				});
				setSelections({});
				setInputText('');
			}
			
			if (response.data.credits !== undefined) {
				setUserData((prevUserData) => ({
					...prevUserData,
					credits: response.data.credits,
				}));
			}

		} catch (error) {
			const axiosError = `Axios error: ${error.message}`;
			setNotification({
				open: true,
				message: axiosError,
				severity: 'error',
			});
		} finally {
			setIsLoading(false);
		}

		// try {
      	// 	const response = await fetch('/api/imagen', {
        // 		method: 'POST',
        // 		headers: {
        //   			'Content-Type': 'application/json',
        // 		},
        // 		body: JSON.stringify(payload),
      	// 	});

    	// 	if (!response.ok) {
        // 		const errorText = `API error: ${response.statusText}`;
        // 		setNotification({
        //   			open: true,
        //   			message: errorText,
        //   			severity: 'error',
        // 		});
		// 	} else {
		// 		const data = await response.json();
		// 		if (data.error) {
		// 			setNotification({
		// 				open: true,
		// 				message: `Server error: ${data.error}`,
		// 				severity: 'error',
		// 			});
		// 		} else if (data.imageUrl) {
		// 			setCurrentImageUrl(data.imageUrl);
		// 			setNotification({
		// 				open: true,
		// 				message: 'Image updated successfully.',
		// 				severity: 'success',
		// 			});
		// 			setSelections({});
		// 			setInputText('');
		// 		} else {
		// 			setNotification({
		// 				open: true,
		// 				message: 'Unexpected API response.',
		// 				severity: 'error',
		// 			});
		// 		}
		// 	}
		// } catch (error) {
    	// 	const fetchError = `Fetch error: ${error.message}`;
      	// 	setNotification({
        // 		open: true,
        // 		message: fetchError,
        // 		severity: 'error',
      	// 	});
    	// } finally {
      	// 	setIsLoading(false);
    	// }
	};

  	useEffect(() => {
    	if (selectedTemplate) {
      		setCurrentImageUrl(selectedTemplate.imageUrl);
    	}
  	}, [selectedTemplate]);

  	return selectedTemplate ? (
		<Box>
			<PageTitle title='Prompt Builder' />
			<Box sx={{ padding: 2, backgroundColor: '#333' }}>
				<Box sx={{
					padding: 2,
					border: '2px solid #000',
					borderRadius: '6px',
					backgroundColor: '#212121',
					display: 'flex',
					flexDirection: 'column',
					minHeight: 'calc(100vh - 24px)',
				}}>
					<Header
						selectedTemplate={selectedTemplate}
						currentImageUrl={currentImageUrl}
						isLoading={isLoading}
					/>
					<OptionSelector
						selectedTemplate={selectedTemplate}
						selections={selections}
						setSelections={setSelections}
					/>
					<Box>
						<ComplexityBar percentage="70%" />
						<InputBar
							selectedTemplate={selectedTemplate}
							inputText={inputText}
							setInputText={setInputText}
						/>
						<SubmitButton onClick={handleSubmit} disabled={isLoading}/>
					</Box>
				</Box>

				<Notification
					open={notification.open}
					onClose={handleCloseNotification}
					message={notification.message}
					severity={notification.severity}
				/>
			</Box>
		</Box>

	) : (
		<Box>
			<PageTitle title='Prompt Builder' />
			<Box sx={{ padding: 4, textAlign: 'center' }}>
				<Typography variant="h6" color="textSecondary">
					Please select a template to get started.
				</Typography>
			</Box>
		</Box>
  	);
};

export default PromptBuilder;
