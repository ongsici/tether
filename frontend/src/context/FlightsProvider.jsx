import React, { createContext, useContext, useState, useEffect } from "react";

// Create Context
const FlightContext = createContext();

// Custom Hook
export const useFlights = () => useContext(FlightContext);

// Provider Component
export const FlightProvider = ({ children }) => {
    const [flights, setFlights] = useState(() => {
        const savedFlights = localStorage.getItem("flights");
        return savedFlights ? JSON.parse(savedFlights) : [];
    });
    
    useEffect(() => {
        localStorage.setItem("flights", JSON.stringify(flights));
    }, [flights]);
    
    return (
        <FlightContext.Provider value={{ flights, setFlights }}>
        {children}
        </FlightContext.Provider>
    );
};