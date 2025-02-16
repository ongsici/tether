// import axios from "axios";

export const login = () => {
    window.location.href = "/.auth/login/github"; // Change provider if needed
  };
  
export const logout = () => {
    window.location.href = "/.auth/logout";
};


export const fetchUser = async () => {
    try {
      const res = await fetch("/.auth/me");
      const data = await res.json();
      return data.clientPrincipal || null; // Returns user object or null if not logged in
    } catch (error) {
      console.error("Failed to fetch user:", error);
      return null;
    }
  };
