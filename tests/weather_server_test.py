import pytest
from ..weather_server import create_app

@pytest.fixture()
def app():
    app = create_app()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
    
    
def test_validate_forecast_request():
    """
    Test the forecast request with valid latitude and longitude.
    """
    client = create_app().test_client()
    latitude = 39.7456
    longitude = -97.0892
    forecast_link = f"forecast/{latitude},{longitude}"
    forecast_request = client.get(forecast_link)
    assert forecast_request.status_code == 200, f"Expected status code 200, but got {forecast_request.status_code}"
    assert "Short Forecast:" in forecast_request.text
    assert "Temperature Characterization:" in forecast_request.text
    
def test_invalid_forecast_request():
    """
    Test the forecast request with invalid latitude and longitude.
    """
    client = create_app().test_client()
    latitude = "-90"
    longitude = "-90"
    forecast_link = f"forecast/{latitude},{longitude}"
    forecast_request = client.get(forecast_link)
    assert forecast_request.status_code == 500, f"Expected status code 500, but got {forecast_request.status_code}"
    assert "Unable to fetch weather data" in forecast_request.text, f"Expected error message not found in response: {forecast_request.text}"    
    
def test_invalid_input():
    client = create_app().test_client()
    latitude = "123"
    longitude = "456"
    forecast_link = f"forecast/{latitude},{longitude}"
    forecast_request = client.get(forecast_link)
    assert forecast_request.status_code == 422, f"Expected status code 422, but got {forecast_request.status_code}"
    assert "Invalid coordinates" in forecast_request.text, f"Expected error message not found in response: {forecast_request.text}"
    
def test_index_page():
    """
    Test the index page.
    """
    client = create_app().test_client()
    index_request = client.get('/')
    assert index_request.status_code == 200, f"Expected status code 200, but got {index_request.status_code}"
    assert "Welcome to the Weather Server!" in index_request.text, f"Expected welcome message not found in response: {index_request.text}"