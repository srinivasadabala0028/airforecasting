import requests
from datetime import datetime

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
        country = location["country"]
        state = location.get("state", "N/A")
        
        # Step 2: Air Pollution API to get air quality data
        air_pollution_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}"

        # Make the Air Pollution API request
        air_pollution_response = requests.get(air_pollution_url)

        # Check if the Air Pollution request was successful
        if air_pollution_response.status_code == 200:
            # Parse the JSON response
            air_pollution_data = air_pollution_response.json()
            
            # Check if data is available
            if "list" in air_pollution_data:
                air_pollution_info = air_pollution_data["list"][0]
                aqi = air_pollution_info["main"]["aqi"]
                components = air_pollution_info["components"]
                
                
                # Print the results
                print(f"City: {city_name}")
                print(f"Latitude: {latitude}")
                print(f"Longitude: {longitude}")
                print(f"Air Quality Index (AQI): {aqi}")
                print("Components:")
                print(f"CO: {components['co']} µg/m³")
                print(f"NO: {components['no']} µg/m³")
                print(f"NO2: {components['no2']} µg/m³")
                print(f"O3: {components['o3']} µg/m³")
                print(f"SO2: {components['so2']} µg/m³")
                print(f"PM2.5: {components['pm2_5']} µg/m³")
                print(f"PM10: {components['pm10']} µg/m³")
                print(f"NH3: {components['nh3']} µg/m³")
            else:
                print("No air pollution data available for the specified location.")
        else:
            print("Error: Unable to fetch air pollution data from the API.")
    else:
        print("No geocoding data available for the specified city.")
else:
    print("Error: Unable to fetch geocoding data from the API.")
