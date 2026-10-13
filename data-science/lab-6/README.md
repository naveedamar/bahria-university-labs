# Lab 6: Simple Linear Regression

Implementation of an end-to-end Simple Linear Regression workflow predicting student exam scores based on weekly study hours.

## Tasks Overview

- **Task 1: Model Training & Evaluation (`exam_score.py`)**
  - Builds the dataset (Study Hours vs. Exam Score).
  - Splits data into 80% train and 20% test sets.
  - Fits a LinearRegression model using scikit-learn.
  - Evaluates performance using MAE, MSE, RMSE, and R² Score.

- **Task 2: Equation & Manual Verification**
  - Calculates intercept (β₀ = 39.36) and slope (β₁ = 6.64).
  - Mathematical formula: `Exam Score = 39.36 + 6.64 * (Study Hours)`.
  - Manually verifies predicted score for 6.5 hours of study (82.49%).

- **Task 3: Model Persistence & CLI Tool (`predict_score.py`)**
  - Exports trained model to `exam_score_model.pkl` via joblib.
  - Interactive CLI script prompting for user study hours to print estimated score.

- **Task 4: Web Application (`app_exam.py`)**
  - Interactive Streamlit dashboard with numeric input, score prediction, and regression plot.

## File Structure

- `exam_score.py`: Model training, metrics evaluation, formula verification, and model export.
- `predict_score.py`: Command-line prediction utility.
- `app_exam.py`: Streamlit web interface.
- `exam_score_model.pkl`: Serialized trained model.

## How to Run

1. Train and evaluate model:
   ```bash
   python exam_score.py
   ```

2. Run CLI predictor:
   ```bash
   python predict_score.py
   ```

3. Launch Streamlit web dashboard:
   ```bash
   streamlit run app_exam.py
   ```
