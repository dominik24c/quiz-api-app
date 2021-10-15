import React, {useContext} from "react";
import AuthContext from "../../context/AuthContext";

const LogoutBtn = () => {
    const authContext = useContext(AuthContext);

    const logoutHandler = () => {
        authContext.logout();
    }

    return (
        <button onClick={logoutHandler}>Logout</button>
    );
}

export default LogoutBtn;