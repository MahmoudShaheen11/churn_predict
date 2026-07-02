from fastapi import FastAPI
from app.schemas import CustomerData
from app.predictor import predict

app = FastAPI(title="Customer Churn Prediction API")


@app.get("/")
def home():
    return {
        "message": "Welcome to Customer Churn Prediction API"
    }


def predict_customer(customer: CustomerData):

    prediction, probability = predict(
        customer.model_dump(),  # model_dump() Convert Pydantic model to dictionary
        model_name="rf"
    )

    result = "Churn" if prediction == 1 else "Not Churn"

    return {
        "prediction": result,
        "probability": round(float(probability), 4)
    }