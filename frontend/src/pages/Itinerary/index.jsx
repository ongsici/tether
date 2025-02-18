import React, { useState, useEffect } from "react";
import { Container, Typography, Button, TextField, Box } from "@mui/material";
import { fetchUser } from "../../utils/auth";
import Footer from "../../components/Footer";
import "./Itinerary.css";

function Itinerary() {
  const [user, setUser] = useState(null);
  const [searchParams, setSearchParams] = useState({
    destination: "",
    departDate: "",
    returnDate: "",
  });

  useEffect(() => {
    async function getUser() {
      const userData = await fetchUser();
      setUser(userData);
    }
    getUser();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSearchParams((prev) => ({ ...prev, [name]: value }));
  };

  const handleSearch = () => {
    console.log("Search initiated with:", searchParams);
    // Call backend API to get search results
  };

  return (
    <Container maxWidth="md" sx={{ mt: 6, textAlign: "center" }} className="home-container">
      <div className="background-overlay"></div>
      <Box className="content-box">
      {user ? (
        <>
          <Typography variant="h4" className="page-title">Plan Your Travel</Typography>

          <Box className="search-box">
            <TextField
              label="Destination"
              name="destination"
              value={searchParams.destination}
              onChange={handleInputChange}
              fullWidth
              className="input-field"
            />
            <TextField
              label="Departure Date"
              name="departDate"
              type="date"
              InputLabelProps={{ shrink: true }}
              value={searchParams.departDate}
              onChange={handleInputChange}
              fullWidth
              className="input-field"
            />
            <TextField
              label="Return Date"
              name="returnDate"
              type="date"
              InputLabelProps={{ shrink: true }}
              value={searchParams.returnDate}
              onChange={handleInputChange}
              fullWidth
              className="input-field"
            />
            <Button variant="contained" className="search-button" onClick={handleSearch}>
              Search Itinerary
            </Button>
          </Box>
        </>
      ) : (
        <>
          <Typography variant="h6" className="welcome-title">Login to search for itinerary</Typography>
        </>
      )}
      </Box>
      <Footer />{/* Include the Footer component */}
    </Container>
  );
}

export default Itinerary;
