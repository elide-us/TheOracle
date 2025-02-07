import { useState, useEffect, useContext } from "react";
import axios from "axios";
import UserContext from "./shared/UserContextProvider";
import { Container, Typography, TextField, Button, Link } from "@mui/material";
//import { Container, Typography, TextField, Button, List, ListItem, ListItemText, Link } from "@mui/material";
//import { useNavigate } from "react-router-dom";

const UserPanel = () => {
    const { userData, setUserData } = useContext(UserContext);
    const [ profile, setProfile ] = useState(null); // Local state for profile details
    // const navigate = useNavigate();

    useEffect(() => {
        if (!userData?.token) return; // Ensure token exists

        axios.get("/api/userpage", {
            headers: { Authorization: `Bearer ${userData.token}` },
        })
        .then((res) => { setProfile(res.data); })
        .catch((err) => console.error("Failed to fetch user data", err));
    }, [userData.token]);

    if (!profile) return <Typography>Loading...</Typography>;
 
    const handleChange = (e) => {
        const { name, value } = e.target;
        setProfile((prevProfile) => ({ ...prevProfile, [name]: value }));
    };
    
    const handleSubmit = (e) => {
        e.preventDefault();
    
        // Post updated profile data to the API
        axios.post("/api/userpage", profile, {
            headers: { Authorization: `Bearer ${userData.token}` },
        })
        .then((res) => {
            setProfile(res.data);

            // Optionally, update the global userData if certain values have changed.
            // For example, if the defaultProvider changes or if you want to sync the credits.
            // You can also add more logic to check if the default provider is one of the linked accounts.
            setUserData((prevData) => ({
                ...prevData,

                defaultProvider: res.data.defaultProvider,
                username: res.data.username,
                email: res.data.email,
                backupEmail: res.data.backupEmail,
                credits: res.data.credits,
            }));
        })
        .catch((err) => console.error("Failed to update user data", err));
    };

    return (
        <Box>
            <Typography variant="h5" gutterBottom>
                User Settings
            </Typography>
            <form onSubmit={handleSubmit}>
                {/* Editable fields */}
                <TextField
                    fullWidth
                    margin="normal"
                    label="Display Name"
                    name="username"
                    value={profile.username || ""}
                    disabled
                />
                <TextField
                    fullWidth
                    margin="normal"
                    label="Email Address"
                    name="email"
                    value={profile.email || ""}
                    disabled
                />
                <TextField
                    fullWidth
                    margin="normal"
                    label="Backup Email"
                    name="backupEmail"
                    value={profile.backupEmail || ""}
                    onChange={handleChange}
                />
                <TextField
                    fullWidth
                    margin="normal"
                    label="Default Provider"
                    name="defaultProvider"
                    value={profile.defaultProvider || ""}
                    disabled
                />
        
                <Button type="submit" variant="contained" color="primary">
                    Save Changes
                </Button>
            </form>
    
            {/* <Typography variant="h6" gutterBottom style={{ marginTop: "2rem" }}>
                Linked Accounts
            </Typography>
            <List>
                {["Microsoft", "Discord", "Google", "Apple"].map((provider) => (
                <ListItem key={provider}>
                    <ListItemText
                        primary={provider}
                        secondary={
                            profile.linkedAccounts?.includes(provider)
                            ? "Linked"
                            : "Not Linked"
                        }
                    />
                    {profile.linkedAccounts?.includes(provider) ? (
                    <Button variant="outlined" size="small">
                        Unlink
                    </Button>
                    ) : (
                    <Button variant="contained" size="small">
                        Link
                    </Button>
                    )}
                </ListItem>
                ))}
            </List> */}
    
            <Typography variant="h6" gutterBottom>
                Credits: {profile.credits}
            </Typography>
            <Link href="/purchase">Buy More Credits</Link>
        </Box>
    );
};

export default UserPanel;
