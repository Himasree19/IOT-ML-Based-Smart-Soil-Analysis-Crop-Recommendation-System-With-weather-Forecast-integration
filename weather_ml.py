import requests
from collections import defaultdict
import pandas as pd
import joblib

# =====================================
# 1. LOAD MODEL
# =====================================
model = joblib.load("crop_model.pkl")

# =====================================
# 2. WEATHER API
# =====================================
API_KEY = "616ce18a87d5572ca38dae92f46296a1"
CITY = "Assam,IN"

url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(url)
data = response.json()

# =====================================
# 3. GET TODAY WEATHER (from forecast)
# =====================================
today = list(data['list'])[0]   # nearest time

temperature = today['main']['temp']
humidity = today['main']['humidity']
rainfall = today.get('rain', {}).get('3h', 0)

# =====================================
# 4. GET TODAY RAIN PROBABILITY
# =====================================
today_date = today['dt_txt'].split(" ")[0]

pops = []

for item in data['list']:
    date = item['dt_txt'].split(" ")[0]
    if date == today_date:
        pops.append(item.get('pop', 0) * 100)

# Google-like smoothing
avg_pop = sum(pops) / len(pops)
avg_pop = min(max(avg_pop, 5), 95)
max_pop = max(pops)
rain_prob = (avg_pop * 0.7) + (max_pop * 0.3)

# =====================================
# 5. SENSOR VALUES (replace later)
# =====================================
N = 91
P = 94
K = 46
ph = 6.15

# =====================================
# 6. CREATE ML INPUT
# =====================================
sample = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],
                      columns=["Nitrogen", "phosphorus", "potassium",
                               "temperature", "humidity", "ph", "rainfall"])

# =====================================
# 8. SHOW WEATHER + DECISION
# =====================================
print("\n🌦️ Weather Summary:")
print(f"Temp: {temperature:.2f}°C")
print(f"Humidity: {humidity}%")
print(f"Rain Probability: {rain_prob:.0f}%")


# =====================================
# 8. PREDICT TOP 2 CROPS
# =====================================
import numpy as np

probs = model.predict_proba(sample)[0]
classes = model.classes_

top2_idx = np.argsort(probs)[-2:][::-1]

print("\n🌱 Crop Recommendations:\n")

for i in top2_idx:
    print(f"{classes[i]} → {probs[i]*100:.2f}%")

# =====================================
# 9. SMART IRRIGATION LOGIC
# =====================================
if rain_prob > 70 or rainfall > 10:
    print("\n💧 Irrigation: OFF (Rain expected)")
else:
    print("\n💧 Irrigation: ON (Low rain expected)")