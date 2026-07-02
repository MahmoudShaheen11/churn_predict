from fastapi import FastAPI
from app.schemas import CustomerData
from app.predictor import predict

app = FastAPI(title="Customer Churn Prediction API")


@app.get("/")
def home():
    return {"message": "Customer Churn API is running"}


@app.post("/predict")
def predict_customer(customer: CustomerData):

    prediction, probability = predict(
        customer.model_dump(),
        model_name="rf"
    )

    result = "Churn" if prediction == 1 else "Not Churn"

    return {
        "prediction": result,
        "probability": round(float(probability), 4)
    }