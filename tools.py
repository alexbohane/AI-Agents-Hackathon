from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool, Tool
import random
import os
from dotenv import load_dotenv
import requests


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

search_tool = DuckDuckGoSearchRun()


@tool
def get_weather_info(location: str) -> str:
    """
    Returns a summary of the current weather in a given location using live search.
    """
    query = f"current weather in {location}"
    results = search_tool.run(query)

    # Return just the top 1–2 sentences of result
    if not results:
        return f"Sorry, I couldn't find the weather for {location}."

    return f"Weather info for {location}: {results[:300]}"


@tool
def search_restaurants(term: str, location: str) -> list:
    """
    Search Google Maps for restaurants or other venues using a keyword and a location.
    Returns a list of the top 3 results with name, rating, address, and place_id for follow-up lookups.
    """
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{term} in {location}",
        "radius": 5000,
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return [{"error": f"API error {response.status_code}"}]

    data = response.json()
    structured_results = []

    for place in data.get("results", [])[:5]:
        structured_results.append({
            "name": place["name"],
            "rating": place.get("rating", None),
            "address": place.get("formatted_address", "N/A"),
            "place_id": place["place_id"]
        })

    return structured_results

@tool
def get_restaurant_details(place_id: str) -> dict:
    """
    Fetches detailed information about a place using its Google Maps place_id.
    Returns phone number, opening hours, and website if available.
    """
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_phone_number,website,opening_hours",
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {"error": f"API error {response.status_code}"}

    data = response.json().get("result", {})
    return {
        "name": data.get("name"),
        "phone": data.get("formatted_phone_number", "N/A"),
        "website": data.get("website", "N/A"),
        "hours": data.get("opening_hours", {}).get("weekday_text", [])
    }