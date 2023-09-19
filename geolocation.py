import requests

# Replace with your OpenWeather API key
api_key = "d90fab7004bbe953db2d107c55bb1d81"

# Enter the city name
city_name = "Delhi"

# Define the API endpoint URL
url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"

# Make the API request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Check if data is available
    if data:
        location = data[0]
        city_name = location["name"]
        latitude = location["lat"]
        longitude = location["lon"]
        country = location["country"]
        state = location.get("state", "N/A")
        
        # Print the results
        print(f"City: {city_name}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Country: {country}")
        print(f"State: {state}")
    else:
        print("No data available for the specified city.")
else:
    print("Error: Unable to fetch data from the API.")