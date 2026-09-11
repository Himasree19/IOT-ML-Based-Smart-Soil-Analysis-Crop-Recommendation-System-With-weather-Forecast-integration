import requests

TOKEN = "0RoxE8WOp5NwC7vtVXETGe08mIgQA_ey"

def get_value(pin):
    url = f"https://blynk.cloud/external/api/get?token={TOKEN}&{pin}"
    response = requests.get(url)
    return response.text

print("Temperature :", get_value("V0"))
print("Humidity    :", get_value("V1"))
print("pH          :", get_value("V3"))

print("Nitrogen    :", get_value("V6"))
print("Phosphorus  :", get_value("V7"))
print("Potassium   :", get_value("V8"))