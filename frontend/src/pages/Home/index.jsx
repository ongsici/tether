import React, { useState, useEffect } from "react";
import { Container, Typography, Button, TextField, Checkbox, FormControlLabel, Box } from "@mui/material";
import { login, fetchUser } from "../../utils/auth";
import "./Home.css";

function Home() {
  const [user, setUser] = useState(null);
  const [searchParams, setSearchParams] = useState({
    source: "",
    destination: "",
    travelDate: "",
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
    <Container maxWidth="md" sx={{ mt: 4, textAlign: "center" }}>
      {user ? (
        // After login: Show search form
        <>
          <Typography variant="h4" sx={{ mb: 2 }}>Plan Your Travel</Typography>

          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <TextField
              label="Source"
              name="source"
              value={searchParams.source}
              onChange={handleInputChange}
              fullWidth
            />
            <TextField
              label="Destination"
              name="destination"
              value={searchParams.destination}
              onChange={handleInputChange}
              fullWidth
            />
            <TextField
              label="Travel Date"
              name="travelDate"
              type="date"
              InputLabelProps={{ shrink: true }}
              value={searchParams.travelDate}
              onChange={handleInputChange}
              fullWidth
            />
            {/* Optional checkboxes */}
            <FormControlLabel
              control={
                <Checkbox
                  checked={searchParams.includeItinerary}
                  onChange={handleCheckboxChange}
                  name="includeItinerary"
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
                />
              }
              label="Include Weather Forecast"
            />
            <Button variant="contained" color="primary" onClick={handleSearch}>
              Search Flights
            </Button>
          </Box>
        </>
      ) : (
        // Before login: Show product description
        <>
          <Typography variant="h3">Welcome to TETHER</Typography>
          <Typography variant="h6" sx={{ my: 2 }}>
            Your AI-powered travel planner. Easily search flights, plan your itinerary, and get weather forecasts.
          </Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={login} 
          >
            Login to Start
          </Button>
        </>
      )}
    </Container>
  );
}

export default Home;

