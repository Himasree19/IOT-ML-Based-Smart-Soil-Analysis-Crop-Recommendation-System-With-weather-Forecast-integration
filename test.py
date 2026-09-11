import joblib

model = joblib.load("crop_model.pkl")

N = 37
P = 52
K = 104
temperature = 31.6
humidity = 67.4
ph = 6.8
rainfall = 120.0

prediction = model.predict([[N, P, K, temperature, humidity, ph, rainfall]])

print("Recommended Crop:", prediction)
print("Done")