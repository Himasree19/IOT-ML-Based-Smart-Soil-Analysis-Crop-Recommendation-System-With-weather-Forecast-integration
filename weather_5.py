import requests
from collections import defaultdict
API_KEY = "616ce18a87d5572ca38dae92f46296a1"
CITY = "Guwahati,IN"

url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

# Store daily data
daily_data = defaultdict(list)

# Group by date
for item in data['list']:
    date = item['dt_txt'].split(" ")[0]   # YYYY-MM-DD

    temp = item['main']['temp']
    humidity = item['main']['humidity']
    rain = item.get('rain', {}).get('3h', 0)
    pop = item.get('pop', 0) * 100   # probability %

    daily_data[date].append((temp, humidity, rain, pop))

# Show next 5 days summary
print("\n🌦️ Next 5 Days Weather Forecast:\n")

count = 0
for date, values in daily_data.items():
    if count == 5:
        break

    temps = [v[0] for v in values]
    hums = [v[1] for v in values]
    rains = [v[2] for v in values]
    pops = [v[3] for v in values]


    avg_temp = sum(temps) / len(temps)
    avg_humidity = sum(hums) / len(hums)
    total_rain = sum(rains)

    avg_pop = sum(pops) / len(pops)
    print(f"{date} → Temp:{avg_temp:.2f}°C, Humidity:{avg_humidity:.2f}%, Rain:{avg_pop:.0f}%")

    count += 1