import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import ResponsiveAppBar from "./components/ResponsiveAppBar";
import Home from "./pages/Home";
import Flights from "./pages/Flights"; 


function App() {
  return (
    <Router>
      <ResponsiveAppBar />
      <Routes>
          <Route path="/flights" element={<Flights />} />
          <Route path="/" element={<Home />} />
      </Routes>
    </Router>

  );
}

export default App;
