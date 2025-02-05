import streamlit as st
import requests
import sqlite3
import pandas as pd
import plotly.express as px

# Set up the database
def init_db():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT,
            temperature REAL,
            humidity REAL,
            wind_speed REAL,
            observation_time TEXT
        )
    ''')
    conn.commit()
    return conn

#Function to fetch weather data
def fetch_weather(city):
    api_key = "b69e40835bb2e01a5053fcd164322df9"  # Replace with your API key
    url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
    response = requests.get(url).json()
    
    if 'current' in response:
        data = {
            'city': city,
            'temperature': response['current']['temperature'],
            'humidity': response['current']['humidity'],
            'wind_speed': response['current']['wind_speed'],
            'observation_time': response['location']['localtime']
        }
        return data
    else:
        return None



# def fetch_weather(city):
#     api_key = "b69e40835bb2e01a5053fcd164322df9"  # Replace with your API key
#     url = f"http://api.weatherstack.com/current?access_key={api_key}&query={city}"
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an error for bad responses
#         data = response.json()
        
#         if 'current' in data:
#             weather_data = {
#                 'city': city,
#                 'temperature': data['current']['temperature'],
#                 'humidity': data['current']['humidity'],
#                 'wind_speed': data['current']['wind_speed'],
#                 'observation_time': data['location']['localtime']
#             }
#             return weather_data
#         else:
#             st.error("No weather data found for the specified city.")
#             return None
#     except requests.ConnectionError:
#         st.error("Failed to connect to the Weatherstack API. Please check your internet connection.")
#         return None
#     except requests.HTTPError as e:
#         st.error(f"HTTP error occurred: {e}")
#         return None
#     except Exception as e:
#         st.error(f"An error occurred: {e}")
#         return None



# Function to store data in SQLite
def store_weather_data(conn, data):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO weather (city, temperature, humidity, wind_speed, observation_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['city'], data['temperature'], data['humidity'], data['wind_speed'], data['observation_time']))
    conn.commit()

# Function to query all weather data for a city from SQLite
def get_all_weather_data(conn, city):
    cursor = conn.cursor()
    query = '''
        SELECT city, temperature, humidity, wind_speed, observation_time
        FROM weather WHERE city = ? ORDER BY observation_time
    '''
    cursor.execute(query, (city,))
    data = cursor.fetchall()
    if data:
        return pd.DataFrame(data, columns=['City', 'Temperature', 'Humidity', 'Wind Speed', 'Observation Time'])
    else:
        return pd.DataFrame()


# import numpy as np

# # Function to query all weather data for a city from SQLite, filling missing dates
# def get_all_weather_data(conn, city):
#     cursor = conn.cursor()
#     query = '''
#         SELECT city, temperature, humidity, wind_speed, observation_time
#         FROM weather WHERE city = ? ORDER BY datetime(observation_time) ASC
#     '''
#     cursor.execute(query, (city,))
#     data = cursor.fetchall()
#     if data:
#         df = pd.DataFrame(data, columns=['City', 'Temperature', 'Humidity', 'Wind Speed', 'Observation Time'])
        
#         # Convert 'Observation Time' to datetime
#         df['Observation Time'] = pd.to_datetime(df['Observation Time'])
        
#         # Set 'Observation Time' as the index
#         df.set_index('Observation Time', inplace=True)

#         # Create a complete date range based on the existing data
#         full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')

#         # Reindex the dataframe to include all dates, filling missing dates with NaN
#         df = df.reindex(full_date_range)

#         # Forward-fill or backward-fill the missing data, or use interpolation
#         df['Temperature'] = df['Temperature'].interpolate(method='linear')
#         df['Humidity'] = df['Humidity'].interpolate(method='linear')
#         df['Wind Speed'] = df['Wind Speed'].interpolate(method='linear')
        
#         # Reset index and rename the index column back to 'Observation Time'
#         df.reset_index(inplace=True)
#         df.rename(columns={'index': 'Observation Time'}, inplace=True)
        
#         return df
#     else:
#         return pd.DataFrame()


# def get_all_weather_data(conn, city):
#     cursor = conn.cursor()
#     query = '''
#         SELECT city, temperature, humidity, wind_speed, observation_time
#         FROM weather WHERE city = ? ORDER BY datetime(observation_time) ASC
#     '''
#     cursor.execute(query, (city,))
#     data = cursor.fetchall()
#     if data:
#         df = pd.DataFrame(data, columns=['City', 'Temperature', 'Humidity', 'Wind Speed', 'Observation Time'])
        
