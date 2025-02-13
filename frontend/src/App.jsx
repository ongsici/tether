import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// import Layout from "./components/Layout";
import ResponsiveAppBar from "./components/ResponsiveAppBar";
import Home from "./pages/Home";


function App() {
  return (
    <Router>
      <ResponsiveAppBar />
      <Routes>
          <Route path="/" element={<Home />} />
      </Routes>
    </Router>

  );
}

export default App;
