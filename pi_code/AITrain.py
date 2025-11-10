import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv("labeled_data.csv")
features = ['light', 'sound', 'motion']
target = 'occupancy' 

X = df[features]
y = df[target]

print("Creating AI model")
model = RandomForestClassifier(n_estimators=100, min_samples_leaf=10, random_state=42)
print("Training model... This might take a moment.")
model.fit(X, y)
print("Saving model to model.pkl...")
joblib.dump(model, "model.pkl")