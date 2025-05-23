# Project Submission - Weather Service Assignment

### Instructions

##### Write an HTTP server that serves the current weather. Your server should expose an endpoint that:

1.    Accepts latitude and longitude coordinates

2.    Returns the short forecast for that area for Today (“Partly Cloudy” etc)

3.    Returns a characterization of whether the temperature is “hot”, “cold”, or “moderate” (use your discretion on mapping temperatures to each type)

4.    Use the National Weather Service API Web Service as a data source. 

The purpose of this exercise is to provide a sample of your work that we can discuss together in the Technical Interview.

·  We respect your time. Spend as long as you need, but we intend it to take around an hour.

·  We do not expect a production-ready service, but you might want to comment on your shortcuts.

·  The submitted project should build and have brief instructions so we can verify that it works.

·  You may write in whatever language or stack you're most comfortable in, but the technical interviewers are most familiar with Typelevel Scala.


# Prereqs for Testing and Running

1. Create a virtual environment 

    `python3 -m venv venvdir`

1. Start virtual environment

    `source venvdir/bin/activate`

3. Install requirements
    `pip3 install -r requirements.txt`


# Running Server

1. Start Flask
    
    `python3 -m flask --app=weather_server.py run`

2. Naviage to index page in a browser to see app information

    `http://127.0.0.1:5000`

3. Navigate to forecast page via the ***/forecast/{latitude},{longitude}*** endpoint

    `http://127.0.0.1:5000/forecast/39.7456,-97.0892`

# Running Tests

1. Run pytest from the root of the WeatherServer directory

    `pytest tests`


