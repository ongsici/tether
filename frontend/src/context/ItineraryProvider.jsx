import React, { createContext, useContext, useState, useEffect } from "react";

// Create Context
const ItineraryContext = createContext();

// Custom Hook
export const useItinerary = () => useContext(ItineraryContext);

// Provider Component
export const ItineraryProvider = ({ children }) => {
  const [itinerary, setItinerary] = useState(() => {
    const savedItinerary = localStorage.getItem("itinerary");
    return savedItinerary ? JSON.parse(savedItinerary) : [];
  });

  useEffect(() => {
    localStorage.setItem("itinerary", JSON.stringify(itinerary));
  }, [itinerary]);

  return (
    <ItineraryContext.Provider value={{ itinerary, setItinerary }}>
      {children}
    </ItineraryContext.Provider>
  );
};
