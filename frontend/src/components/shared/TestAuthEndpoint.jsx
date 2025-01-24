import { useContext } from 'react';
import UserContext from './UserContextProvider';

const TestAuthEndpoint = () => {
  const { token } = useContext(UserContext);

  const handleTestAuth = async () => {
    try {
      const response = await fetch('/api/auth/test', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
  
      if (!response.ok) {
        throw new Error(`API Response failure: ${response.statusText}`);
      }
  
      const data = await response.json();
  
      // Log the response for debugging
      console.log(`Success! Response: ${JSON.stringify(data)}`);
      alert(`Success! Credits: ${data.credits}`);
    } catch (error) {
      console.error('Error testing auth endpoint:', error);
      alert(`Error: ${error.message || 'Unable to test auth endpoint'}`);
    }
  };

  return (
    <button onClick={handleTestAuth} style={{ padding: '10px 20px', cursor: 'pointer' }}>
      Test Auth Endpoint
    </button>
  );
};

export default TestAuthEndpoint;
