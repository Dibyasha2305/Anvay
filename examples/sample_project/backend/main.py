from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):
    input: str


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float


@app.post("/predict")
def predict(request: PredictionRequest):

    return PredictionResponse(
        prediction="not connected",
        confidence=0.0
    )