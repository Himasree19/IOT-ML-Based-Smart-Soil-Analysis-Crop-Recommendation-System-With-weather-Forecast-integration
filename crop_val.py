# =====================================
# 1. IMPORT LIBRARIES
# =====================================
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# =====================================
# 2. LOAD MODEL
# =====================================
model = joblib.load("crop_model.pkl")

# =====================================
# 3. LOAD VALIDATION DATA
# =====================================
data = pd.read_csv(r"C:\Users\LENOVO\Desktop\mca_4th_implementation\dataset\Validate\crop_data_val.csv")

# =====================================
# 4. SPLIT INPUT AND OUTPUT
# =====================================
X_val = data.drop("label", axis=1)
y_val = data["label"]

# =====================================
# 5. PREDICT
# =====================================
y_pred = model.predict(X_val)

# =====================================
# 6. ACCURACY
# =====================================
accuracy = accuracy_score(y_val, y_pred)
print("Validation Accuracy:", accuracy)

# =====================================
# 7. CLASSIFICATION REPORT
# =====================================
print("\nClassification Report:\n")
print(classification_report(y_val, y_pred))

# =====================================
# 8. CONFUSION MATRIX
# =====================================
cm = confusion_matrix(y_val, y_pred)

plt.figure(figsize=(12,10))
sns.heatmap(cm, cmap="Blues")
plt.title("Validation Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()