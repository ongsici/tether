const APIM_URL="https://tether-apim-2.azure-api.net/api/submitData";
const APIM_SAVE_URL="https://tether-apim-2.azure-api.net/api/saveData";
const APIM_RETRIEVE_URL="https://tether-apim-2.azure-api.net/api/retrieveData";
const APIM_REMOVE_URL="https://tether-apim-2.azure-api.net/api/removeData"
// const APIM_URL="http://localhost:8000/api/submitData"
// const APIM_SAVE_URL="http://localhost:8000/api/saveData";
// const APIM_RETRIEVE_URL="http://localhost:8000/api/retrieveData"
// const APIM_REMOVE_URL="http://localhost:8000/api/removeData"

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

      const responseData = await response.json();
      if (responseData.user_id !== requestBody.user_id) {
        return { success: false, message: "User ID mismatch." };
      }

      return {
        success: true,
        status: responseData.status,
        message: responseData.message,
      };
    } catch (error) {
      console.error("Error saving flight:", error);
      return { success: false, message: "Error saving flight." };
    }
  };

export const saveIitnerary = async (requestBody) => {
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
      throw new Error("Failed to save itinerary");
    }

    const responseData = await response.json();
    if (responseData.user_id !== requestBody.user_id) {
      return { success: false, message: "User ID mismatch." };
    }

    return {
      success: true,
      status: responseData.status,
      message: responseData.message,
    };
  } catch (error) {
    console.error("Error saving itinerary:", error);
    return { success: false, message: "Error saving itinerary." };
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

    const responseData = await response.json();

    if (responseData.user_id !== requestBody.user_id) {
      return { success: false, message: "User ID mismatch." };
    }

    return {
      success: true,
      status: responseData.status,
      message: responseData.message,
    };

  } catch (error) {
    console.error("Error removing flight:", error);
    return { success: false, message: "Error removing flight." };
  }
};


export const removeItinerary = async (requestBody) => {
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
      throw new Error("Failed to remove itinerary");
    }

    const responseData = await response.json();

    if (responseData.user_id !== requestBody.user_id) {
      return { success: false, message: "User ID mismatch." };
    }

    return {
      success: true,
      status: responseData.status,
      message: responseData.message,
    };
  } catch (error) {
    console.error("Error removing itinerary:", error);
    return { success: false, message: "Error removing itinerary." };
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