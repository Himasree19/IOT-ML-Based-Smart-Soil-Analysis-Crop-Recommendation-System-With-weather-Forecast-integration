import pandas as pd
import joblib
import numpy as np
print ("Starting...")
# Load model
model = joblib.load("crop_model.pkl")
print ("Model Loaded")
# Input sample (same format as training)
sample = pd.DataFrame([[91, 94, 46, 29.36, 76.24, 6.15, 92.82]],
                      columns=["Nitrogen", "phosphorus", "potassium",
                               "temperature", "humidity", "ph", "rainfall"])
print ("Sample:", sample)
# Get probabilities
probs = model.predict_proba(sample)[0]

# Get class labels
classes = model.classes_

# Get indices of top 2 probabilities
top2_idx = np.argsort(probs)[-2:][::-1]

print("Top 2 Crop Recommendations:\n")

for i in top2_idx:
    print(f"{classes[i]} → {probs[i]*100:.2f}%")