import React, { useState } from 'react';
import { Box, Typography, Table, TableContainer, TableHead, TableRow, TableCell, TableBody, Paper, Accordion, AccordionSummary, AccordionDetails, Button, CircularProgress} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import FlightIcon from '@mui/icons-material/Flight';
import AddIcon from '@mui/icons-material/Add';
// import useFetchUser from "../../hooks/useFetchUser";
import { saveFlight } from '../../utils/api';
import Toast from '../../components/Toast';
import { useFlights } from '../../context/FlightsProvider';
import "./Flights.css";

const FlightResults = () => {
  // const user = useFetchUser();
  const user = { userId: "abc123" };
  const { flights } = useFlights();
  const [toast, setToast] = useState({ message: '', type: '', visible: false });
  const [buttonLoading, setButtonLoading] = useState(false);

  console.log("Received Flight Data:", flights); // Debugging line

  const handleSaveFlight = async (flight) => {
    setButtonLoading(true);
    const payload = {
      user_id: user.userId,
      flights: flight
    }
    console.log("Saving Flight:", payload);
    const result = await saveFlight(payload);
    setButtonLoading(false);
    setToast({
      message: result.message,
      type: result.success ? "success" : "error",
      visible: true,
    });

  };

  return (
    <Box className="results-container">
    <div className="background-overlay"></div>

      {toast.visible && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast({ ...toast, visible: false })}
        />
      )}

      <Typography variant="h4" className="results-header" sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 700, mt: 5}}>
        Flight Options
      </Typography>
      {user ? (
        flights.length === 0 ? (
          <Typography variant="body1">No flights found.</Typography>
        ) : (
          <div className="results-box">
            {flights.map((flight, index) => (
              <div key={index} className="flight-container">
                <Box className="flight-summary">
                  <Typography variant="h6" className="flight-summary-title">
                  <div className="flight-route">
            
                  {flight.FlightResponse.outbound.map((segment, idx, arr) => (
                    <React.Fragment key={idx}>
                      <span className="airport-text">{segment.SegmentResponse.departure_airport}</span>
                      {idx < arr.length - 1 && ( // Display arrow between segments
                        <div className="route-line">
                          <FlightIcon className="flight-icon" />
                        </div>
                      )}
                    </React.Fragment>
                  ))}
                  {/* Display final destination */}
                  <div className="route-line">
                    <FlightIcon className="flight-icon" />
                  </div>
                  <span className="airport-text">
                    {flight.FlightResponse.outbound[flight.FlightResponse.outbound.length - 1].SegmentResponse.destination_airport}
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
                      {idx < arr.length - 1 && ( // Display arrow between segments
                        <div className="route-line">
                          <FlightIcon className="flight-icon" />
                        </div>
                      )}
                    </React.Fragment>
                  ))}
                  {/* Display final destination */}
                  <div className="route-line">
                    <FlightIcon className="flight-icon" />
                  </div>
                  <span className="airport-text">
                    {flight.FlightResponse.inbound[flight.FlightResponse.inbound.length - 1].SegmentResponse.destination_airport}
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
  
                <div className="save-button-container">
                  {buttonLoading ? (
                    <CircularProgress size={24} className="loading-spinner"/> 
                  ) : (
                    <Button 
                      variant="contained" 
                      className="save-flight-button" 
                      startIcon={<AddIcon />}
                      onClick={() => handleSaveFlight(flight)}>
                      Save Flight
                    </Button>
                  )}
                  
                </div>
  
              </div>
            ))}
          </div>
        )
      ) : (
        <>
          <Typography variant="h6" className="welcome-title">Login to view flight options</Typography>
        </>
      )}
      
    </Box>
  );
};

export default FlightResults;
