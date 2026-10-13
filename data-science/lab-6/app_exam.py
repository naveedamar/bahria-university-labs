import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib

model = joblib.load("exam_score_model.pkl")

data = {
    "Study_Hours": [1.5, 2.0, 3.0, 3.5, 4.5, 5.0, 6.0, 7.0, 8.0, 9.0],
    "Exam_Score": [48, 52, 58, 63, 70, 74, 81, 86, 92, 97],
}
df = pd.DataFrame(data)

st.set_page_config(page_title="Exam Score Predictor")
st.title("Student Exam Score Predictor")
st.write("Predict final exam score (%) based on weekly study hours using Simple Linear Regression.")

st.header("Study Information")
study_hours = st.number_input(
    "Enter Weekly Study Hours:",
    min_value=0.0,
    max_value=24.0,
    value=6.5,
    step=0.5,
)

if st.button("Predict Exam Score"):
    prediction = model.predict(pd.DataFrame([[study_hours]], columns=["Study_Hours"]))[0]
    st.success("Prediction Completed!")
    st.metric(
        label="Estimated Exam Score",
        value=f"{prediction:.2f}%"
    )

    st.subheader("Regression Line & Prediction")
    X_range = np.linspace(1, 10, 100).reshape(-1, 1)
    y_range = model.predict(pd.DataFrame(X_range, columns=["Study_Hours"]))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["Study_Hours"], df["Exam_Score"], color="blue", label="Actual Data Points")
    ax.plot(X_range, y_range, color="red", label="Regression Line")
    ax.scatter([study_hours], [prediction], color="green", s=130, zorder=5, label=f"Your Prediction ({study_hours} hrs)")
    ax.set_xlabel("Weekly Study Hours")
    ax.set_ylabel("Final Exam Score (%)")
    ax.set_title("Exam Score vs. Study Hours")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend()
    st.pyplot(fig)

    st.subheader("Model Information & Formula")
    st.write(f"**Intercept (β₀):** {model.intercept_:.2f}")
    st.write(f"**Slope (β₁):** {model.coef_[0]:.2f} score points per study hour")
    st.latex(rf"\text{{Exam Score}} = {model.intercept_:.2f} + {model.coef_[0]:.2f} \times (\text{{Study Hours}})")
