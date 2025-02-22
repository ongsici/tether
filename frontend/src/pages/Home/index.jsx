import React, { useState, useEffect } from "react";
import { Container, Typography, Button, TextField, Checkbox, FormControlLabel, Box, Autocomplete, Select, MenuItem, InputLabel, FormControl } from "@mui/material";
import { login, fetchUser } from "../../utils/auth";
import { searchTravel } from "../../utils/api";
import "./Home.css";
// import Toast from "../../components/Toast";

function Home() {
  const [user, setUser] = useState(null);
  const [cities, setCities] = useState([]);
  // const [showToast, setShowToast] = useState(false)
  const [searchParams, setSearchParams] = useState({
    source: "",
    destination: "",
    departDate: "",
    returnDate: "",
    numTravellers: 1,
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
    fetch("/cities.json")
      .then(response => response.json())
      .then(data => {
        setCities(data);
      });
  }, []);

  const getTodayDate = () => {
    const today = new Date();
    return today.toISOString().split("T")[0];  // Format as YYYY-MM-DD
  };

  // const handleErrorToast = () => {
  //   setShowToast(true);
  //   setTimeout(() => setShowToast(false), 3000);
  // };

  const handleInputChange = (name, value) => {
    setSearchParams((prev) => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setSearchParams((prev) => ({ ...prev, [name]: checked }));
  };

  const handleSearch = async () => {

    const sourceCity = cities.find(city => city.city === searchParams.source?.city)?.code;
    const destinationCity = cities.find(city => city.city === searchParams.destination?.city)?.code;
    
    if (!sourceCity || !destinationCity || !searchParams.departDate || !searchParams.returnDate || !searchParams.numTravellers) {
      // handleErrorToast();
      alert("Please select valid source and destination.");
      return;
    }
    
    const requestBody = {
      flights: {
        source: sourceCity,
        destination: destinationCity,
        departureDate: searchParams.departDate,
        returnDate: searchParams.returnDate,
        numTravellers: searchParams.numTravellers.toString(),
      },
    };
    
    if (searchParams.includeItinerary) {
      requestBody.itinerary = {
        destination: destinationCity,
        startDate: searchParams.departDate,
        endDate: searchParams.returnDate,
      };
    }

    if (searchParams.includeWeather) {
      requestBody.weather = {
        destination: destinationCity,
        startDate: searchParams.departDate,
        endDate: searchParams.returnDate,
      };
    }
    console.log("API Request:", JSON.stringify(requestBody, null, 2));

    const data = await searchTravel(requestBody);
    if (data) {
      console.log("Response:", data);
    } else {
      console.error("Failed to fetch travel data");
    }
  };

  // if (showToast) {
  //   return (
  //     <Toast message="Error (TODO: change message)" onClose={() => setShowToast(false)} />
  //   )
  // }

  return (
    <Container maxWidth="md" sx={{ mt: 6, textAlign: "center" }} className="home-container">
      <div className="background-overlay"></div>
      <Box className="content-box">
      {!user ? (
        <>
          <Typography variant="h4" className="page-title">Plan Your Travel</Typography>

          <Box className="search-box">
          
            <Autocomplete
              freeSolo
              options={cities}
              getOptionLabel={(option) => `${option.city} (${option.country})`}
              value={searchParams.source || null}
              onChange={(event, newValue) => handleInputChange("source", newValue)}
              renderInput={(params) => <TextField {...params} label="Source" fullWidth className="input-field" />}
            />

            <Autocomplete
              freeSolo
              options={cities}
              getOptionLabel={(option) => `${option.city} (${option.country})`}
              value={searchParams.destination || null}
              onChange={(event, newValue) => handleInputChange("destination", newValue)}
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
              inputProps={{
                min: getTodayDate(),
              }}
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
              inputProps={{
                min: searchParams.departDate || getTodayDate(),  
              }}
            />
            <FormControl fullWidth className="input-field">
                <InputLabel id="travellers-label">Number of Travellers</InputLabel>
                <Select
                  labelId="travellers-label"
                  value={searchParams.numTravellers}
                  onChange={(e) => handleInputChange("numTravellers", e.target.value)}
                  label="Number of Travellers"
                >
                  {[1, 2, 3, 4, 5, 6, 7, 8].map((num) => (
                    <MenuItem key={num} value={num}>
                      {num}
                    </MenuItem>
                  ))}
                </Select>
            </FormControl>
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
