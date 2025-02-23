import React from 'react';
import { useLocation } from 'react-router-dom';
import { Box, Typography, Table, TableContainer, TableHead, TableRow, TableCell, TableBody, Paper, Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import FlightIcon from '@mui/icons-material/Flight';
import "./Flights.css";

const FlightResults = () => {
  const { state } = useLocation();
  const flights = state?.flightData || []; // This retrieves the data passed in 'state'

  console.log("Received Flight Data:", flights); // Debugging line

  return (
    <Box className="results-container">
    <div className="background-overlay"></div>
      <Typography variant="h5" className="results-box">
        Flight Options
      </Typography>
      {flights.length === 0 ? (
        <Typography variant="body1">No flights found.</Typography>
      ) : (
        <div className="results-box">
          {flights.map((flight, index) => (
            <div key={index} className="flight-container">
              <Box className="flight-summary">
                <Typography variant="h6" className="flight-summary-title">
                <div className="flight-route">
                    <span className="airport-text">{`${flight.FlightResponse.outbound[0].SegmentResponse.departure_airport}`}</span>
                    <div className="route-line">
                    <FlightIcon className="flight-icon" />
                    </div>
                    <span className="airport-text">{flight.FlightResponse.outbound[0].SegmentResponse.destination_airport}</span>
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
                    <span className="airport-text">{`${flight.FlightResponse.inbound[0].SegmentResponse.departure_airport}`}</span>
                    <div className="route-line">
                    <FlightIcon className="flight-icon" />
                    </div>
                    <span className="airport-text">{flight.FlightResponse.inbound[0].SegmentResponse.destination_airport}</span>
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
            </div>
          ))}
        </div>
      )}
    </Box>
  );
};

export default FlightResults;
