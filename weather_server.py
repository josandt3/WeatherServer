import requests

from flask import Flask

FORECAST_LINK = "https://api.weather.gov/points/{lattitude},{longitude}"
COLD_TEMPATURE_MAX = 45
MODERATE_TEMPATURE_MAX = 70

def create_app():
    # create and configure the app
    app = Flask(__name__)

    def get_tempature_characterization(temp):
        """
        Function to get the temperature characterization based on the given temperature.
        """
        if temp <= COLD_TEMPATURE_MAX:
            return "Cold"
        elif temp <= MODERATE_TEMPATURE_MAX:
            return "Moderate"
        else:
            return "Hot"

    @app.route('/')
    def index():
        # index page
        return "Welcome to the Weather Server! Use /forecast/[lattitude],[longitude] to get weather forecast. For example: http://127.0.0.1:5000/forecast/39.7456,-97.0892", 200

    @app.route('/forecast/<lattitude>,<longitude>')
    def show_forecast(lattitude, longitude):
        # short forecast and tempature status for the given lattitude and longitude
        try:
            forecast_request = requests.get(FORECAST_LINK.format(lattitude=lattitude, longitude=longitude))
            if forecast_request.status_code != 200:
                return f"Unable to fetch weather data for {longitude},{lattitude}", 500
        except Exception as e:
            return f"Unable to fetch weather data for {longitude},{lattitude}. Error: {e}", 500
        try:
            forecast_json = forecast_request.json()
            forecast_details_url = forecast_json["properties"]["forecast"]
        except Exception as e:
            return f"Unable to parse weather data for {longitude},{lattitude}", 500
        forecast_details_request = requests.get(forecast_details_url)
        if forecast_details_request.status_code != 200:
            return f"Unable to fetch weather details for {longitude},{lattitude}. " \
                    f"Error: {forecast_details_request.text}", {forecast_details_request.status_code}
        try:
            forecast_details_json = forecast_details_request.json()
            short_forecast = forecast_details_json["properties"]["periods"][0]["shortForecast"]
            tempature = forecast_details_json["properties"]["periods"][0]["temperature"]
        except Exception as e:
            return f"Unable to parse weather details for {longitude},{lattitude}. Error: {e}", 500
        return f"Short Forecast: {short_forecast}. " \
                f"Tempature Characterization: {get_tempature_characterization(tempature)}", 200

    return app