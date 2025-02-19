import React, { useState, useEffect } from "react";
import { Container, Typography, Box } from "@mui/material";
import { fetchUser } from "../../utils/auth";
import "./Dashboard.css";

function Dashboard() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    async function getUser() {
      const userData = await fetchUser();
      setUser(userData);
    }
    getUser();
  }, []);

//   const handleInputChange = (e) => {
//     const { name, value } = e.target;
//     setSearchParams((prev) => ({ ...prev, [name]: value }));
//   };


  return (
    <Container maxWidth="md" sx={{ mt: 6, textAlign: "center" }} className="home-container">
      <div className="background-overlay"></div>
      <Box className="content-box">
      {user ? (
        <>
          <Typography variant="h6" className="page-title">Display saved items</Typography>
        </>
      ) : (
        <>
          <Typography variant="h6" className="welcome-title">Login to retrieve saved items</Typography>
        </>
      )}
      </Box>
    </Container>
  );
}

export default Dashboard;
