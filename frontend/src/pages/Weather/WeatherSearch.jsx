import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import { Container, Typography, Button, TextField, Box, Autocomplete, CircularProgress} from "@mui/material";
// import useFetchUser from "../../hooks/useFetchUser";
import useFetchCities from "../../hooks/useFetchCities";
import { searchTravel } from "../../utils/api";
import "./Weather.css";

function Weather() {
  // const user = useFetchUser();
  const user = { userId: "abc123" };
  const cities = useFetchCities("/weather_cities.json"); 
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useState({
    destination: null
  });

  const handleInputChange = (name, value) => {
    setSearchParams((prev) => ({ ...prev, [name]: value }));
  };

  const handleSearch = async () => {  
    const destinationCity = searchParams.destination ? searchParams.destination.city : null;
    const destinationCountryCode = searchParams.destination ? searchParams.destination.country_code : null;
      
    if (!destinationCity || !destinationCountryCode) {
      alert("Please select destination.");
      return;
    }
    setLoading(true);
    
    const requestBody = {
      user_id: user.userId,
      weather: {
        city: destinationCity,
        country_code: destinationCountryCode
      },
    };
    
    console.log("API Request:", JSON.stringify(requestBody, null, 2));

    const data = await searchTravel(requestBody);
    if (data) {
      console.log("Response:", data);
        if (data.user_id === user.userId) {
          navigate('/weather/results', { state: { weatherData: data.results } });
        }
    } else {
      console.error("Failed to fetch travel data");
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 10, textAlign: "center" }} className="home-container">
      <div className="background-overlay"></div>
      
      <Box className="content-box">
      {user ? (
        <>
          <Typography variant="h4" className="page-title" sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 700 }}>Plan Your Travel</Typography>
         
          <Box className="search-box" sx={{ width: "400px" }}>
            <Autocomplete
              freeSolo
              options={cities}
              getOptionLabel={(option) => `${option.city} (${option.country})`}
              value={searchParams.destination || null}
              onChange={(event, newValue) => handleInputChange("destination", newValue)}
              renderInput={(params) => <TextField {...params} label="Destination" fullWidth className="input-field" />}
            />

            <Button variant="contained" className="search-button" onClick={handleSearch}>
              Search Weather
            </Button>
          </Box> 
          {loading && (
          <>
            <div className="overlay"></div>

            <div className="loader-container">
              <CircularProgress sx={{ color: '#023641', mb: 2 }} />
              <Typography variant="h6" className="loading-text">
                Just a moment, we're packing your bags!
              </Typography>
            </div>
          </>
          )}
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
