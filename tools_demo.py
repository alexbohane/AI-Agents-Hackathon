from langchain.tools import tool

@tool
def get_weather_info(location: str) -> str:
    """
    Returns a summary of the current weather in a given location using live search.
    """
    # Hardcoded weather for demo purposes
    demo_weather = {
        "Paris": "Weather info for Paris: Currently 23°C with slight clouds and moderate breeze.",
        "Nice": "Weather info for Nice: Sunny and 27°C with clear skies.",
        "Lyon": "Weather info for Lyon: Cloudy and 18°C with occasional showers."
    }

    return demo_weather.get(location, f"Weather info for {location}: 20°C and partly cloudy.")


@tool
def search_restaurants(term: str, location: str) -> list:
    """
    Search for restaurants or other venues using a keyword and a location.
    Returns a list of the top 3 results with name, rating, address, and place_id for follow-up lookups.
    """
    # Hardcoded mock search result
    return [
        {
            "name": "Trattoria Milano",
            "rating": 4.6,
            "address": "12 Rue des Italiens, 75009 Paris",
            "place_id": "demo-italian-1"
        },
        {
            "name": "Sakura Sushi",
            "rating": 4.5,
            "address": "45 Rue Saint-Lazare, 75008 Paris",
            "place_id": "demo-sushi-1"
        },
        {
            "name": "La Table de Paris",
            "rating": 4.3,
            "address": "88 Boulevard Haussmann, 75008 Paris",
            "place_id": "demo-french-1"
        }
    ]


@tool
def get_restaurant_details(place_id: str) -> dict:
    """
    Fetches detailed information about a user's chosen restaurant using a place_id.
    Returns phone number, opening hours, and website if available.
    """
    # Hardcoded mock details
    demo_details = {
        "demo-italian-1": {
            "name": "Trattoria Milano",
            "phone": "+33 1 42 00 00 01",
            "website": "https://trattoriamilano.example.com",
            "hours": [
                "Mon–Fri: 12:00–14:30, 19:00–22:30",
                "Sat–Sun: 12:00–15:00, 19:00–23:00"
            ]
        },
        "demo-sushi-1": {
            "name": "Sakura Sushi",
            "phone": "+33 1 42 00 00 02",
            "website": "https://sakuraparis.example.com",
            "hours": [
                "Every day: 11:30–15:00, 18:00–22:30"
            ]
        },
        "demo-french-1": {
            "name": "La Table de Paris",
            "phone": "+33 1 42 00 00 03",
            "website": "https://latableparis.example.com",
            "hours": [
                "Tue–Sun: 12:00–14:30, 19:00–22:00",
                "Closed Monday"
            ]
        }
    }

    return demo_details.get(place_id, {
        "name": "Unknown",
        "phone": "N/A",
        "website": "N/A",
        "hours": ["Information not available"]
    })
