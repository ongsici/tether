// const APIM_URL="https://tether-apim-2.azure-api.net/api/submitData";
const APIM_URL="http://localhost:8000/api/submitData"
const APIM_SAVE_URL="http://localhost:8000/api/saveData";
const APIM_RETRIEVE_URL="http://localhost:8000/api/retrieveData"
const APIM_REMOVE_URL="http://localhost:8000/api/removeData"

const subscriptionKey = process.env.REACT_APP_APIM_SUBSCRIPTION_KEY;

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
          "Ocp-Apim-Subscription-Key": subscriptionKey
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


export const removeFlight = async (requestBody) => {
  try {
    const response = await fetch(`${APIM_REMOVE_URL}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscriptionKey
      },
      body: JSON.stringify(requestBody),
    });
    if (!response.ok) {
      throw new Error("Failed to remove flight");
    }
    return { success: true, message: "Flight removed successfully!" };
  } catch (error) {
    console.error("Error removing flight:", error);
    return { success: false, message: "Error removing flight." };
  }
};
  
export const getSavedDetails = async (requestBody) => {

  try {
    const response = await fetch (`${APIM_RETRIEVE_URL}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": subscriptionKey
      },
      body: JSON.stringify(requestBody),
    });
    if (!response.ok) {
      throw new Error("Failed to retrieve saved details");
    }
    return await response.json();
  } catch (error) {
    console.error("Error retrieving saved details: ", error);
    return null;
  }
}