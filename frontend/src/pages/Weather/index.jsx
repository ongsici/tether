import React, { useState } from "react";
import { Container, Typography, Button, TextField, Box, Autocomplete } from "@mui/material";
import useFetchUser from "../../hooks/useFetchUser";
import useFetchCities from "../../hooks/useFetchCities";
import { getTodayDate } from "../../utils/helpers";
import { searchTravel } from "../../utils/api";
import "./Weather.css";

function Weather() {
  const user = useFetchUser();
  const cities = useFetchCities(); 
  const [searchParams, setSearchParams] = useState({
    destination: "",
    departDate: "",
    returnDate: "",
  });

  const handleInputChange = (name, value) => {
    setSearchParams((prev) => ({ ...prev, [name]: value }));
  };

  const handleSearch = async () => {
      
      const destinationCity = cities.find(city => city.city === searchParams.destination?.city)?.code;
      
      if (!destinationCity || !searchParams.departDate || !searchParams.returnDate ) {
        alert("Please select valid source and destination.");
        return;
      }
      
      const requestBody = {
        flights: {
          destination: destinationCity,
          departureDate: searchParams.departDate,
          returnDate: searchParams.returnDate,
        },
      };
      
      console.log("API Request:", JSON.stringify(requestBody, null, 2));
  
      const data = await searchTravel(requestBody);
      if (data) {
        console.log("Response:", data);
      } else {
        console.error("Failed to fetch travel data");
      }
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
            <Button variant="contained" className="search-button" onClick={handleSearch}>
              Search Weather
            </Button>
          </Box>
        </>
      ) : (
        <>
          <Typography variant="h6" className="welcome-title">Login to search for weather</Typography>
        </>
      )}
      </Box>
    </Container>
  );
}

export default Weather;
