import joblib
import pandas as pd

# تحميل الموديلات
rf_model = joblib.load("models/forest_tuned.pkl")
xgb_model = joblib.load("models/xgb-tuned.pkl")

# تحميل الـ Preprocessor
preprocessor = joblib.load("models/preprocessor.pkl")
print("Models Loaded Successfully")

# Sample data
sample = pd.DataFrame({
    "CreditScore": [619],
    "Geography": ["France"],
    "Gender": ["Female"],
    "Age": [42],
    "Tenure": [2],
    "Balance": [0.0],
    "NumOfProducts": [1],
    "HasCrCard": [1],
    "IsActiveMember": [1],
    "EstimatedSalary": [101348.88]
})

# Preprocess
sample_processed = preprocessor.transform(sample)

# Random Forest
rf_prediction = rf_model.predict(sample_processed)
rf_probability = rf_model.predict_proba(sample_processed)

# XGBoost
xgb_prediction = xgb_model.predict(sample_processed)
xgb_probability = xgb_model.predict_proba(sample_processed)

print("===== Random Forest =====")
print("Prediction:", rf_prediction[0])
print("Probability:", rf_probability[0])

print("\n===== XGBoost =====")
print("Prediction:", xgb_prediction[0])
print("Probability:", xgb_probability[0])