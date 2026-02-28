# ML-Based Diabetes Prediction

A machine learning project that predicts whether a patient is likely to have diabetes based on clinical features such as glucose level, BMI, blood pressure, age, and more.

The project includes data preprocessing, model training, evaluation, and a small app script for running predictions on new patient data.

---

## Features

- 📊 **Data preprocessing**
  - Handles missing values and outliers
  - Feature scaling / normalization (e.g., `StandardScaler`)
- 🧠 **Machine learning model**
  - Trained using `scikit-learn` (e.g., Logistic Regression / Random Forest)
  - Saved model file: `db.model`
- 📈 **Model evaluation**
  - Accuracy, confusion matrix, and basic classification metrics
- 🩺 **Prediction script**
  - Takes patient input (from script or UI) and returns diabetes risk prediction
- 🧮 **Dataset**
  - `diabetes_m2023` – cleaned version of the classic Pima Indians Diabetes dataset (or a similar diabetes dataset)

---

## Project Structure

```text
ml-diabetes-prediction/
├─ P1.py                  # Notebook-style / training script (EDA + training)
├─ P2.py                  # Prediction / app script (loads db.model)
├─ db.model               # Trained ML model (saved with joblib / pickle)
├─ diabetes_m2023.csv     # Diabetes dataset (features + label)
├─ p1_dpapp/              # (Optional) app / UI code if used
├─ requirements.txt       # Python dependencies
├─ .gitignore             # Files and folders Git should ignore
└─ README.md              # Project documentation