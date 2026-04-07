from fastapi import FastAPI
from services.scam_service import analyze_message

app = FastAPI()

@app.post("/check")
def check_scam(text: str):
    return analyze_message(text)