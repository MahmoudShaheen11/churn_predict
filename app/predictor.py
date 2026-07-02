import joblib
import pandas as pd

rf_model = joblib.load("models/forest_tuned.pkl")
xgb_model = joblib.load("models/xgb-tuned.pkl")
preprocessor = joblib.load("models/preprocessor.pkl")


def predict(customer_data: dict, model_name="rf"):

    df = pd.DataFrame([customer_data])

    processed = preprocessor.transform(df)

    if model_name == "xgb":
        model = xgb_model
    else:
        model = rf_model

    prediction = model.predict(processed)[0]
    probability = model.predict_proba(processed)[0][1]

    return prediction, probability