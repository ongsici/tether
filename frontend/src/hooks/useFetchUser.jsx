import { useState, useEffect } from "react";
import { fetchUser } from "../utils/auth";

const useFetchUser = () => {
    const [user, setUser] = useState(null);
  
    useEffect(() => {
      async function getUser() {
        const userData = await fetchUser();
        setUser(userData);
      }
      getUser();
    }, []);
  
    return user;
  };
  
export default useFetchUser;