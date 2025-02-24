import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import { Container, Typography, Button, TextField, Box, Autocomplete, FormControl, InputLabel, Select, MenuItem, CircularProgress } from "@mui/material";
import useFetchUser from "../../hooks/useFetchUser";
import useFetchCities from "../../hooks/useFetchCities";
import { getTodayDate, getAirportOptions } from "../../utils/helpers";
import { searchTravel } from "../../utils/api";
import "./Flights.css";

function Flights() {
  const user = useFetchUser();
  const cities = useFetchCities();  
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useState({
    source: "",
    destination: "",
    departDate: "",
    returnDate: "",
    numTravellers: 1
  });

  const handleInputChange = (name, value) => {
    setSearchParams((prev) => ({ ...prev, [name]: value }));
  };

  const handleSearch = async () => {
    const sourceAirport = searchParams.source?.airportCode;
    const destinationAirport = searchParams.destination?.airportCode;

    if (!sourceAirport || !destinationAirport || !searchParams.departDate || !searchParams.returnDate || !searchParams.numTravellers) {
      alert("Please select valid source and destination.");
      return;
    }
  
    setLoading(true);
  
    const requestBody = {
      flights: {
        source: sourceAirport,
        destination: destinationAirport,  
        departureDate: searchParams.departDate,
        returnDate: searchParams.returnDate,
        numTravellers: searchParams.numTravellers.toString(),
      },
    };
  
    console.log("API Request:", JSON.stringify(requestBody, null, 2));
  
    const data = await searchTravel(requestBody);
    if (data) {
      console.log("Response:", data);
      navigate('/flights/results', { state: { flightData: data } });
    } else {
      console.error("Failed to fetch travel data");
    }
    setLoading(false);
  };
  
  // const getAirportOptions = (inputValue) => {
  //   const query = (typeof inputValue === 'string' ? inputValue : '').toLowerCase();
  
  //   const matchingCities = cities.filter((city) =>
  //     city.city.toLowerCase().includes(query)
  //   );
    
  //   return matchingCities.flatMap((city) =>
  //     city.airports.map((airport, index) => ({
  //       city: city.city,
  //       country: city.country,
  //       airportCode: airport,
  //       airportName: city.airport_names[index],
  //       fullLabel: `${airport} (${city.city}, ${city.country})`,
  //     }))
  //   );
  // };
    

  return (
    <Container maxWidth="md" sx={{ mt: 6, textAlign: "center" }} className="home-container">
      <div className="background-overlay"></div>
      <Box className="content-box">
      {!user ? (
        <>
          <Typography variant="h4" className="page-title" sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 700 }}>Plan Your Travel</Typography>

          <Box className="search-box">


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

{/* 

            <Autocomplete
                freeSolo
                options={getAirportOptions(searchParams.destination || "")}
                getOptionLabel={(option) => option.fullLabel}
                value={searchParams.destination || null}
                onChange={(event, newValue) => handleInputChange("destination", newValue)}
                renderInput={(params) => <TextField {...params} label="Destination" fullWidth className="input-field" />}
            /> */}

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

            <Button variant="contained" className="search-button" onClick={handleSearch}>
              Search Flights
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
          <Typography variant="h6" className="welcome-title">Login to search for flights</Typography>
        </>
      )}
      </Box>
    </Container>
  );
}

export default Flights;
