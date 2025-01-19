import { createContext, useState } from 'react';

// Initialize context with default values to avoid destructuring errors
const UserContext = createContext({
    user: null,          // Default user value
    setUser: () => {},     // No-op function
    logoutUser: () => {},    // No-op function
});

export const UserContextProvider = ({ children }) => {
    const [user, setUser] = useState(null); // State to hold user data

    // Function to log in the user and set their data
    // const logIn = (userData) => {
    //     setUser({
    //         internalToken: userData.token, // Bearer token
    //         username: userData.username,
    //         email: userData.email,
    //         profilePicture: userData.profilePicture
    //     });
    // };

    // Function to log out the user and clear their data
    const logoutUser = () => {
        setUser(null);
    };

    // Provide the context value to child components
    return (
        <UserContext.Provider value={{ user, setUser, logoutUser }}>
            {children}
        </UserContext.Provider>
    );
};

export default UserContext;
