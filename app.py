from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class EmailInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"status": "Online", "message": "Ryvox Email Environment is running!"}

@app.post("/predict")
def predict_email(data: EmailInput):
    text = data.text.lower()

    if "win" in text or "offer" in text:
        return {"label": "spam"}
    elif "meeting" in text or "report" in text:
        return {"label": "important"}
    else:
        return {"label": "normal"}