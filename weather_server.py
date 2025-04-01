import requests

from flask import Flask

FORECAST_LINK = "https://api.weather.gov/points/{latitude},{longitude}"
COLD_TEMPERATURE_MAX = 45
MODERATE_TEMPERATURE_MAX = 70

def create_app():
    # create and configure the app
    app = Flask(__name__)

    def get_temperature_characterization(temp):
        """
        Function to get the temperature characterization based on the given temperature.
        """
        if temp <= COLD_TEMPERATURE_MAX:
            return "Cold"
        elif temp <= MODERATE_TEMPERATURE_MAX:
            return "Moderate"
        else:
            return "Hot"

    @app.route('/')
    def index():
        # index page
        return "Welcome to the Weather Server! Use /forecast/[latitude],[longitude] to get weather forecast. " \
               "For example: http://127.0.0.1:5000/forecast/39.7456,-97.0892", 200

    @app.route('/forecast/<latitude>,<longitude>')
    def show_forecast(latitude, longitude):
        # Validate input
        lat = float(latitude)
        lon = float(longitude)
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return f"Invalid coordinates for {latitude}, {longitude}. " \
                "Latitude must be between -90 and 90, longitude between -180 and 180", 422
        
        # fetch short forecast and temperature status for the given latitude and longitude
        try:
            forecast_request = requests.get(FORECAST_LINK.format(latitude=latitude, longitude=longitude))
            if forecast_request.status_code != 200:
                return f"Unable to fetch weather data for {latitude},{longitude}", 500
        except Exception as e:
            return f"Unable to fetch weather data for {latitude},{longitude}. Error: {e}", 500
        try:
            forecast_json = forecast_request.json()
            forecast_details_url = forecast_json["properties"]["forecast"]
        except Exception as e:
            return f"Unable to parse weather data for {latitude},{longitude}", 500
        forecast_details_request = requests.get(forecast_details_url)
        if forecast_details_request.status_code != 200:
            return f"Unable to fetch weather details for {latitude},{longitude}. " \
                    f"Error: {forecast_details_request.text}", {forecast_details_request.status_code}
        try:
            forecast_details_json = forecast_details_request.json()
            short_forecast = forecast_details_json["properties"]["periods"][0]["shortForecast"]
            temperature = forecast_details_json["properties"]["periods"][0]["temperature"]
        except Exception as e:
            return f"Unable to parse weather details for {latitude},{longitude}. Error: {e}", 500
        return f"Short Forecast: {short_forecast}. " \
                f"Temperature Characterization: {get_temperature_characterization(temperature)}", 200

    return app