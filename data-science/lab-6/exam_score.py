import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

data = {
    "Study_Hours": [1.5, 2.0, 3.0, 3.5, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0],
    "Exam_Score": [48, 52, 58, 63, 70, 74, 81, 86, 92, 97],
}
df = pd.DataFrame(data)
print("Student Exam Score Dataset:")
print(df)

X = df[["Study_Hours"]]
y = df["Exam_Score"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("\nTraining Features (X_train):")
print(X_train)
print("\nTesting Features (X_test):")
print(X_test)

model = LinearRegression()
model.fit(X_train, y_train)
print("\nModel Training Completed!")

y_pred = model.predict(X_test)
print("\nActual Test Exam Scores:")
print(y_test.values)
print("\nPredicted Test Exam Scores:")
print(np.round(y_pred, 2))

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\nModel Evaluation Metrics:")
print(f"MAE: {mae:.2f}")
print(f"MSE: {mse:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.4f}")

beta_0 = model.intercept_
beta_1 = model.coef_[0]

print("\nModel Coefficients:")
print(f"Intercept (β₀): {beta_0:.2f}")
print(f"Slope (β₁): {beta_1:.2f}")

print("\nMathematical Formula:")
print(f"Exam Score = {beta_0:.2f} + {beta_1:.2f} * (Study Hours)")

study_hours_manual = 6.5
manual_score = beta_0 + (beta_1 * study_hours_manual)
model_score = model.predict(pd.DataFrame([[study_hours_manual]], columns=["Study_Hours"]))[0]

print(f"\nManual Verification for {study_hours_manual} Study Hours:")
print(f"Formula Calculation: {beta_0:.2f} + {beta_1:.2f} * {study_hours_manual} = {manual_score:.2f}%")
print(f"Model .predict() Calculation: {model_score:.2f}%")

joblib.dump(model, "exam_score_model.pkl")
print("\nModel exported successfully to 'exam_score_model.pkl'!")

plt.figure(figsize=(8, 5))
plt.scatter(X, y, color="blue", label="Actual Student Data")
plt.plot(X, model.predict(X), color="red", label="Regression Line")
plt.scatter([study_hours_manual], [model_score], color="green", s=100, zorder=5,
            label=f"Prediction (6.5 hrs = {model_score:.1f}%)")
plt.xlabel("Weekly Study Hours")
plt.ylabel("Final Exam Score (%)")
plt.title("Student Exam Score Prediction Based on Study Hours")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("exam_score_regression.png")
print("Saved regression plot to 'exam_score_regression.png'")
