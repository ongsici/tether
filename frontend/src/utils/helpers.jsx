
export const getTodayDate = () => {
    const today = new Date();
    return today.toISOString().split("T")[0];  
  };

export const getAirportOptions = (inputValue, cities) => {
  const query = (typeof inputValue === 'string' ? inputValue : '').toLowerCase();

  const matchingCities = cities.filter((city) =>
    city.city.toLowerCase().includes(query)
  );
  
  return matchingCities.flatMap((city) =>
    city.airports.map((airport, index) => ({
      city: city.city,
      country: city.country,
      airportCode: airport,
      airportName: city.airport_names[index],
      fullLabel: `${airport} (${city.city}, ${city.country})`,
    }))
  );
};