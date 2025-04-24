from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

app = Flask(__name__)


@app.route("/")
def home():
    return "Pisst's heut?"


################################################# ROUTES ######################################################################

"""
Route to get weather data of a location per URL parameters
    - city
    - country 

example call:   127.0.0.1:5000/weather/data?city=Berlin&country=DE
"""


@app.route("/weather/data")
def getWeatherDataByLocation():
    city = request.args.get("city")
    country = request.args.get("country", "DE")

    if not city:
        return jsonify({"error": "Parameter 'city' ist erforderlich"}), 400

    locationData = getLocationData(city, country)

    lat = locationData[0]["lat"]
    lon = locationData[0]["lon"]

    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric",
        "lang": "de",
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return (
            jsonify({"error": "Fehler bei der Anfrage zur OpenWeather API"}),
            response.status_code,
        )

    return jsonify(response.json())


################################################# LOCAL FUNCTIONS ######################################################################


def getLocationData(city, country):
    url = "https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": f"{city},{country}", "limit": 1, "appid": OPENWEATHERMAP_API_KEY}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return {"error": "Fehler bei der Anfrage zur OpenWeather API"}

    return response.json()


#######################################################################################################################


if __name__ == "__main__":
    app.run(debug=True)
