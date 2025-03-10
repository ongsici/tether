import React, { useState, useEffect } from "react";
import { Box, Typography, Card, CardMedia, CardContent, Grid, CircularProgress, Button, } from "@mui/material";
import RemoveCircleOutlineIcon from '@mui/icons-material/RemoveCircleOutline';
import useFetchUser from "../../hooks/useFetchUser";
import { getSavedDetails, removeItinerary } from "../../utils/api";
import Toast from '../../components/Toast';
import "./SavedItinerary.css";

function SavedItinerary() {
    const user = useFetchUser();
    // const user = { userId: "abc123"};
    const [savedItinerary, setSavedItinerary] = useState([]);
    const [loading, setLoading] = useState(false);
    const [buttonLoading, setButtonLoading] = useState(false);
    const [toast, setToast] = useState({ message: '', type: '', visible: false });

    useEffect(() => {
        const fetchItinerary = async () => {
            setLoading(true);
            const userId = user.userId;
            const params = `user_id=${userId}&type=itinerary`;

            try{
              const itinerary = await getSavedDetails(params);
              if (itinerary.user_id === user.userId) {
                setSavedItinerary(itinerary.itinerary);
                } else {
                setSavedItinerary([]); 
                }
            } catch (error){
              console.log("Error fetching itinerary: ", error);
              setSavedItinerary([]); 
            }
            setLoading(false);
        };

        fetchItinerary();
    }, [user]);

    const handleRemoveItinerary = async (activity_id) => {
        setButtonLoading(true);
        const payload = {
          user_id: user.userId,
          activity_id: activity_id
        }
        console.log("Removing Itinerary:", payload);
        const result = await removeItinerary(payload);
        setButtonLoading(false);
        setToast({
          message: result.message,
          type: result.success ? "success" : "error",
          visible: true,
        });
        if (result.success){
          setSavedItinerary((prevItinerary) => prevItinerary.filter(activity => activity.activity_id !== activity_id));
        }
      }

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
        <Box className="itinerary-container" sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '80vh' }}>
          <div className="background-overlay"></div>

          {toast.visible && (
            <Toast
              message={toast.message}
              type={toast.type}
              onClose={() => setToast({ ...toast, visible: false })}
            />
          )}

          <Typography variant="h4" className="itinerary-title" sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 700, mt: 5 }}>
            Saved Itinerary
          </Typography>
          {user ? (
          savedItinerary && savedItinerary.length === 0 ? (
            <Typography variant="body1" className="no-activities">
              No saved itinerary found.
            </Typography>
          ) : (
            <div className="results-box">
            <Grid container spacing={3} className="activities-grid">
              {savedItinerary?.map((activity) => (
                <Grid item xs={12} sm={6} md={4} lg={3} key={activity.activity_id} className="activity-card">
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
                      <Typography variant="h7" className="activity-details" >
                        {activity.city}
                      </Typography>
                      <Typography variant="body2" className="activity-details" sx={{ mt: 2 }}>
                        {activity.activity_details}
                      </Typography>
                      {/* <Typography variant="subtitle1" className="activity-price">
                        Price: {activity.price_amount} {activity.price_currency}
                      </Typography> */}
                    </CardContent>
                    
                    <div className="save-button-container">
                      {buttonLoading ? (
                          <CircularProgress size={24} className="loading-spinner"/> 
                        ) : (
                        <Button
                          variant="contained"
                          className="save-itinerary-button"
                          startIcon={<RemoveCircleOutlineIcon />}
                          onClick={() => handleRemoveItinerary(activity.activity_id)}
                        >
                          Remove Itinerary
                        </Button>
                      )}
                    </div>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </div>
          )) : (
            <Typography variant="h6" className="welcome-title">
              Login to view saved itinerary
            </Typography>
          )}
        </Box>
      );
    };



export default SavedItinerary;

