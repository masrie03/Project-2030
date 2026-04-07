# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from ai.scam_detector import detect_scam

app = FastAPI(title="MyShield 2.0 MVP")

class Message(BaseModel):
    text: str

@app.post("/detect_scam")
def api_detect_scam(message: Message):
    """
    API endpoint that receives a message and returns scam detection result.
    """
    result = detect_scam(message.text)
    return result

# Optional: Run with uvicorn if testing locally
# uvicorn main:app --reload