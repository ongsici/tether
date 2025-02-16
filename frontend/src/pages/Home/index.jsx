import React, { useState, useEffect } from "react";
import { Container, Typography, Button, TextField, Checkbox, FormControlLabel, Box } from "@mui/material";
import { login, fetchUser } from "../../utils/auth";
import "./Home.css";

function Home() {
  const [user, setUser] = useState(null);
  const [searchParams, setSearchParams] = useState({
    source: "",
    destination: "",
    departDate: "",
    returnDate: "",
    includeItinerary: false,
    includeWeather: false,
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

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setSearchParams((prev) => ({ ...prev, [name]: checked }));
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
              label="Source"
              name="source"
              value={searchParams.source}
              onChange={handleInputChange}
              fullWidth
              className="input-field"
            />
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
            <FormControlLabel
              control={
                <Checkbox
                  checked={searchParams.includeItinerary}
                  onChange={handleCheckboxChange}
                  name="includeItinerary"
                  className="checkbox"
                />
              }
              label="Include Itinerary Suggestions"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={searchParams.includeWeather}
                  onChange={handleCheckboxChange}
                  name="includeWeather"
                  className="checkbox"
                />
              }
              label="Include Weather Forecast"
            />
            <Button variant="contained" className="search-button" onClick={handleSearch}>
              Search Flights
            </Button>
          </Box>
        </>
      ) : (
        <>
          <Typography variant="h3" className="welcome-title">Welcome to TETHER</Typography>
          <Typography variant="h6" className="description-text">
            Your AI-powered travel planner. Easily search flights, plan your itinerary, and get weather forecasts.
          </Typography>
          <Button className="login-button" onClick={login}>
            Login to Start
          </Button>
        </>
      )}
      </Box>
    </Container>
  );
}

export default Home;
