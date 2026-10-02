# Machine Learning Labs

This directory contains practical laboratory implementations, datasets exploration, and exercises for the Machine Learning course.

---

## 📌 What & Why

- **What:** Practical implementations of fundamental machine learning concepts, including exploratory data analysis (EDA), data cleaning, feature engineering, regression, and classification algorithms using Python and `scikit-learn`.
- **Why:** To understand how core machine learning algorithms work under the hood, how to evaluate model performance beyond simple accuracy (using precision, recall, F1-score, and confusion matrices), and how to solve real-world problems like price prediction, medical diagnostics, employee attrition, and customer churn.

---

## 🛠️ Requirements & Setup

Make sure you have Python installed along with the required libraries:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn kagglehub
```

---

## 📦 Dataset Management & KaggleHub

### How Datasets Are Handled Here
In these notebooks, datasets are managed programmatically via the **`kagglehub` API**:
- If you are authenticated with Kaggle on your machine (via `~/.kaggle/kaggle.json` or by logging into Kaggle), `kagglehub.dataset_download()` automatically caches and loads datasets directly without needing manual file downloads:

```python
import os
import kagglehub

path = kagglehub.dataset_download("owner-name/dataset-name")
print("Downloaded path:", path)
print("Files in dataset:", os.listdir(path))
```

### For Users Without Kaggle Authentication
If you do not want to use `kagglehub` or do not have a Kaggle account configured:
1. Download the dataset manually as a `.csv` file directly from [Kaggle](https://www.kaggle.com/datasets).
2. Place the `.csv` file in your preferred folder (or the root `datasets/` directory).
3. Replace the `kagglehub` and `os.path.join(path, ...)` loading cells in the notebook with a standard pandas read:

```python
import pandas as pd

df = pd.read_csv("path/to/your/downloaded_file.csv")
```

---

## 🔍 How to Find Kaggle Dataset Identifiers

To find the exact string identifier (e.g., `"johnsmith88/heart-disease-dataset"`):

1. Go to [kaggle.com/datasets](https://www.kaggle.com/datasets) and search for your topic (e.g., *"heart disease"*).
2. Click on the dataset page.
3. Look at the URL in your web browser address bar:
   ```text
   https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset
                                   └──────────────┬──────────────┘
                                         Dataset Identifier
   ```
4. Copy the two-part text after `/datasets/` (`owner-username/dataset-slug`).
5. Pass that copied string into `kagglehub.dataset_download("...")`:

```python
import os
import kagglehub

# Replace with the identifier copied from the URL:
path = kagglehub.dataset_download("johnsmith88/heart-disease-dataset")

# Print the directory and inspect the exact file name:
print("Folder path:", path)
print("Files inside:", os.listdir(path))
```
