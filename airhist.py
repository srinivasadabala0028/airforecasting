import requests
from datetime import datetime
import pytz

# Replace with your OpenWeather API key
api_key = "d90fab7004bbe953db2d107c55bb1d81"

# Enter the city name
city_name = "Delhi"

# Step 1: Geocoding API to get latitude and longitude
geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"

# Make the Geocoding API request
geocoding_response = requests.get(geocoding_url)

# Check if the Geocoding request was successful
if geocoding_response.status_code == 200:
    # Parse the JSON response
    geocoding_data = geocoding_response.json()
    
    # Check if data is available
    if geocoding_data:
        location = geocoding_data[0]
        latitude = location["lat"]
        longitude = location["lon"]
        
        # Step 2: Specify the start and end dates in Unix time format
        start_date = datetime(2020, 11, 27, 0, 0, 0)
        start_timestamp_utc = int(start_date.timestamp())
        
        # Calculate the end date as today's date
        end_date = datetime.utcnow()
        end_timestamp_utc = int(end_date.timestamp())
        
        # Step 3: Historical Air Pollution API to get historical air quality data
        historical_air_pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution/history?lat={latitude}&lon={longitude}&start={start_timestamp_utc}&end={end_timestamp_utc}&appid={api_key}"
        
        # Make the Historical Air Pollution API request
        historical_air_pollution_response = requests.get(historical_air_pollution_url)

        # Check if the Historical Air Pollution request was successful
        if historical_air_pollution_response.status_code == 200:
            # Parse the JSON response
            historical_air_pollution_data = historical_air_pollution_response.json()
            
            # Check if data is available
            if "list" in historical_air_pollution_data:
                historical_data = historical_air_pollution_data["list"]
                
                # Convert UTC timestamps to IST (Indian Standard Time) and print date, AQI, and components
                for data_point in historical_data:
                    utc_time = datetime.utcfromtimestamp(data_point['dt'])
                    ist_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Kolkata'))
                    date_in_ist = ist_time.strftime('%Y-%m-%d')
                    aqi = data_point['main']['aqi']
                    components = data_point['components']
                    
                    print(f"Date (IST): {date_in_ist}")
                    print(f"AQI: {aqi}")
                    print("Components:")
                    print(f"CO: {components['co']} µg/m³")
                    print(f"NO: {components['no']} µg/m³")
                    print(f"NO2: {components['no2']} µg/m³")
                    print(f"O3: {components['o3']} µg/m³")
                    print(f"SO2: {components['so2']} µg/m³")
                    print(f"PM2.5: {components['pm2_5']} µg/m³")
                    print(f"PM10: {components['pm10']} µg/m³")
                    print(f"NH3: {components['nh3']} µg/m³")
                    print("\n")
            else:
                print("No historical air pollution data available for the specified location and date range.")
        else:
            print("Error: Unable to fetch historical air pollution data from the API.")
    else:
        print("No geocoding data available for the specified city.")
else:
    print("Error: Unable to fetch geocoding data from the API.")
