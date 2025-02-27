import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import { Container, Typography, Button, TextField, Box, FormControl, InputLabel, Select, MenuItem, Autocomplete, CircularProgress } from "@mui/material";
import useFetchCities from "../../hooks/useFetchCities";
import { searchTravel } from "../../utils/api";
import { useItinerary } from "../../context/ItineraryProvider";
import "./Itinerary.css";

const Itinerary = () => {
  const user = { userId: "abc123" };
  const cities = useFetchCities(); 
  const navigate = useNavigate();
  const { setItinerary } = useItinerary();
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useState({
    destination: "",
    radius: "",
    limit: "",
  });

  const handleInputChange = (name, value) => {
    setSearchParams((prev) => ({ ...prev, [name]: value }));
  };

  const handleSearch = async () => {
    const destinationCity = searchParams.destination ? searchParams.destination.city : null;
    
    if (!destinationCity || !searchParams.radius || !searchParams.limit ) {
      alert("Please select valid source and destination.");
      return;
    }

    setLoading(true);
    
    const requestBody = {
      user_id: user.userId,
      itinerary: {
        city: destinationCity,
        radius: searchParams.radius,
        limit: searchParams.limit,
      },
    };
    
    console.log("API Request:", JSON.stringify(requestBody, null, 2));

    const data = await searchTravel(requestBody);
    if (data) {
      console.log("Response:", data);
      if (data.user_id === user.userId) {
        setItinerary(data.results);
        navigate('/itinerary/results');
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
          <Typography variant="h4" className="page-title" sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 700 }} >Plan Your Travel</Typography>
          
          <Box className="search-box" sx={{ width: "400px" }}>
            <Autocomplete
              freeSolo
              options={cities}
              getOptionLabel={(option) => `${option.city} (${option.country})`}
              value={searchParams.destination || null}
              onChange={(event, newValue) => handleInputChange("destination", newValue)}
              renderInput={(params) => <TextField {...params} label="Destination" fullWidth className="input-field" />}
            />

            <FormControl fullWidth className="radius-field" sx={{"& .MuiInputBase-root": { height: "60px" } }}>
                <InputLabel id="radius-label">Search Radius (km)</InputLabel>
                <Select
                  labelId="radius-label"
                  value={searchParams.radius}
                  onChange={(e) => handleInputChange("radius", e.target.value)}
                  label="Search Radius" className="input-field"
                >
                  {[...Array(20).keys()].map(num => (
                    <MenuItem key={num+1} value={num+1}>{num+1}</MenuItem>
                  ))}
                </Select>
            </FormControl>

            <FormControl fullWidth className="limit-field" sx={{"& .MuiInputBase-root": { height: "60px" } }}>
                <InputLabel id="limit-label">Number of Activities</InputLabel>
                <Select
                  labelId="limit-label"
                  value={searchParams.limit}
                  onChange={(e) => handleInputChange("limit", e.target.value)}
                  label="Number of Activities" className="input-field"
                >
                  {[...Array(10).keys()].map(num => (
                    <MenuItem key={num+1} value={num+1}>{num+1}</MenuItem>
                  ))}
                </Select>
            </FormControl>
          
            <Button variant="contained" className="search-button" onClick={handleSearch}>
              Search Itinerary
            </Button>
          </Box>

          {loading && (
          <>
            <div className="overlay"></div>
            <div className="loader-container">
              <CircularProgress sx={{ color: '#023641' }} />
              <Typography variant="h6" className="loading-text">
                Just a moment, we're looking for exciting stuff for you!
              </Typography>
            </div>
          </>
          )}
        </>
      ) : (
        <Typography variant="h6" className="welcome-title">Login to search for itinerary</Typography>
      )}
      </Box>
    </Container>
  );
}

export default Itinerary;

