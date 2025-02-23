import React, { useState } from "react";
import { Container, Typography, Button, TextField, Box, Autocomplete, CircularProgress} from "@mui/material";
import useFetchUser from "../../hooks/useFetchUser";
import useFetchCities from "../../hooks/useFetchCities";
import { searchTravel } from "../../utils/api";
import "./Weather.css";

function Weather() {
  const user = useFetchUser();
  const cities = useFetchCities(); 
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState({ });
  const [searchParams, setSearchParams] = useState({
    destination: ""
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
    setLoading(true);
    setResults({ });
    
    const requestBody = {
      weather: {
        destination: destinationCity,
      },
    };
    
    console.log("API Request:", JSON.stringify(requestBody, null, 2));

    const data = await searchTravel(requestBody);
    if (data) {
      console.log("Response:", data);
      setResults(data);
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

            <Button variant="contained" className="search-button" onClick={handleSearch}>
              Search Weather
            </Button>
          </Box> 
          {loading && <CircularProgress sx={{ mt: 2 }} />}
          {!loading && results?.results && (
            <Box className="weather-box">
              <Typography variant="h5">Weather Forecast</Typography>
              <pre>{JSON.stringify(results.results, null, 2)}</pre>
            </Box>
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
