import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ItineraryProvider } from "./context/ItineraryProvider";
import { FlightProvider } from "./context/FlightsProvider";
import ResponsiveAppBar from "./components/ResponsiveAppBar";
import AboutUs from "./pages/AboutUs";
import Home from "./pages/Home/Home";
import FlightSearch from "./pages/Flights/FlightSearch"; 
import FlightResults from "./pages/Flights/FlightResults";
import Itinerary from "./pages/Itinerary/ItinerarySearch";  
import ItineraryResults from "./pages/Itinerary/ItineraryResults";
import Weather from "./pages/Weather/WeatherSearch";
import WeatherResults from "./pages/Weather/WeatherResults";
import Footer from "./components/Footer";
import SavedFlights from "./pages/SavedFlights"
import SavedItinerary from "./pages/SavedItinerary";


function App() {
  return (
    <FlightProvider>
    <ItineraryProvider>
      <Router>
        <ResponsiveAppBar />
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<AboutUs />} />
            <Route path="/flights" element={<FlightSearch />} />
            <Route path="/flights/results" element={<FlightResults />} />
            <Route path="/itinerary" element={<Itinerary />} />
            <Route path="/itinerary/results" element={<ItineraryResults />} />
            <Route path="/weather" element={<Weather />} />
            <Route path="/weather/results" element={<WeatherResults />} />
            <Route path="/savedflights" element={<SavedFlights />} />
            <Route path="/saveditinerary" element={<SavedItinerary />} />
        </Routes>
        <Footer /> {/* Include the Footer component */}
      </Router>
    </ItineraryProvider>
    </FlightProvider>

  );
}

export default App;
