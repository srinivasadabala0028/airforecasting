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
        
        # Step 2: One Call Weather API to get air pollution data
        one_call_url = f"http://api.openweathermap.org/data/2.5/onecall?lat={latitude:.6f}&lon={longitude:.6f}&exclude=minutely,hourly,daily,alerts&appid={api_key}"

        # Make the One Call API request
        one_call_response = requests.get(one_call_url)

        # Check if the One Call request was successful
        if one_call_response.status_code == 200:
            # Parse the JSON response
            one_call_data = one_call_response.json()
            
            # Check if data is available
            if "current" in one_call_data:
                current_data = one_call_data["current"]
                aqi = current_data.get("pollution", {}).get("aqi")
                timestamp = current_data.get('dt', 0)
                
                # Convert Unix timestamp to date
                date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
                
                # Print the results
                print(f"City: {city_name}")
                print(f"Latitude: {latitude}")
                print(f"Longitude: {longitude}")
                print(f"Air Quality Index (AQI): {aqi}")
                print(f"Date (IST): {date}")
            else:
                print("No air pollution data available for the specified location.")
        else:
            print("Error: Unable to fetch air pollution data from the One Call API.")
    else:
        print("No geocoding data available for the specified city.")
else:
    print("Error: Unable to fetch geocoding data from the API.")
