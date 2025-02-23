import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import ResponsiveAppBar from "./components/ResponsiveAppBar";
import AboutUs from "./pages/AboutUs";
import Home from "./pages/Home/Home";
import HomeResults from "./pages/Home/HomeResults";
import FlightSearch from "./pages/Flights/FlightSearch"; 
import FlightResults from "./pages/Flights/FlightResults";
import Itinerary from "./pages/Itinerary";  
import Weather from "./pages/Weather";
import Footer from "./components/Footer";
import Dashboard from "./pages/Dashboard";


function App() {
  return (
    <Router>
      <ResponsiveAppBar />
      <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/results" element={<HomeResults />} />
          <Route path="/about" element={<AboutUs />} />
          <Route path="/flights" element={<FlightSearch />} />
          <Route path="/flights/results" element={<FlightResults />} />
          <Route path="/itinerary" element={<Itinerary />} />
          <Route path="/weather" element={<Weather />} />
          <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
      <Footer /> {/* Include the Footer component */}
    </Router>

  );
}

export default App;
