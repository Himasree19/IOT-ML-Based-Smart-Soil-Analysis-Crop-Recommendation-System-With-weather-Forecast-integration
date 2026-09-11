import pandas as pd
df = pd.read_csv(r"C:\Users\LENOVO\Downloads\Crop_recommendation.csv")              
print(df['label'].value_counts())