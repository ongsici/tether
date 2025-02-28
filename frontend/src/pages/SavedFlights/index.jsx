import React, { useState, useEffect } from "react";
import {
  Typography,
  Box,
  Container,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  // Button,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import FlightIcon from "@mui/icons-material/Flight";
// import useFetchUser from "../../hooks/useFetchUser";
import { getSavedFlights } from "../../utils/api";
import "./SavedFlights.css";

function SavedFlights() {
  // const user = useFetchUser();
  const user = { userId: "abc123"};
  const [savedFlights, setSavedFlights] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchFlights = async () => {
        setLoading(true);
        const requestBody = { user_id: user.userId };
        const flights = await getSavedFlights(requestBody);
        if (flights.user_id === user.userId) {
          setSavedFlights(flights.results);
        } else {
          setSavedFlights([]); 
        }
        setLoading(false);
      };

    fetchFlights();
}, [user.userId]); 

  if (loading) {
    return (
      <>
      <div className="background-overlay"></div>
      <div className="overlay"></div>
      <div className="loader-container">
        
          <CircularProgress sx={{ color: '#023641', mb: 2 }} />
          <Typography variant="h6" className="loading-text">
            Just a moment, we're retrieving your saved flights!
          </Typography>

      </div>
      </>
    );
  }


  return (
    <Container maxWidth="md" sx={{ mt: 6, textAlign: "center" }} className="home-container">
      <div className="background-overlay"></div>
      <Box className="content-box">
        <Typography variant="h4" className="results-header" sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 700, mt: 5}}>
          Saved Flights
        </Typography>
      {user ? (
        savedFlights && savedFlights.length === 0 ? (
          <Typography variant="body1">No flights found.</Typography>
        ) : (
          <div className="results-box">
            {savedFlights.map((flight, index) => (
              <div key={index} className="flight-container">
                <Box className="flight-summary">
                  <Typography variant="h6" className="flight-summary-title">
                    <div className="flight-route">
                      {flight.FlightResponse.outbound.map((segment, idx, arr) => (
                        <React.Fragment key={idx}>
                          <span className="airport-text">{segment.SegmentResponse.departure_airport}</span>
                          {idx < arr.length - 1 && (
                            <div className="route-line">
                              <FlightIcon className="flight-icon" />
                            </div>
                          )}
                        </React.Fragment>
                      ))}
                      <div className="route-line">
                        <FlightIcon className="flight-icon" />
                      </div>
                      <span className="airport-text">
                        {
                          flight.FlightResponse.outbound[
                            flight.FlightResponse.outbound.length - 1
                          ].SegmentResponse.destination_airport
                        }
                      </span>
                    </div>
                  </Typography>
                  <Typography variant="body2" className="flight-details">
                    {`Price: €${flight.FlightResponse.price_per_person}`}
                  </Typography>
                  <Typography variant="body2" className="flight-details">
                    {`Passengers: ${flight.FlightResponse.outbound[0].SegmentResponse.num_passengers}`}
                  </Typography>
                </Box>
                <Accordion className="flight-accordion">
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography>Outbound Flight Details</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <TableContainer component={Paper}>
                      <Table className="results-table">
                        <TableHead>
                          <TableRow>
                            <TableCell>Flight Number</TableCell>
                            <TableCell>Departure</TableCell>
                            <TableCell>Arrival</TableCell>
                            <TableCell>Duration</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {flight.FlightResponse.outbound.map((segment, idx) => (
                            <TableRow key={idx}>
                              <TableCell>{`${segment.SegmentResponse.airline_code} ${segment.SegmentResponse.flight_number}`}</TableCell>
                              <TableCell>{`${segment.SegmentResponse.departure_date} ${segment.SegmentResponse.departure_time}`}</TableCell>
                              <TableCell>{`${segment.SegmentResponse.arrival_date} ${segment.SegmentResponse.arrival_time}`}</TableCell>
                              <TableCell>{segment.SegmentResponse.duration}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </AccordionDetails>
                </Accordion>

                {/* Inbound flight section */}
                <Box className="flight-summary">
                  <Typography variant="h6" className="flight-summary-title">
                    <div className="flight-route">
                      {flight.FlightResponse.inbound.map((segment, idx, arr) => (
                        <React.Fragment key={idx}>
                          <span className="airport-text">{segment.SegmentResponse.departure_airport}</span>
                          {idx < arr.length - 1 && (
                            <div className="route-line">
                              <FlightIcon className="flight-icon" />
                            </div>
                          )}
                        </React.Fragment>
                      ))}
                      <div className="route-line">
                        <FlightIcon className="flight-icon" />
                      </div>
                      <span className="airport-text">
                        {
                          flight.FlightResponse.inbound[
                            flight.FlightResponse.inbound.length - 1
                          ].SegmentResponse.destination_airport
                        }
                      </span>
                    </div>
                  </Typography>
                  <Typography variant="body2" className="flight-details">
                    {`Duration: ${flight.FlightResponse.inbound[0].SegmentResponse.duration}`}
                  </Typography>
                  <Typography variant="body2" className="flight-details">
                    {`Passengers: ${flight.FlightResponse.inbound[0].SegmentResponse.num_passengers}`}
                  </Typography>
                </Box>
                <Accordion className="flight-accordion">
                  <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                    <Typography>Inbound Flight Details</Typography>
                  </AccordionSummary>
                  <AccordionDetails>
                    <TableContainer component={Paper}>
                      <Table className="results-table">
                        <TableHead>
                          <TableRow>
                            <TableCell>Flight Number</TableCell>
                            <TableCell>Departure</TableCell>
                            <TableCell>Arrival</TableCell>
                            <TableCell>Duration</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {flight.FlightResponse.inbound.map((segment, idx) => (
                            <TableRow key={idx}>
                              <TableCell>{`${segment.SegmentResponse.airline_code} ${segment.SegmentResponse.flight_number}`}</TableCell>
                              <TableCell>{`${segment.SegmentResponse.departure_date} ${segment.SegmentResponse.departure_time}`}</TableCell>
                              <TableCell>{`${segment.SegmentResponse.arrival_date} ${segment.SegmentResponse.arrival_time}`}</TableCell>
                              <TableCell>{segment.SegmentResponse.duration}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </TableContainer>
                  </AccordionDetails>
                </Accordion>

                {/* <div className="save-button-container">
                  <Button
                    variant="contained"
                    className="save-flight-button"
                    startIcon={<AddIcon />}
                    onClick={() => handleSaveFlight(flight)}
                  >
                    Save Flight
                  </Button>
                </div> */}
              </div>
            ))}
          </div>
        )
      ) : (
        <>
          <Typography variant="h6" className="welcome-title">Login to retrieve saved flights</Typography>
        </>
      )}
      </Box>
    </Container>
  );
}

export default SavedFlights;
