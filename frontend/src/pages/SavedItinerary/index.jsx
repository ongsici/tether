import React, { useState, useEffect } from "react";
import { Box, Typography, Card, CardMedia, CardContent, Grid, CircularProgress } from "@mui/material";
// import useFetchUser from "../../hooks/useFetchUser";
import { getSavedDetails } from "../../utils/api";
import "./SavedItinerary.css";

function SavedItinerary() {
    // const user = useFetchUser();
    const user = { userId: "abc123"};
    const [savedItinerary, setSavedItinerary] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const fetchItinerary = async () => {
            setLoading(true);
            const requestBody = { 
                user_id: user.userId,
                type: "itinerary"
            };
            const itinerary = await getSavedDetails(requestBody);
            if (itinerary.user_id === user.userId) {
                setSavedItinerary(itinerary.results);
                } else {
                setSavedItinerary([]); 
                }
            setLoading(false);
        };

        fetchItinerary();
    }, [user.userId]);

    if (loading) {
        return (
          <>
          <div className="background-overlay"></div>
          <div className="overlay"></div>
          <div className="loader-container">
            
              <CircularProgress sx={{ color: '#023641', mb: 2 }} />
              <Typography variant="h6" className="loading-text">
                Just a moment, we're retrieving your saved itinerary!
              </Typography>
    
          </div>
          </>
        );
      }

    return (
        <Box className="itinerary-container">
          <div className="background-overlay"></div>
          <Typography variant="h4" className="itinerary-title" sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 700, mt: 5 }}>
            Saved Itinerary
          </Typography>
          {savedItinerary && savedItinerary.length === 0 ? (
            <Typography variant="body1" className="no-activities">
              No saved itinerary found.
            </Typography>
          ) : (
            <Grid container spacing={3} className="activities-grid">
              {savedItinerary?.map((activity) => (
                <Grid item xs={12} sm={6} md={4} key={activity.activity_id} className="activity-card">
                  <Card className="card">
                      <CardMedia
                        component="img"
                        height="200"
                        image={activity.pictures}
                        alt={activity.activity_name}
                        className="activity-image"
                      />
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



export default SavedItinerary;

