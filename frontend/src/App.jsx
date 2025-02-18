import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import ResponsiveAppBar from "./components/ResponsiveAppBar";
import Home from "./pages/Home";
import Flights from "./pages/Flights"; 
import Itinerary from "./pages/Itinerary";  
import Weather from "./pages/Weather";
import Footer from "./components/Footer";


function App() {
  return (
    <Router>
      <ResponsiveAppBar />
      <Routes>
          <Route path="/flights" element={<Flights />} />
          <Route path="/itinerary" element={<Itinerary />} />
          <Route path="/weather" element={<Weather />} />
          <Route path="/" element={<Home />} />
      </Routes>
      <Footer /> {/* Include the Footer component */}
    </Router>

  );
}

export default App;
