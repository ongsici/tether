import React, { useState, useEffect } from "react";
import Papa from "papaparse";
import { Container, Typography, Button, TextField, Checkbox, FormControlLabel, Box, Autocomplete } from "@mui/material";
import { login, fetchUser } from "../../utils/auth";
// import Footer from "../../components/Footer";
import "./Home.css";

function Home() {
  const [user, setUser] = useState(null);
  const [cities, setCities] = useState([]);
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

  useEffect(() => {
    // Load city list from CSV file
    fetch("../../assets/cities.csv")
      .then(response => response.text())
      .then(csv => {
        Papa.parse(csv, {
          header: true,
          skipEmptyLines: true,
          complete: (result) => {
            setCities(result.data.map(row => `${row.cities} (${row.countries})`));
          },
        });
      });
  }, []);

  const handleInputChange = (name, value) => {
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
            <Autocomplete
              freeSolo
              options={cities}
              value={searchParams.source}
              onInputChange={(event, newValue) => handleInputChange("source", newValue)}
              renderInput={(params) => <TextField {...params} label="Source" fullWidth className="input-field" />}
            />

            <Autocomplete
              freeSolo
              options={cities}
              value={searchParams.destination}
              onInputChange={(event, newValue) => handleInputChange("destination", newValue)}
              renderInput={(params) => <TextField {...params} label="Destination" fullWidth className="input-field" />}
            />
            <TextField
              label="Departure Date"
              name="departDate"
              type="date"
              InputLabelProps={{ shrink: true }}
              value={searchParams.departDate}
              onChange={(e) => handleInputChange(e.target.name, e.target.value)}
              fullWidth
              className="input-field"
            />
            <TextField
              label="Return Date"
              name="returnDate"
              type="date"
              InputLabelProps={{ shrink: true }}
              value={searchParams.returnDate}
              onChange={(e) => handleInputChange(e.target.name, e.target.value)}
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
              Search Travel
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
