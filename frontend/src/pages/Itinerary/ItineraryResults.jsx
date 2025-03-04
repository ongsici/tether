import React, { useState } from "react";
import { Box, Typography, Card, CardMedia, CardContent, Grid, Button, CircularProgress } from "@mui/material";
import Toast from '../../components/Toast';
import AddIcon from '@mui/icons-material/Add';
import { useItinerary } from "../../context/ItineraryProvider";
import { saveIitnerary } from '../../utils/api';
// import useFetchUser from "../../hooks/useFetchUser";
import "./Itinerary.css";

const ItineraryResults = () => {
  // const user = useFetchUser();
  const user = { userId: "abc123" };
  const { itinerary } = useItinerary();
  const [toast, setToast] = useState({ message: '', type: '', visible: false });
  const [buttonLoading, setButtonLoading] = useState({});

  console.log("Received Itinerary Data:", itinerary);

  const handleSaveItinerary = async (activity) => {
    setButtonLoading((prev) => ({ ...prev, [activity.activity_id]: true }));
    const payload = {
      user_id: user.userId,
      itinerary: activity
    }

    console.log("Saving Itinerary:", payload);
    const result = await saveIitnerary(payload);
    setButtonLoading((prev) => ({ ...prev, [activity.activity_id]: false }));
    setToast({
      message: result.message,
      type: result.success ? "success" : "error",
      visible: true,
    });
  }

  return (
    <Box className="itinerary-container">
      <div className="background-overlay"></div>

      {toast.visible && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast({ ...toast, visible: false })}
        />
      )}

      <Typography variant="h4" className="itinerary-title" sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 700, mt: 5 }}>
        Itinerary Suggestions
      </Typography>
      {user ? (
        itinerary && itinerary.length === 0 ? (
          <Typography variant="body1" className="no-activities">
            No activities found.
          </Typography>
        ) : (
          <div className="results-box">
            <Grid container spacing={3} className="activities-grid" sx={{ maxWidth: "100%", margin: "0 auto" }}>
              {itinerary?.map((activity) => (
                <Grid
                  item
                  xs={12}
                  sm={6}
                  md={4}
                  lg={3}
                  key={activity.activity_id}
                  className="activity-card"
                >
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
                      {/* <Typography variant="subtitle1" className="activity-price">
                        Price: {activity.price_amount} {activity.price_currency}
                      </Typography> */}
                    </CardContent>

                    <div className="save-button-container">
                      {buttonLoading[activity.activity_id] ? (
                          <CircularProgress size={24} className="loading-spinner"/> 
                      ) : (
                        <Button
                          variant="contained"
                          className="save-itinerary-button"
                          startIcon={<AddIcon />}
                          onClick={() => handleSaveItinerary(activity)}
                        >
                          Save Itinerary
                        </Button>
                      )
                      }
                      
                    </div>

                  </Card>
                </Grid>
              ))}
            </Grid>
          </div>
        )
      ) : (
        <Typography variant="h6" className="welcome-title">
          Login to view itinerary options
        </Typography>
      )}
    </Box>
  );
};

export default ItineraryResults;
