# How to Build a Python Weather Report by City App: Simple & Detailed Guide

<!-- Meta Description: Learn how to create a Python-based Weather Report by City app—first with a one-liner using wttr.in, then with a full-featured solution using OpenStreetMap’s Nominatim geocoding and the Open-Meteo API. Step-by-step code breakdown, error handling, and best practices included. -->

## Table of Contents

1. [Introduction](#introduction)  
2. [Prerequisites](#prerequisites)  
3. [Quick & Simple: wttr.in One-Liner](#quick--simple-wttrin-one-liner)  
4. [The Detailed Approach](#the-detailed-approach)  
   - [1. Geocoding with Nominatim](#1-geocoding-with-nominatim)  
   - [2. Fetching Weather Data from Open-Meteo](#2-fetching-weather-data-from-open-meteo)  
   - [3. Mapping Weather Codes to Descriptions](#3-mapping-weather-codes-to-descriptions)  
   - [4. Error Handling & User Feedback](#4-error-handling--user-feedback)  
5. [Putting It All Together](#putting-it-all-together)  
6. [SEO & Best Practices](#seo--best-practices)  
7. [Conclusion](#conclusion)

---

## Introduction

Whether you’re building a CLI tool for quick forecasts or a full-blown weather dashboard, fetching and displaying weather by city is a classic Python project. In this guide, you’ll first see a **minimal** one-liner solution using wttr.in, then dive into a **robust** implementation leveraging:

- **Nominatim** (OpenStreetMap’s geocoding service)  
- **Open-Meteo API** for current weather data  
- Python’s `requests` library for HTTP calls  

By the end, you’ll understand each section of the code and best practices for error handling, user-agent headers, and mapping weather codes to human-friendly descriptions.

---

## Prerequisites

Make sure you have:

- **Python 3.7+** installed  
- The **requests** library:  
  ```bash
  pip install requests
  ```  
- A basic understanding of HTTP requests and JSON parsing  
- (Optional) An IDE or text editor like VS Code for syntax highlighting  

---

## Quick & Simple: wttr.in One-Liner

For an ultra-lightweight solution, you can use [wttr.in](https://wttr.in/)—a free weather service for the terminal:

```python
import requests

city = input("City: ")
res = requests.get(f"http://wttr.in/{city}?format=3")
print(res.text)
```

- **How it works:**  
  1. Prompts the user for a city name.  
  2. Sends a GET request to wttr.in with `?format=3` (returns “City: +temp +condition”).  
  3. Prints the concise result.  

**Pros:** No API key required; one-liner.  
**Cons:** Limited formatting, no fine-grained control, depends on an external service’s uptime.

---

## The Detailed Approach

For production-grade projects, you’ll often need more control, reliability, and clarity. Let’s explore a two-step version:

### 1. Geocoding with Nominatim

```python
def get_weather(city):
    geocode_url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
    headers = {
        'User-Agent': 'WeatherApp (contact@example.com)'
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
    # ... proceed to fetch weather data
```

- **Why geocode?** Most weather APIs require latitude & longitude.  
- **User-Agent header:** Nominatim requires a descriptive User-Agent to identify your application ([OSM Usage Policy](https://operations.osmfoundation.org/policies/nominatim/)).  
- **JSON parsing & validation:** Always check for empty lists or malformed JSON to avoid crashes.

### 2. Fetching Weather Data from Open-Meteo

```python
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}&current=temperature_2m,weathercode"
    )
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    if 'current' in weather_data:
        current = weather_data['current']
        temperature = current['temperature_2m']
        code = current['weathercode']
        description = get_weather_description(code)

        print(f"Weather in {city.title()}:  ")
        print(f"Temperature: {temperature}°C")
        print(f"Condition: {description}")
    else:
        print(f"Error: Unable to retrieve weather data for '{city}'.")
```

- **Open-Meteo API:** Free, no API key required for basic usage.  
- **Current weather:** We request only `temperature_2m` and `weathercode` to minimize payload.  
- **Data validation:** Ensure the `current` key exists before accessing nested fields.

### 3. Mapping Weather Codes to Descriptions

```python
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
```

- **Why map codes?** Weather APIs use numeric codes for conditions; mapping makes output human-friendly.  
- **Extensibility:** You can extend this dictionary to include icons, humidity, wind speed, etc.

### 4. Error Handling & User Feedback

- **JSON decode errors:** Wrap `response.json()` in a try/except to catch invalid JSON.  
- **Network issues:** Handle `requests.exceptions.RequestException` for timeouts or connection errors.  
- **Invalid input:** Prompt the user to re-enter if the city name yields no geocoding result.

---

## Putting It All Together

```python
import requests

if __name__ == "__main__":
    city = input("Enter city name: ")
    get_weather(city)
```

Combine the functions defined above in a single script to create a seamless CLI weather tool.

---

## SEO & Best Practices

- **Target Keywords:** “Python weather report by city”, “wttr.in tutorial”, “Open-Meteo Python”, “Nominatim geocoding”.  
- **Header Hierarchy:** Use `<h1>` for the main title, `<h2>`/`<h3>` for subsections.  
- **Code Blocks:** Wrap snippets with triple backticks for syntax highlighting.  
- **Internal Linking:** Link to related projects or documentation.  
- **Mobile Optimization:** Ensure code blocks scroll horizontally on small screens.  
- **Alt Text for Images:** If you include screenshots, add descriptive alt text.

---

## Conclusion

You now have two approaches to fetch weather by city in Python:

1. A **one-line** wttr.in solution for quick CLI checks.  
2. A **detailed** implementation using Nominatim geocoding and the Open-Meteo API for production-grade apps.  

Experiment by extending the mapping dictionary, adding error logging, or integrating with a web framework like Flask or Django. Happy coding!

