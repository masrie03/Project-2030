# ai/config.py
import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

class Config:
    # Google Cloud & Vertex AI
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    LOCATION = os.getenv("LOCATION", "us-central1")
    DATA_STORE_ID = os.getenv("DATA_STORE_ID")
    
    # API Key
    API_KEY = os.getenv("GENAI_API_KEY")
    
    # Model Selection
    # Use 2.0 Flash for the 'Brain' logic
    MODEL_NAME = "gemini-2.0-flash" 
    
    # Safety Check
    @classmethod
    def validate(cls):
        missing = [k for k, v in cls.__dict__.items() if not k.startswith("__") and v is None]
        if missing:
            print(f" Warning: Missing configuration for: {', '.join(missing)}")
        else:
            print(f"Config Loaded: Project 2030 is ready.")

# Run validation on startup
Config.validate()