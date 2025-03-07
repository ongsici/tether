import React from "react";
import { useLocation } from "react-router-dom";
import { Box, Card, CardContent, Typography, Grid, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";
import { WbSunny, Cloud, Thunderstorm, AcUnit, BeachAccess, Storm } from "@mui/icons-material";
import DeviceThermostatIcon from '@mui/icons-material/DeviceThermostat';
import WaterIcon from '@mui/icons-material/Water';
import AirIcon from '@mui/icons-material/Air';
import useFetchUser from "../../hooks/useFetchUser";
import "./Weather.css";

const weatherIcons = {
  Clear: <WbSunny fontSize="large" color="warning" />,
  Clouds: <Cloud fontSize="large" color="action" />,
  Rain: <Thunderstorm fontSize="large" color="primary" />,
  Thunderstorm: <Thunderstorm fontSize="large" color="primary" />,
  Snow: <AcUnit fontSize="large" color="info" />,
  Drizzle: <BeachAccess fontSize="large" color="secondary" />,
  Atmosphere: <Storm fontSize="large" color="action"/>
};

const getWeatherGradient = (weather) => {
  switch (weather) {
    case "Clear":
      return "linear-gradient(135deg, #FFD700, #FFA500)";
    case "Clouds":
      return "linear-gradient(135deg, #B0BEC5, #78909C)"; 
    case "Rain":
      return "linear-gradient(135deg, #4FC3F7, #0288D1)"; 
    case "Snow":
      return "linear-gradient(135deg, #E0F7FA, #B3E5FC)";
    case "Thunderstorm":
      return "linear-gradient(135deg, #616161, #212121)"; 
    case "Drizzle":
      return "linear-gradient(135deg, #81D4FA, #4FC3F7)"; 
    case "Atmosphere":
      return "linear-gradient(135deg, #D7CCC8, #A1887F)"; 
    default:
      return "linear-gradient(135deg, #CFD8DC, #B0BEC5)"; 
  }
};

const WeatherResults = () => {
  const { state } = useLocation();
  const data = state?.weatherData;
  const user = useFetchUser();

  if (!data) {
    return <Typography>No weather data available</Typography>;
  }

  const { current, forecast } = data;

  return (
    <Box className="results-container">
      <div className="background-overlay"></div>

      {
        user ? (
          <>
          <Typography variant="h4" className="city-header" 
              sx={{ marginTop: 2, fontFamily: 'Roboto, sans-serif', fontWeight: 'bold', fontSize: '32px', color: '#023641' }}>
            {current.city}, {current.country}
          </Typography>


          <Grid container spacing={1} justifyContent="center" sx={{ marginBottom: 4, marginTop: 4}}>

            {/* Weather Description Card */}
            <Grid item xs={12} sm={6} md={2}>
              <Card className="weather-card" sx={{ width: '180px', backgroundColor: "rgba(255, 255, 255, 0.7)", boxShadow: 3, borderTop: "4px solid #023641", borderBottom: "4px solid #023641" }}>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: "bold" }} gutterBottom>
                    Weather
                  </Typography>
                  <div className="weather-icon">{weatherIcons[current.weather_main] || weatherIcons.Clouds}</div>
                  <Typography variant="h5">{current.weather_main}</Typography>
                  <Typography variant="body1">{current.weather_description}</Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Temperature Card */}
            <Grid item xs={12} sm={6} md={2}>
              <Card className="weather-card" sx={{ width: '180px', backgroundColor: "rgba(255, 255, 255, 0.7)",boxShadow: 3, borderTop: "4px solid #023641", borderBottom: "4px solid #023641" }}>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: "bold" }} gutterBottom>
                    Temperature
                  </Typography>
                  <DeviceThermostatIcon fontSize="large" sx={{ marginBottom: 2 }}/>
                  <Typography variant="h5">{current.temperature}°C</Typography>
                  <Typography variant="body2">Feels Like: {current.feels_like}°C</Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Humidity Card */}
            <Grid item xs={12} sm={6} md={2}>
              <Card className="weather-card" sx={{ width: '180px', backgroundColor: "rgba(255, 255, 255, 0.7)",boxShadow: 3, borderTop: "4px solid #023641", borderBottom: "4px solid #023641" }}>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: "bold" }} gutterBottom>
                    Humidity
                  </Typography>
                  <WaterIcon fontSize="large" sx={{ marginBottom: 2 }}/>
                  <Typography variant="h5">{current.humidity}%</Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* Wind Speed Card */}
            <Grid item xs={12} sm={6} md={2}>
              <Card className="weather-card" sx={{ width: '180px', backgroundColor: "rgba(255, 255, 255, 0.7)", boxShadow: 3, borderTop: "4px solid #023641", borderBottom: "4px solid #023641" }}>
                <CardContent>
                  <Typography variant="h6" sx={{ fontWeight: "bold" }} gutterBottom>
                    Wind Speed
                  </Typography>
                  <AirIcon fontSize="large" sx={{ marginBottom: 2 }}/>
                  <Typography variant="h5">{current.wind_speed} m/s</Typography>
                </CardContent>
              </Card>
            </Grid>

            
          </Grid>
          

          {/* Forecast Section */}
          <Typography variant="h5" className="forecast-header" 
                  sx={{fontFamily: 'Roboto, sans-serif', fontWeight: 'bold', fontSize: '28px', color: '#023641', marginBottom: 2}}>
            6-Day Forecast
          </Typography>

          {/* Forecast Table */}
          <Box sx={{ maxWidth: "1000px", margin: "0 auto", padding: 2 }}>
            <TableContainer component={Paper} sx={{ backgroundColor: "rgba(255, 255, 255, 0.6)", boxShadow: 3, borderRadius: "12px" , marginBottom: 6, borderTop: "4px solid #023641", borderBottom: "4px solid #023641" }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell align="center" sx={{ fontWeight: "bold" }}>Date</TableCell>
                    <TableCell align="center" sx={{ fontWeight: "bold" }} >Weather</TableCell>
                    <TableCell align="center" sx={{ fontWeight: "bold" }} >Temp (Min - Max) °C</TableCell>
                    <TableCell align="center" sx={{ fontWeight: "bold" }} >UV Index</TableCell>
                    <TableCell align="center" sx={{ fontWeight: "bold" }} >Precipitation (%)</TableCell>
                    <TableCell align="center" sx={{ fontWeight: "bold" }}>Wind Speed (m/s)</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {forecast.map((day) => (
                    <TableRow key={day.date}>
                      <TableCell align="center">
                        <Typography variant="subtitle1">{day.date}</Typography>
                      </TableCell>
                      <TableCell align="center">
                        <Card
                          className="forecast-card"
                          sx={{
                            background: getWeatherGradient(day.weather_main),
                            color: "white",
                            borderRadius: "12px",
                            boxShadow: 2,
                            padding: 1,
                            minWidth: "120px",
                            display: "flex",
                            flexDirection: "column",
                            alignItems: "center",
                            justifyContent: "center",
                          }}
                        >
                          {weatherIcons[day.weather_main] || <Cloud fontSize="large" />}
                          <Typography variant="body2">{day.weather_description}</Typography>
                        </Card>
                      </TableCell>
                      <TableCell align="center">
                        {day.temperature_min}°C - {day.temperature_max}°C
                      </TableCell>
                      <TableCell align="center">{day.uv_index_max}</TableCell>
                      <TableCell align="center">{day.precipitation_probability_max}%</TableCell>
                      <TableCell align="center">{day.wind_speed_max} m/s</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
          </>
        ) : (
          <>
            <Typography variant="h6" className="welcome-title">Login to search for weather</Typography>
          </>
        )
        
      }
      
    </Box>
  );
};

export default WeatherResults;
