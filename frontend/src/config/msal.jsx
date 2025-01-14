const msalConfig = {
    auth: {
        clientId: "a31f643e-0f62-4075-8e2a-da99a1d593fc",
        authority: "https://login.microsoftonline.com/common",
        redirectUri: "http://localhost:5173",
    },
};

const loginRequest = {
    scopes: ["User.Read"],
};

export { msalConfig, loginRequest };