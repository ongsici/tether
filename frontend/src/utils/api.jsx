const APIM_URL="https://tether-apim-2.azure-api.net/api/submitData";
const APIM_SAVE_URL="http://localhost:8000/api/saveData";

const subscriptionKey = process.env.APIM_SUBSCRIPTION_KEY;

export const searchTravel = async (requestBody) => {
    try {
      const response = await fetch(`${APIM_URL}`, {
        method: "POST",
        headers: { "Content-Type": "application/json",
                  "Ocp-Apim-Subscription-Key": subscriptionKey
        },
        body: JSON.stringify(requestBody),
      });
  
      if (!response.ok) {
        throw new Error("Failed to fetch travel results");
      }
  
      return await response.json();
    } catch (error) {
      console.error("API Error:", error);
      return null;
    }

  };

export const saveFlight = async (requestBody) => {
    try {
      const response = await fetch(`${APIM_SAVE_URL}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      });
      if (!response.ok) {
        throw new Error("Failed to save flight");
      }
      return { success: true, message: "Flight saved successfully!" };
    } catch (error) {
      console.error("Error saving flight:", error);
      return { success: false, message: "Error saving flight." };
    }
  };
  
