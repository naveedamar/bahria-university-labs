import joblib
import pandas as pd

model = joblib.load("exam_score_model.pkl")
hours = float(input("Enter weekly study hours: "))
prediction = model.predict(pd.DataFrame([[hours]], columns=["Study_Hours"]))

print("\nEstimated Final Exam Score:")
print(f"{prediction[0]:.2f}%")
