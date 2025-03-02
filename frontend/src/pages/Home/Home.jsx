import { Box, Container, Grid, Card, CardContent, Typography, CardActionArea } from "@mui/material";
import { FlightTakeoff, Map, WbSunny } from "@mui/icons-material";
import { Link } from "react-router-dom";
import "./Home.css";

function Home() {
  return (
    <Container maxWidth="md" sx={{ mt: 6, textAlign: "center" }} className="home-container">
      <div className="background-overlay"></div>
      <Box className="content-box">

        <Grid container spacing={4} justifyContent="center" className="home-card-page">
          {/* Flight Card */}
          <Grid item xs={12} sm={4}>
            <Card className="home-card">
              <CardActionArea component={Link} to="/flights">
                <CardContent sx={{ textAlign: "center" }}>
                  <FlightTakeoff sx={{ fontSize: 50, color: "#023641" }} />
                  <Typography variant="h5" sx={{ mt: 2, fontFamily: 'Roboto, sans-serif' }}>
                    Flight Search
                  </Typography>
                  <Typography variant="body2" className="description-text" sx={{ mt: 1 }}>
                    Find the best flights to your desired destinations.
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>

          {/* Itinerary Card */}
          <Grid item xs={12} sm={4}>
            <Card className="home-card">
              <CardActionArea component={Link} to="/itinerary">
                <CardContent sx={{ textAlign: "center" }}>
                  <Map sx={{ fontSize: 50, color: "#023641" }} />
                  <Typography variant="h5" sx={{ mt: 2 }}>
                    Itinerary Planner
                  </Typography>
                  <Typography variant="body2" className="description-text" sx={{ mt: 1 }}>
                    Plan your trip with our easy-to-use itinerary tool.
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>

          {/* Weather Card */}
          <Grid item xs={12} sm={4}>
            <Card className="home-card">
              <CardActionArea component={Link} to="/weather">
                <CardContent sx={{ textAlign: "center" }}>
                  <WbSunny sx={{ fontSize: 50, color: "#023641;" }} />
                  <Typography variant="h5" sx={{ mt: 2 }}>
                    Weather Forecast
                  </Typography>
                  <Typography variant="body2" className="description-text" sx={{ mt: 1 }}>
                    Get real-time weather updates for your travel destination.
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
}

export default Home;

