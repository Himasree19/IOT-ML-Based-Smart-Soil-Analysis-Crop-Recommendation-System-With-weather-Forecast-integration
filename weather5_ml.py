import requests
from collections import defaultdict
import pandas as pd
import joblib
import numpy as np

import requests
import time

TOKEN = "0RoxE8WOp5NwC7vtVXETGe08mIgQA_ey"

def get_value(pin):
    url = f"https://blynk.cloud/external/api/get?token={TOKEN}&{pin}"
    return float(requests.get(url).text)

def send_to_blynk(pin, value):
    url = f"https://blynk.cloud/external/api/update?token={TOKEN}&{pin}={value}"
    requests.get(url)

def send_event(event_code, message):
        url = (
            f"https://blynk.cloud/external/api/logEvent"
            f"?token={TOKEN}"
            f"&code={event_code}"
            f"&description={message}"
        )
        requests.get(url)
# =====================================
# 1. LOAD MODEL
# =====================================
model = joblib.load("crop_model.pkl")

while True:
    
    print("\n==========================")
    print("Running New Prediction")
    print("==========================")
    # =====================================
    # 2. WEATHER API
    # =====================================
    API_KEY = "616ce18a87d5572ca38dae92f46296a1"
    CITY = "Guwahati,IN"

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    # Safety check
    if 'list' not in data:
        print("API Error:", data)
        time.sleep(60)
        continue
    # =====================================
    # 3. PROCESS 5-DAY DATA
    # =====================================
    daily_data = defaultdict(list)

    thunderstorm_sent = False

    for item in data['list']:

        weather_main = item['weather'][0]['main']
        date = item['dt_txt'].split(" ")[0]

        temp = item['main']['temp']
        humidity = item['main']['humidity']
        rain = item.get('rain', {}).get('3h', 0)
        pop = item.get('pop', 0) * 100

        daily_data[date].append((temp, humidity, rain, pop))

        if weather_main == "Thunderstorm" and not thunderstorm_sent:

            send_event(
                "thunderstorm",
                "Thunderstorm Alert! Heavy storm expected. Switch OFF irrigation."
            )

            thunderstorm_sent = True

    # =====================================
    # 4. CALCULATE 5-DAY AVERAGE
    # =====================================
    temps_all = []
    hums_all = []
    rains_all = []
    pops_all = []
    forecast_strings = []
    count = 0
    print("\n🌦️ 5-Day Weather Forecast:\n")

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

        # Rain probability smoothing
        avg_pop = sum(pops) / len(pops)
        avg_pop = min(max(avg_pop, 5), 95)
        max_pop = max(pops)
        final_pop = (avg_pop * 0.7) + (max_pop * 0.3)

        print(f"{date} → Temp:{avg_temp:.2f}°C, Humidity:{avg_humidity:.2f}%, Rain:{final_pop:.0f}%")
        forecast_text = (
        f"Temp: {avg_temp:.1f}°C\n"
        f"Humidity: {avg_humidity:.0f}%\n"
        f"Rain: {final_pop:.0f}%"
    )
        forecast_strings.append(forecast_text)
        temps_all.append(avg_temp)
        hums_all.append(avg_humidity)
        rains_all.append(total_rain)
        pops_all.append(final_pop)
        print(forecast_strings)
        print("Count =", len(forecast_strings))

        count += 1
    send_to_blynk("V12", forecast_strings[0])
    send_to_blynk("V13", forecast_strings[1])
    send_to_blynk("V14", forecast_strings[2])
    send_to_blynk("V15", forecast_strings[3])
    send_to_blynk("V16", forecast_strings[4])

    # =====================================
    # 5. FINAL AVERAGE FOR ML
    # =====================================
    temperature = sum(temps_all) / len(temps_all)
    humidity = sum(hums_all) / len(hums_all)
    rainfall = sum(rains_all)   # TOTAL rainfall over 5 days
    rain_prob = sum(pops_all) / len(pops_all)
    send_to_blynk("V18", round(rain_prob))
    if rain_prob > 80:

        send_event(
            "heavy_rain",
            "Heavy Rain Expected. Irrigation may not be required."
        )

    # =====================================
    # 6. SENSOR VALUES
    # =====================================
    N = get_value("V6")
    P = get_value("V7")
    K = get_value("V8")
    ph = get_value("V3")

    # =====================================
    # 7. CREATE ML INPUT
    # =====================================
    sample = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]],
                        columns=["Nitrogen", "phosphorus", "potassium",
                                "temperature", "humidity", "ph", "rainfall"])

    # =====================================
    # 8. SHOW FINAL WEATHER USED
    # =====================================
    print("\n📊 Average Weather (Used for Prediction):")
    print(f"Temp: {temperature:.2f}°C")
    print(f"Humidity: {humidity:.2f}%")
    print(f"Rain Probability: {rain_prob:.0f}%")

    # =====================================
    # 9. ML PREDICTION
    # =====================================
    probs = model.predict_proba(sample)[0]
    classes = model.classes_
    best_index = np.argmax(probs)

    recommended_crop = classes[best_index]

    print("\nRecommended Crop:", recommended_crop)
    send_to_blynk("V10", recommended_crop)
    print("Crop sent to Blynk V10:", recommended_crop)
    # =====================================
    # 10. IRRIGATION LOGIC
    # =====================================
    if rain_prob > 70 or rainfall > 10:
        print("\n💧 Irrigation: OFF (Rain expected)")
    else:
        print("\n💧 Irrigation: ON (Low rain expected)")
        
    print("\nWaiting 60 seconds for next prediction...")
    time.sleep(60)