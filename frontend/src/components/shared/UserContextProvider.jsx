import { createContext, useState } from 'react';

// Initialize context with default values to avoid destructuring errors
const UserContext = createContext({
    userData: null,          // Default user value
    setUserData: () => {},     // No-op function
    clearUserData: () => {},    // No-op function
});

export const UserContextProvider = ({ children }) => {
    const [userData, setUserData] = useState(null);

    const clearUserData = () => {
        setUserData(null);
    };

    return (
        <UserContext.Provider value={{ userData, setUserData, clearUserData }}>
            {children}
        </UserContext.Provider>
    );
};

export default UserContext;
