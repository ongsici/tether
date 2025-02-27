import React, { useState } from "react";
import { Container, Typography, Button, TextField, Checkbox, FormControlLabel, Box, Autocomplete, Select, MenuItem, InputLabel, FormControl, CircularProgress } from "@mui/material";
import { login } from "../../utils/auth";
import { searchTravel } from "../../utils/api";
import { getTodayDate, getAirportOptions } from "../../utils/helpers";
import useFetchCities from "../../hooks/useFetchCities";
// import useFetchUser from "../../hooks/useFetchUser";
import "./Home.css";
import { useNavigate } from "react-router";

function Home() {
  // const user = useFetchUser();
  const user = { userId: "abc123" };
  const cities = useFetchCities(); 

  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useState({
    source: "",
    destination: "",
    destinationCity: "",
    departDate: "",
    returnDate: "",
    numTravellers: 1,
    includeItinerary: false,
  });


  const handleInputChange = (name, value) => {
    setSearchParams((prev) => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setSearchParams((prev) => ({ ...prev, [name]: checked }));
  };

  const handleSearch = async () => {

    const sourceAirport = searchParams.source?.airportCode;
    const destinationAirport = searchParams.destination?.airportCode;
    const destinationCity = searchParams.destination?.city;
    
    if (!sourceAirport || !destinationAirport || !searchParams.departDate || !searchParams.returnDate || !searchParams.numTravellers) {
      // handleErrorToast();
      alert("Please select valid source and destination.");
      return;
    }

    setLoading(true);
    
    const requestBody = {
      user_id: user.userId,
      flights: {
        origin_loc_code: sourceAirport,
        destination_loc_code: destinationAirport,
        departure_date: searchParams.departDate,
        return_date: searchParams.returnDate,
        num_passenger: searchParams.numTravellers.toString(),
      },
    };
    
    if (searchParams.includeItinerary) {
      requestBody.itinerary = {
        destination: destinationCity,
        startDate: searchParams.departDate,
        endDate: searchParams.returnDate,
      };
    }

    console.log("API Request:", JSON.stringify(requestBody, null, 2));

    const data = await searchTravel(requestBody);
    if (data) {
      console.log("Response:", data);
      if (data.user_id === user.userId) {
        navigate('/results', { state: { flightData: data } });
      }
    } else {
      console.error("Failed to fetch travel data");
    }
    setLoading(false);
  };


  return (
    <Container maxWidth="md" sx={{ mt: 6, textAlign: "center" }} className="home-container">
      <div className="background-overlay"></div>
      <Box className="content-box">
      {user ? (
        <>
          <Typography variant="h4" className="page-title" sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 700 }}>Plan Your Travel</Typography>

          <Box className="search-box" sx={{ width: "600px" }}>
          
            <Autocomplete
              freeSolo
              options={getAirportOptions(searchParams.source || "", cities)}
              getOptionLabel={(option) => option.fullLabel}
              value={searchParams.source || null}
              onChange={(event, newValue) => handleInputChange("source", newValue)}
              renderInput={(params) => <TextField {...params} label="Source" fullWidth className="input-field" />}
              renderOption={(props, option) => (
                <li {...props} className="MuiAutocomplete-option" style={{ display: 'flex', flexDirection: 'column' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                    <span className="option-city-country" style={{ textAlign: 'left' }}> 
                      {option.city}, {option.country}
                    </span>
                    <span className="airport-code">{option.airportCode}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                    <span className="option-airport-name" style={{ textAlign: 'left' }}>
                      {option.airportName}
                    </span>
                  </div>
                </li>
              )}
            />

            <Autocomplete
              freeSolo
              options={getAirportOptions(searchParams.destination || "", cities)}
              getOptionLabel={(option) => option.fullLabel}
              value={searchParams.destination || null}
              onChange={(event, newValue) => handleInputChange("destination", newValue)}
              renderInput={(params) => <TextField {...params} label="Destination" fullWidth className="input-field" />}
              renderOption={(props, option) => (
                <li {...props} className="MuiAutocomplete-option" style={{ display: 'flex', flexDirection: 'column' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                    <span className="option-city-country" style={{ textAlign: 'left' }}> 
                      {option.city}, {option.country}
                    </span>
                    <span className="airport-code">{option.airportCode}</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
                    <span className="option-airport-name" style={{ textAlign: 'left' }}>
                      {option.airportName}
                    </span>
                  </div>
                </li>
              )}
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
            <FormControl fullWidth className="input-field" sx={{"& .MuiInputBase-root": { height: "60px" } }}>
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
        
            <Button variant="contained" className="search-button" onClick={handleSearch}>
              Search Travel
            </Button>
          </Box>
          {loading && (
          <>
            {/* Whitewash Overlay */}
            <div className="overlay"></div>

            {/* Centered Circular Progress */}
            <div className="loader-container">
              <CircularProgress sx={{ color: '#023641' }} />
              <Typography variant="h6" className="loading-text">
                Just a moment, we're packing your bags!
              </Typography>
            </div>
          </>
          )}
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
