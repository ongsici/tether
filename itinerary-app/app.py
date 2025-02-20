from fastapi import FastAPI
import ollama
import requests
import json
import uvicorn

app = FastAPI()

# OLLAMA_HOST = "http://0.0.0.0:11434"
OLLAMA_HOST = "http://host.docker.internal:11434"  # Change 0.0.0.0 to host.docker.internal


@app.get("/")
def get_ollama_response():
    # return {"message": "Server is working!"}
    city = "Sydney"
    start_date = "2025-02-18"
    end_date = "2025-02-21"
    weather = "sunny"
    interests = None

    prompt = f"""
    Suggest 10 activities to do for a trip to {city} from {start_date} to {end_date},
    given that the weather forecast is {weather} with a temperature of {20}°C.    
    Some of my interests include: {interests}.
    Please only output activities in a json format. An example of the format is:
    {{
        "activities": [
            {{
            "price": 0,
            "activity_name": "Hiking",
            "location": "Mountain Trail",
            "description": "A challenging yet scenic hike through rugged terrain offering breathtaking views of the valley."
            }},
            {{
            "price": 80,
            "activity_name": "Cooking Class",
            "location": "Culinary Studio",
            "description": "A hands-on class where participants learn to cook a variety of dishes from professional chefs."
            }},
            {{
            "price": 50,
            "activity_name": "Museum Tour",
            "location": "City Museum",
            "description": "An educational tour exploring art, history, and culture through curated exhibits."
            }}
        ]
        }}
        Do NOT return any additional text besides these relevant fields.
        As for the price of these activities, please return all the values as Euros (EUR).
    """
        

    response_text = ""

    # Format the message correctly
    messages = [{"role": "user", "content": prompt}]

    client = ollama.Client(host=OLLAMA_HOST)

    # Stream the response
    for chunk in client.chat(model="llama3.2", messages=messages, stream=True):
        if hasattr(chunk, "message") and hasattr(chunk.message, "content"):  # Ensure correct access
            response_text += chunk["message"]["content"]

    # Check if the response is empty
    if not response_text.strip():
        print("Error: Empty response received from Ollama.")
        return None

    # Parse the response as JSON
    try:
        response_json = json.loads(response_text)
        print(response_json)
        return response_json
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print("Raw response:", response_text)  # Debugging output
        return None

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)