# train_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the dataset
df = pd.read_csv("south_lhonak_flood_dataset.csv")

# Features and target
X = df.drop(columns=["GLOF_Event"])
y = df["GLOF_Event"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the model
joblib.dump(model, "flood_prediction_model.pkl")
print("Model saved as flood_prediction_model.pkl")

# Save model and test data for evaluation
joblib.dump((X_test, y_test), "test_data.pkl")  # Save test data separately
print("Model and test data saved.")