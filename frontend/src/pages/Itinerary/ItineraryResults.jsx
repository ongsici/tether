import React from "react";
import { useLocation } from "react-router-dom";
import {  Box, Typography, Card, CardMedia, CardContent, Grid } from "@mui/material";
import "./Itinerary.css";

const ItineraryResults = () => {
  const { state } = useLocation();
  const itinerary = state?.itineraryData || [];

  console.log("Received Itinerary Data:", itinerary);

  return (
    <Box className="itinerary-container">
    <div className="background-overlay"></div>
        <Typography variant="h4" className="itinerary-title" sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 700, mt: 5}}>
            Itinerary Suggestions
        </Typography>
      {itinerary.length === 0 ? (
        <Typography variant="body1" className="no-activities">
          No activities found.
        </Typography>
      ) : (
        <Grid container spacing={3} className="activities-grid">
          {itinerary.map((activity) => (
            <Grid item xs={12} sm={6} md={4} key={activity.activity_id} className="activity-card">
              <Card className="card">
                {activity.pictures?.length > 0 && (
                  <CardMedia
                    component="img"
                    height="200"
                    image={activity.pictures[0]}
                    alt={activity.activity_name}
                    className="activity-image"
                  />
                )}
                <CardContent className="card-content">
                  <Typography variant="h6" className="activity-name">
                    {activity.activity_name}
                  </Typography>
                  <Typography variant="body2" className="activity-details">
                    {activity.activity_details}
                  </Typography>
                  <Typography variant="subtitle1" className="activity-price">
                    Price: {activity.price_amount} {activity.price_currency}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};

export default ItineraryResults;
