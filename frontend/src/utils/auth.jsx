
export const login = () => {
    window.location.href = "/.auth/login/github"; // Change provider if needed
  };
  
export const logout = () => {
window.location.href = "/.auth/logout";
};

export const fetchUser = async () => {
try {
    const response = await fetch("/.auth/me");
    if (!response.ok) throw new Error("Failed to fetch user");

    const data = await response.json();
    return data?.[0] || null; // Assuming user data is the first item in an array
} catch (error) {
    console.error("Error fetching user:", error);
    return null;
}
};
