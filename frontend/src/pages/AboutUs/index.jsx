import React from 'react';
import { Box, Typography, Container, Button, Card, CardContent } from '@mui/material';
import { Link } from 'react-router-dom';
import './AboutUs.css';

const AboutUs = () => {
  return (
    <Box className="about-us-container">
      <div className="background-overlay"></div>

      <Container>
        <Typography variant="h2" className="about-us-title" sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 700, textAlign: 'center', marginBottom: 4, marginTop: 8, color: '#023641' }}>
          About Us
        </Typography>
        <Card className="about-us-card" sx={{ borderRadius: 6, padding: 2, backgroundColor: "rgba(255, 255, 255, 0.6)", borderTop: "6px solid #023641" }}>
          <CardContent className="about-us-card-content">
            <Typography variant="body1" className="about-us-description">
              Welcome to our app, your all-in-one travel companion! Inspired by our love for exploring new places, we created Tether — short for "Travel Together." 
              More than just a name, Tether represents our mission to connect you, the traveler, to destinations worldwide, making trip planning seamless and more enjoyable.
              
              We help you plan seamless trips with three core services:
              <ul>
                <li><strong>Flight Search:</strong> Easily find return flights between cities with flexible dates.</li>
                <li><strong>Itinerary Discovery:</strong> Discover recommended places to visit in your chosen destination.</li>
                <li><strong>Weather Forecast:</strong> Stay up-to-date with current weather information and a 6-day forecast for your travel locations.</li>
              </ul>
              Our goal is to make your travel experience stress-free and enjoyable by providing all the essentials in one platform. 
              You can also save your flight and itinerary details for easy access later, making your trip planning effortless. 
              Let us assist you in planning your next adventure!
            </Typography>
          </CardContent>
        </Card>

        <Box className="cta-container" sx={{ textAlign: 'center', marginTop: 5 }}>
          <Link to="/">
            <Button variant="contained" className="cta-button" sx={{ backgroundColor: '#023641' }}>
              Start Your Journey Now!
            </Button>
          </Link>
        </Box>
      </Container>
    </Box>
  );
};

export default AboutUs;
