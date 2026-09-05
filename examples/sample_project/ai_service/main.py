from pydantic import BaseModel
from fastapi import FastAPI
app = FastAPI()

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    result: str
    score: float

@app.post("/generate") 

def generate(request: GenerateRequest): 
    return GenerateResponse(
        result="positive",
        score=0.95
          )