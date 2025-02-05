# Weather Data Tracker
The Weather Data Tracker is a Streamlit-based web application that fetches weather data for a specific city using the WeatherStack API and stores it in a local SQLite database. The app allows users to analyze weather data (temperature, humidity, and wind speed) over time and visualize it using various graph types.

# Features
Fetch real-time weather data for any city using the WeatherStack API.
Store and track weather data (temperature, humidity, wind speed, and observation time) in an SQLite database.
Visualize weather data trends with interactive charts (line, bar, scatter) using Plotly.
Analyze historical weather data for temperature, humidity, and wind speed.

# Requirements
Python 3.7 or higher

Streamlit

Requests

SQLite3

Pandas

Plotly

# Setup Instructions

## Step 1: Install Dependencies

Ensure you have Python 3.7+ installed.

You can install the required dependencies by running the following commands:

pip install streamlit requests pandas plotly
## Step 2: Set Up the WeatherStack API
Create a free account on WeatherStack.

Get your API key from the WeatherStack dashboard.

Replace the placeholder API key in the code:

Open the weather_tracker.py file and replace the line:

api_key = "b69e40835bb2e01a5053fcd164322df9"  # Replace with your API key with your actual WeatherStack API key.

## Step 3: Run the Application
You can now start the Streamlit app by running: 

streamlit run weather_tracker.py

This will launch the Streamlit application in your default web browser.

### Screenshot of Weather Data Tracker
![image](https://github.com/user-attachments/assets/81639851-5a61-4af3-9961-55cbd461ef67)

### Select the parameter to be analyzed
![image](https://github.com/user-attachments/assets/2cfc9b0b-fac9-40f3-9607-218299487f31)

### Select Graph Type
![image](https://github.com/user-attachments/assets/5409b4d6-5abc-46dc-8ce8-f8a15bd52255)

### Line plot of Temperature
![image](https://github.com/user-attachments/assets/a4629f8a-3c78-43dd-a543-758122e8e646)







