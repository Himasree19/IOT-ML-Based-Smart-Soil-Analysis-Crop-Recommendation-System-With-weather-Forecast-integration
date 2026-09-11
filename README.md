INTRODUCTION

The IoT & ML-Based Smart Soil Analysis & Crop Recommendation System with Weather Forecast Integration is a smart agriculture platform designed to optimize farming. It combines real-time IoT soil sensors, Machine Learning models, and live weather forecast APIs to evaluate soil parameters and recommend optimal crops for cultivation.

KEY FEATURES

  -Real-time Soil & Environmental Sensing: Reads NPK levels, pH values, soil moisture, temperature, and humidity using ESP microcontrollers and sensors.

  -Intelligent Crop Recommendation: Applies trained ML models (scikit-learn) to analyze soil and environmental data to suggest optimal crops.

  -Live Weather Integration: Fetches real-time weather forecast API data to improve recommendation accuracy based on upcoming conditions.

  -Cloud & Remote Monitoring: Syncs real-time sensor metrics with IoT platforms (Blynk) for remote visibility via mobile and web dashboards.

  -Automated Control: Supports relay-based automation for smart irrigation systems based on live soil moisture thresholds.

SYSTEM ARCHITECTURE
  <img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/0d189be5-a36d-4bea-b3fe-b0844e141667" />

TECH STACK & HARDWARE COMPONENTS
 * Software, Cloud & APIs
   - Programming languages: Python 3.x (Backend & ML), C/C++ (Embedded Hardware)
   - IoT & Cloud Platform: Blynk Cloud
   - External APIs: Live Weather Forecast API
   - Development Tools: Arduino IDE,  VS Code
 * Hardware Components
  - ESP32 / ESP8266 Microcontroller: Primary IoT board handling sensor data collection and cloud connectivity.
  - Soil NPK Sensor: Measures Nitrogen (N), Phosphorus (P), and Potassium (K) levels in the soil.
  - Soil pH Sensor: Measures the acidity or alkalinity level of the soil.
  - Soil Moisture Sensor: Measures the volumetric water content in the soil.
  - DHT11 / DHT22 Sensor: Captures ambient temperature and humidity levels.
  - Relay Module & Water Pump:Enables automated irrigation control based on soil moisture thresholds.

* DEPENDENCIES & LIBRARIES
 - Arduino Libraries
    - WiFi.h
    - WiFiClient.h
    - BlynkSimpleEsp32.h
    - DHT.h
    - HardwareSerial.h
    - ThingSpeak.h
    - Wire.h
    - Adafruit_GFX.h
    - Adafruit_SSD1306.h
    - ESP32 Arduino Core
  - Python Libraries
    - requests
    - pandas
    - numpy
    - joblib
    - collections
    - time
    - scikit-learn
  * APIs / Cloud Services
    - Blynk IoT
    - ThingSpeak
    - OpenWeatherMap API
* HOW TO RUN
  - Open the Arduino IDE.
  - Open the ESP32 .ino file.
  - Upload the code to the ESP32.
  - Open the Blynk IoT Dashboard.
  - Open the ThingSpeak Channel.
  - Open the project folder containing weather5_ml.py and crop_model.pkl.
  - Open Command Prompt/Terminal in the project folder.
  - Run the Python program using: python weather5_ml.py
  - Keep the Python program running.
  - The system will continuously collect sensor data, process weather information, predict the suitable crop, and update the Blynk dashboard and OLED display.
* REPOSITORY STRUCTURE
  - connections Folder
   - This folder contains individual hardware testing programs used to check whether each sensor and component is working correctly before integrating them into       the main project.
   - Main Project Files
    - crop_train.py – Trains the machine learning model using the crop dataset.
    - crop_test.py – Tests the trained crop recommendation model.
    - crop_val.py – Validates the performance of the crop prediction model.
    - crop_model.pkl – Saved Random Forest machine learning model used for crop prediction.
    - test.py – Used for testing the project’s Python functionality.
    - test_blynk.py – Tests communication between Python and the Blynk IoT platform.
    - u.py – Utility/testing Python code used during development.
    - weather.py – Retrieves and processes weather information.
    - weather_5.py – Processes weather forecasts for multiple days.
    - weather_ml.py – Combines weather data with the ML model for crop recommendation.
    - weather5_ml.py – Main Python program integrating weather data, sensor data, ML prediction, and Blynk communication.
