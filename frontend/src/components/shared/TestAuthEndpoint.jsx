import { useContext } from 'react';
import axios from 'axios';
import UserContext from './UserContextProvider';

const TestAuthEndpoint = () => {
  const { token } = useContext(UserContext);

  const handleTestAuth = async () => {
    try {
      const response = await axios.get('/auth/test', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      alert(`Success! Response: ${JSON.stringify(response.data)}`);
    } catch (error) {
      console.error('Error testing auth endpoint:', error);
      alert(`Error: ${error.response?.data?.detail || 'Unable to test auth endpoint'}`);
    }
  };

  return (
    <button onClick={handleTestAuth} style={{ padding: '10px 20px', cursor: 'pointer' }}>
      Test Auth Endpoint
    </button>
  );
};

export default TestAuthEndpoint;
