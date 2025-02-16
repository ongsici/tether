
export const login = () => {
    window.location.href = "/.auth/login/github"; // Change provider if needed
  };
  
export const logout = () => {
    window.location.href = "/.auth/logout";
};

// export const fetchUser = async () => {
// try {
//     const response = await fetch("/.auth/me");
//     if (!response.ok) throw new Error("Failed to fetch user");

//     const data = await response.json();
//     return data?.[0] || null; // Assuming user data is the first item in an array
// } catch (error) {
//     console.error("Error fetching user:", error);
//     return null;
// }
// };

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