#         # Convert 'Observation Time' to datetime, specifying the format if necessary
#         df['Observation Time'] = pd.to_datetime(df['Observation Time'], format="%Y-%m-%d %H:%M")  # Specify the format
        
#         # Set 'Observation Time' as the index
#         df.set_index('Observation Time', inplace=True)

#         # Create a complete date range based on the existing data
#         full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')

#         # Reindex the dataframe to include all dates, filling missing dates with NaN
#         df = df.reindex(full_date_range)

#         # Forward-fill or backward-fill the missing data, or use interpolation
#         df['Temperature'] = df['Temperature'].interpolate(method='linear')
#         df['Humidity'] = df['Humidity'].interpolate(method='linear')
#         df['Wind Speed'] = df['Wind Speed'].interpolate(method='linear')
        
#         # Reset index and rename the index column back to 'Observation Time'
#         df.reset_index(inplace=True)
#         df.rename(columns={'index': 'Observation Time'}, inplace=True)

#         return df
#     else:
#         return pd.DataFrame()





# Now, in the Streamlit app, when analyzing the latest data:
if st.button("Analyze Latest Data"):
    df = get_all_weather_data(conn, city)
    if not df.empty:
        st.write(df)
        plot_weather_data(df, metric, graph_type)
    else:
        st.error(f"No data available for {city}.")

    



# Function to visualize data using Plotly
def plot_weather_data(data, metric, graph_type):
    if not data.empty:
        if metric == "Temperature":
            y_axis = 'Temperature'
        elif metric == "Humidity":
            y_axis = 'Humidity'
        elif metric == "Wind Speed":
            y_axis = 'Wind Speed'
        
        # Plot based on selected graph type
        if graph_type == "Line":
            fig = px.line(data, x='Observation Time', y=y_axis, title=f"{metric} Trend (Line Chart)")
        elif graph_type == "Bar":
            fig = px.bar(data, x='Observation Time', y=y_axis, title=f"{metric} Trend (Bar Chart)")
        elif graph_type == "Scatter":
            fig = px.scatter(data, x='Observation Time', y=y_axis, title=f"{metric} Trend (Scatter Chart)")
        
        st.plotly_chart(fig)

# Streamlit app UI
st.title("Weather Data Tracker")

conn = init_db()

# Input for city
city = st.text_input("Enter City", "New York")

# # Fetch and store current weather data
# if st.button("Fetch Weather Data"):
#     data = fetch_weather(city)
#     if data:
#         store_weather_data(conn, data)
#         st.success(f"Weather data for {city} fetched and stored successfully!")
#     else:
#         st.error(f"Failed to fetch data for {city}")

# # Analyze the most recent weather data
# st.write("## Weather Data Analysis")

# # Dropdown to select metric
# metric = st.selectbox("Select Metric to Analyze", ("Temperature", "Humidity", "Wind Speed"))

# # Dropdown to select graph type
# graph_type = st.selectbox("Select Graph Type", ("Line", "Bar", "Scatter"))

# # Display all data analysis
# if st.button("Analyze Latest Data"):
#     df = get_all_weather_data(conn, city)
#     if not df.empty:
#         st.write(df)
#         plot_weather_data(df, metric, graph_type)
#     else:
#         st.error(f"No data available for {city}.")

# Fetch and store current weather data
if st.button("Fetch Weather Data", key="fetch_weather_button"):
    data = fetch_weather(city)
    if data:
        store_weather_data(conn, data)
        st.success(f"Weather data for {city} fetched and stored successfully!")
    else:
        st.error(f"Failed to fetch data for {city}")

# Analyze the most recent weather data
st.write("## Weather Data Analysis")

# Dropdown to select metric
metric = st.selectbox("Select Metric to Analyze", ("Temperature", "Humidity", "Wind Speed"))

# Dropdown to select graph type
graph_type = st.selectbox("Select Graph Type", ("Line", "Bar", "Scatter"))

# Display all data analysis
if st.button("Analyze Latest Data", key="analyze_data_button"):
    df = get_all_weather_data(conn, city)
    if not df.empty:
        st.write(df)
        plot_weather_data(df, metric, graph_type)
    else:
        st.error(f"No data available for {city}.")
