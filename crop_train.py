# =====================================
# 1. IMPORT LIBRARIES
# =====================================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
import joblib

# =====================================
# 2. LOAD DATASET
# =====================================
data = pd.read_csv(r"C:\Users\LENOVO\Desktop\mca_4th_implementation\dataset\Train\crop_data_train.csv")

# =====================================
# 3. SPLIT INPUT AND OUTPUT
# =====================================
X = data.drop("label", axis=1)
y = data["label"]

# =====================================
# 4. CREATE MODEL
# =====================================
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# =====================================
# 5. TRAIN MODEL
# =====================================
model.fit(X, y)

print("Model trained successfully ✅")

# =====================================
# 6. PREDICTION ON TRAIN DATA
# =====================================
y_pred = model.predict(X)

# =====================================
# 7. CONFUSION MATRIX
# =====================================
cm = confusion_matrix(y, y_pred)

plt.figure(figsize=(12, 10))
sns.heatmap(cm, cmap="Blues")
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# =====================================
# 8. TRAINING ACCURACY
# =====================================
accuracy = accuracy_score(y, y_pred)
print("Training Accuracy:", accuracy)

# =====================================
# 9. ACCURACY vs TREES (LOSS ALTERNATIVE)
# =====================================
tree_range = [10, 20, 30, 50, 70, 100]
accuracies = []

for n in tree_range:
    temp_model = RandomForestClassifier(n_estimators=n, random_state=42)
    temp_model.fit(X, y)
    pred = temp_model.predict(X)
    acc = accuracy_score(y, pred)
    accuracies.append(acc)

plt.figure()
plt.plot(tree_range, accuracies, marker='o')
plt.title("Accuracy vs Number of Trees")
plt.xlabel("Number of Trees")
plt.ylabel("Accuracy")
plt.show()

# =====================================
# 10. SAVE MODEL
# =====================================
joblib.dump(model, "crop_model.pkl")

print("Model saved successfully ✅")