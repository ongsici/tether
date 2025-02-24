import React from "react";
import { useLocation } from "react-router-dom";
import { Box, Card, CardContent, Typography, Grid } from "@mui/material";
import { WbSunny, Cloud, Thunderstorm, AcUnit, BeachAccess } from "@mui/icons-material";
import "./Weather.css";

const weatherIcons = {
    Clear: <WbSunny />,
    Clouds: <Cloud />,
    Rain: <Thunderstorm />,
    Snow: <AcUnit />,
    Drizzle: <BeachAccess />,
  };

const WeatherResults = () => {
  const { state } = useLocation();
  const data = state?.weatherData;

  if (!data || !data.results) {
    return <Typography>No weather data available</Typography>;
  }

  const { current, forecast } = data.results;

  return (
    <Box className="results-container">
      <div className="background-overlay"></div>

      {/* Current Weather */}
      <Card className="weather-card">
        <CardContent>
          <Typography variant="h5" gutterBottom>
            Current Weather in {current.city}, {current.country_code}
          </Typography>
          <Grid container alignItems="center" spacing={2}>
            <Grid item>
              {weatherIcons[current.weather_main] || <Cloud />} {/* Default icon if no match */}
            </Grid>
            <Grid item>
              <Typography variant="h6">{current.weather_main}</Typography>
              <Typography variant="body1">{current.weather_description}</Typography>
            </Grid>
          </Grid>
          <Typography variant="body2">Temperature: {current.temperature}°C</Typography>
          <Typography variant="body2">Feels Like: {current.feels_like}°C</Typography>
          <Typography variant="body2">Humidity: {current.humidity}%</Typography>
          <Typography variant="body2">Wind Speed: {current.wind_speed} m/s</Typography>
        </CardContent>
      </Card>

      {/* Forecast Grid */}
      <Typography variant="h6" gutterBottom>
        6-Day Forecast
      </Typography>
      <Grid container spacing={2}>
        {forecast.map((day) => (
          <Grid item xs={12} sm={6} md={4} key={day.date}>
            <Card className="forecast-card">
              <CardContent>
                <Grid container alignItems="center" spacing={1}>
                  <Grid item>
                    {weatherIcons[day.weather_main] || <Cloud />}
                  </Grid>
                  <Grid item xs>
                    <Typography variant="subtitle1">{day.date}</Typography>
                    <Typography variant="body2">{day.weather_description}</Typography>
                  </Grid>
                </Grid>
                <Typography variant="body2">
                  Temp: {day.temperature_min}°C - {day.temperature_max}°C
                </Typography>
                <Typography variant="body2">UV Index: {day.uv_index_max}</Typography>
                <Typography variant="body2">
                  Precipitation: {day.precipitation_probability_max}%
                </Typography>
                <Typography variant="body2">Wind: {day.wind_speed_max} m/s</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default WeatherResults;
