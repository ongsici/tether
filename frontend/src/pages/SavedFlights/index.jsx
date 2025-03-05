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
  Button,
} from "@mui/material";
import RemoveCircleOutlineIcon from '@mui/icons-material/RemoveCircleOutline';
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import FlightIcon from "@mui/icons-material/Flight";
import { Tooltip, IconButton } from "@mui/material";
import InfoOutlinedIcon from "@mui/icons-material/InfoOutlined";
import useFetchUser from "../../hooks/useFetchUser";
import { getSavedDetails, removeFlight } from "../../utils/api";
import Toast from '../../components/Toast';
import "./SavedFlights.css";

function SavedFlights() {
  const user = useFetchUser();
  // const user = { userId: "abc123"};
  const [savedFlights, setSavedFlights] = useState([]);
  const [loading, setLoading] = useState(false);
  const [buttonLoading, setButtonLoading] = useState(false);
  const [toast, setToast] = useState({ message: '', type: '', visible: false });

  useEffect(() => {
    const fetchFlights = async () => {
        setLoading(true);
        const userId = user.userId;
        const params = `user_id=${userId}&type=flights`;

        try {
          const flights = await getSavedDetails(params);
          if (flights.user_id === userId) {
            setSavedFlights(flights.flights);
          } else {
            setSavedFlights([]);
          }
        } catch (error) {
          console.error("Error fetching flights:", error);
          setSavedFlights([]); // In case of error, set to empty array
        }
        setLoading(false);
      };

    fetchFlights();
}, [user]); 

  const handleRemoveFlight = async (flight_id) => {
    setButtonLoading(true);
    const payload = {
      user_id: user.userId,
      flight_id: flight_id
    }
    console.log("Removing Flight:", payload);
    const result = await removeFlight(payload);
    setButtonLoading(false);
    setToast({
      message: result.message,
      type: result.success ? "success" : "error",
      visible: true,
    });
    
    if (result.success){
      setSavedFlights((prevFlight) => prevFlight.filter(flight => flight.FlightResponse.flight_id !== flight_id));
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
            Just a moment, we're retrieving your saved flights!
          </Typography>

      </div>
      </>
    );
  }

  return (
    <Container className="home-container">
      <div className="background-overlay"></div>

      {toast.visible && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast({ ...toast, visible: false })}
        />
      )}

      <Box className="content-box">
        <Typography variant="h4" className="results-header" sx={{ fontFamily: 'Roboto, sans-serif', fontWeight: 700, mt: 5}}>
          Saved Flights
        </Typography>
      {user ? (
        savedFlights && savedFlights.length === 0 ? (
          <Typography variant="body1">No saved flights found.</Typography>
        ) : (
          <div className="results-box">
            {savedFlights.map((flight, index) => (
              <div key={index} className="flight-container">
                <Box className="flight-summary">
                  <Typography variant="h6" className="flight-summary-title">
                  <div className="flight-route">
                    {flight.FlightResponse.outbound.map((segment, idx, arr) => (
                      <React.Fragment key={idx}>
                        <div className="segment">
                          <span className="airport-text">
                            {`${segment.SegmentResponse.departure_airport} ${segment.SegmentResponse.departure_time}`}
                          </span>
                          <Typography variant="body2" className="city-text" sx = {{ fontWeight: 500, color: '#023641' }}>
                            {segment.SegmentResponse.departure_city}
                          </Typography>
                        </div>
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
                    <div className="segment">
                      <span className="airport-text">
                        {`${flight.FlightResponse.outbound[flight.FlightResponse.outbound.length - 1].SegmentResponse.destination_airport} ${flight.FlightResponse.outbound[flight.FlightResponse.outbound.length - 1].SegmentResponse.arrival_time}`}
                      </span>
                      <Typography variant="body2" className="city-text" sx = {{ fontWeight: 500, color: '#023641' }}>
                        {flight.FlightResponse.outbound[flight.FlightResponse.outbound.length - 1].SegmentResponse.destination_city}
                      </Typography>
                    </div>
                  </div>
                  </Typography>

                  <Typography variant="body2" className="flight-details">
                  <Tooltip 
                      title="Total price for the round-trip flight" 
                      PopperProps={{
                        modifiers: [
                          {
                            name: 'offset',
                            options: {
                              offset: [0, 5], // Adjust offset to position the tooltip appropriately
                            },
                          },
                        ],
                      }} 
                      placement="top" 
                    >
                      <IconButton size="small" >
                        <InfoOutlinedIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                    {`Total Price: €${flight.FlightResponse.total_price}`}
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
                        <div className="segment">
                          <span className="airport-text">
                            {`${segment.SegmentResponse.departure_airport} ${segment.SegmentResponse.departure_time}`}
                          </span>
                          <Typography variant="body2" className="city-text" sx = {{ fontWeight: 500, color: '#023641' }}>
                            {segment.SegmentResponse.departure_city}
                          </Typography>
                        </div>
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
                    <div className="segment">
                      <span className="airport-text">
                        {`${flight.FlightResponse.inbound[flight.FlightResponse.inbound.length - 1].SegmentResponse.destination_airport} ${flight.FlightResponse.inbound[flight.FlightResponse.inbound.length - 1].SegmentResponse.arrival_time}`}
                      </span>
                      <Typography variant="body2" className="city-text" sx = {{ fontWeight: 500, color: '#023641' }}>
                        {flight.FlightResponse.inbound[flight.FlightResponse.inbound.length - 1].SegmentResponse.destination_city}
                      </Typography>
                    </div>
                  </div>
                  </Typography>
                  {/* <Typography variant="body2" className="flight-details">
                    {`Duration: ${flight.FlightResponse.inbound[0].SegmentResponse.duration}`}
                  </Typography> */}
                  {/* <Typography variant="body2" className="flight-details">
                    {`Passengers: ${flight.FlightResponse.inbound[0].SegmentResponse.num_passengers}`}
                  </Typography> */}
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

                <div className="save-flight-button-container">
                  {buttonLoading ? (
                    <CircularProgress size={24} className="loading-spinner"/> 
                  ) : (
                  <Button
                    variant="contained"
                    className="save-flight-button"
                    startIcon={<RemoveCircleOutlineIcon />}
                    onClick={() => handleRemoveFlight(flight.FlightResponse.flight_id)}
                  >
                    Remove Flight
                  </Button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )
      ) : (
        <>
          <Typography variant="h6" className="welcome-title">Login to view saved flights</Typography>
        </>
      )}
      </Box>
    </Container>
  );
}

export default SavedFlights;
