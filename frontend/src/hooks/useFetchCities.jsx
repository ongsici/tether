import { useEffect, useState } from "react";

const useFetchCities = (url) => {
    const [cities, setCities] = useState([]);
  
    useEffect(() => {
      if (!url) return; 
  
      fetch(url)
        .then((response) => response.json())
        .then((data) => setCities(data))
        .catch((error) => console.error("Error fetching cities:", error));
    }, [url]); 
  
    return cities;
  };
  
export default useFetchCities;