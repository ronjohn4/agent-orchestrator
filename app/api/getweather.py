from langchain_core.tools import tool
import json
import urllib.parse
import urllib.request
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

MODEL = "llama3.2"

#-------------------------------------------------------------------
# weather tool
#-------------------------------------------------------------------
# Open-Meteo WMO weather code descriptions (simplified)
WEATHER_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "foggy",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    71: "slight snow",
    73: "moderate snow",
    75: "heavy snow",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
}


def _fetch_weather(city: str) -> str:
    """Fetch real weather for a city using Open-Meteo (no API key)."""
    try:
        # Geocode city name to coordinates
        geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
        geocode_params = urllib.parse.urlencode({"name": city, "count": 1})
        with urllib.request.urlopen(f"{geocode_url}?{geocode_params}", timeout=10) as r:
            geo = json.loads(r.read().decode())
        results = geo.get("results")
        if not results:
            return f"Could not find a location named '{city}'."
        lat = results[0]["latitude"]
        lon = results[0]["longitude"] 
        name = results[0].get("name", city)

        # Fetch current weather
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = urllib.parse.urlencode({
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,weather_code",
        })
        with urllib.request.urlopen(f"{weather_url}?{weather_params}", timeout=10) as r:
            data = json.loads(r.read().decode())
        current = data.get("current", {})
        temp = current.get("temperature_2m")
        unit = data.get("current_units", {}).get("temperature_2m", "°C")
        humidity = current.get("relative_humidity_2m")
        code = current.get("weather_code", 0)
        description = WEATHER_CODES.get(code, "unknown conditions")

        return (
            f"In {name}: {description}, {temp}{unit} "
            f"(humidity {humidity}%)."
        )
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        return f"Could not fetch weather for '{city}': {e}."


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city (e.g. 'London', 'New York')."""
    return _fetch_weather(city)


#-------------------------------------------------------------------
# Sub-agent for weather
#-------------------------------------------------------------------
model = ChatOllama(model=MODEL)

subagent_runnable = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt=(
        "You are a specialized weather agent. "
        "Always use the get_weather tool to get accurate information. "
        "Return the shortest possible response that answers the question—no extra "
        "context, no preamble, just the answer."
    )
)


@tool("get_weather_subagent", description="Used to find weather related information.")
def get_weather_subagent(query: str) -> str:
    """This sub-agent can determine the weather for a given city"""
    result = subagent_runnable.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content
