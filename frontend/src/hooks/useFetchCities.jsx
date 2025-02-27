import { useEffect, useState } from "react";

const useFetchCities = () => {
    const [cities, setCities] = useState([]);
  
    useEffect(() => {
      fetch("/cities.json")
        .then((response) => response.json())
        .then((data) => {
          setCities(data);
        })
        .catch((error) => console.error("Error fetching cities:", error));
    }, []);
  
    return cities;
  };
  
export default useFetchCities;