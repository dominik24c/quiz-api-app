import {createContext, useState, useEffect, useCallback} from "react";

const AuthContext = createContext({
    isLoggedIn: false,
    token: null,
    login: (token, expirationTime) => {
    },
    logout: () => {
    }
})

const ACCESS_TOKEN = 'access-token';
const EXPIRED_TIME = 'expired-time';
let logoutTimer = null;

const getRemainingTimeToLogout = (expiredDate) => {
    const currentTime = new Date().getTime();
    const expiredTime = new Date(expiredDate).getTime();
    return expiredTime - currentTime;
}
const getToken = () => {
    const token = localStorage.getItem(ACCESS_TOKEN);
    const expiredDate = localStorage.getItem(EXPIRED_TIME);

    const remainingTime = getRemainingTimeToLogout(expiredDate);
    if (remainingTime <= 1000) {
        localStorage.removeItem(ACCESS_TOKEN);
        localStorage.removeItem(EXPIRED_TIME);
        return null;
    }

    return {
        token,
        expiredTime: remainingTime
    };
}

export const AuthContextProvider = (props) => {
    const tokenData = getToken();
    const [token, setToken] = useState(tokenData ? tokenData.token : null);
    const isLoggedIn = !!token;

    const logoutHandler = useCallback(() => {
        localStorage.removeItem(ACCESS_TOKEN);
        localStorage.removeItem(EXPIRED_TIME);
        setToken(null);

        if (logoutTimer) {
            clearTimeout(logoutTimer);
        }
    }, []);


    const loginHandler = (token, expirationTime) => {
        localStorage.setItem(ACCESS_TOKEN, token);
        localStorage.setItem(EXPIRED_TIME, expirationTime);
        setToken(token);
        const remainingTime = getRemainingTimeToLogout(expirationTime);
        logoutTimer = setTimeout(logoutHandler, remainingTime);
    };

    useEffect(() => {
        if (tokenData) {
            // console.log(tokenData.expiredTime)

            logoutTimer = setTimeout(logoutHandler, tokenData.expiredTime)
        }
    }, [tokenData, logoutHandler]);


    const contextValue = {
        token: token,
        isLoggedIn: isLoggedIn,
        login: loginHandler,
        logout: logoutHandler
    }

    return (
        <AuthContext.Provider value={contextValue}>
            {props.children}
        </AuthContext.Provider>
    );
}

export default AuthContext;