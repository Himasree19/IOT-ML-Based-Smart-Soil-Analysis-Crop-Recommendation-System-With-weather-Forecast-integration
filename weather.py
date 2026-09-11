import requests

API_KEY = "616ce18a87d5572ca38dae92f46296a1"
CITY = "Mangaldoi"   # change to your location

url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

# DEBUG: print full response
print("API Response:", data)

# SAFE ACCESS
if 'main' in data:
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    rainfall = data.get('rain', {}).get('1h', 0)

    print("Temperature:", temperature)
    print("Humidity:", humidity)
    print("Rainfall:", rainfall)
else:
    print("Error from API:", data.get("message", "Unknown error"))