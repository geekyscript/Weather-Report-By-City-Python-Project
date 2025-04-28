import requests


def get_weather(city):
    # Geocoding to get latitude and longitude
    geocode_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"

    headers = {
        'User-Agent': 'WeatherApp (contact@example.com)'  # Replace with your contact info or app name
    }

    response = requests.get(geocode_url, headers=headers)
    try:
        location_data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: Unable to fetch location data. Try again later.")
        return

    if not location_data:
        print(f"Error: Unable to find location data for '{city}'. Please check the city name.")
        return

    latitude = location_data[0]['lat']
    longitude = location_data[0]['lon']

    # Fetching weather data from Open-Meteo API
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&current=temperature_2m,weathercode"
    )

    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    if 'current' in weather_data:
        current_weather = weather_data['current']
        temperature = current_weather['temperature_2m']
        weather_code = current_weather['weathercode']
        weather_description = get_weather_description(weather_code)

        print(f"Weather in {city.title()}:")
        print(f"Temperature: {temperature}°C")
        print(f"Condition: {weather_description}")
    else:
        print(f"Error: Unable to retrieve weather data for '{city}'.")


def get_weather_description(code):
    weather_descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Drizzle: Light",
        53: "Drizzle: Moderate",
        55: "Drizzle: Dense intensity",
        56: "Freezing Drizzle: Light",
        57: "Freezing Drizzle: Dense intensity",
        61: "Rain: Slight",
        63: "Rain: Moderate",
        65: "Rain: Heavy intensity",
        66: "Freezing Rain: Light",
        67: "Freezing Rain: Heavy intensity",
        71: "Snow fall: Slight",
        73: "Snow fall: Moderate",
        75: "Snow fall: Heavy intensity",
        77: "Snow grains",
        80: "Rain showers: Slight",
        81: "Rain showers: Moderate",
        82: "Rain showers: Violent",
        85: "Snow showers: Slight",
        86: "Snow showers: Heavy",
        95: "Thunderstorm: Slight or moderate",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_descriptions.get(code, "Unknown weather condition")


if __name__ == "__main__":
    city = input("Enter city name: ")
    get_weather(city)
