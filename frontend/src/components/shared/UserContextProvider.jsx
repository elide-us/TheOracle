import { createContext, useState } from 'react';

// Initialize context with default values to avoid destructuring errors
const UserContext = createContext({
    user: null,          // Default user value
    logIn: () => {},     // No-op function
    logOut: () => {},    // No-op function
});

export const UserContextProvider = ({ children }) => {
    const [user, setUser] = useState(null); // State to hold user data

    // Function to log in the user and set their data
    const logIn = (userData) => {
        setUser({
            profileUrl: userData.profileUrl,
            username: userData.username,
            token: userData.token, // Bearer token
        });
    };

    // Function to log out the user and clear their data
    const logOut = () => {
        setUser(null);
    };

    // Provide the context value to child components
    return (
        <UserContext.Provider value={{ user, logIn, logOut }}>
            {children}
        </UserContext.Provider>
    );
};

export default UserContext;
