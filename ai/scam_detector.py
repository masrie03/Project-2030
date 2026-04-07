import os
import time
import joblib
import traceback
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# --- CONFIGURATION ---
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = "us-central1"
DATA_STORE_ID = os.getenv("DATA_STORE_ID")
# We use the 2.0 model as the central 'Brain'
MODEL_NAME = "gemini-2.5-flash" 

# --- INITIALIZE CLIENTS ---
client = None
try:
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)
    print(f"✅ Gemini 2.0 Brain Initialized")
except Exception as e:
    print(f"❌ Initialization Failed: {e}")

# Load the Local ML model (The 'Fast Sensor')
try:
    local_ml_model = joblib.load('ai/scam_model.pkl')
except:
    local_ml_model = None
    print("⚠️ Local ML model not found. Proceeding with Brain only.")

# --- THE BRAIN LOGIC ---

# --- THE BRAIN LOGIC ---

def detect_scam(text: str):
    # 1. GET SENSOR DATA (Local ML)
    local_score = 0.5 # Default to 'Unsure'
    if local_ml_model:
        try:
            probs = local_ml_model.predict_proba([text])[0]
            local_score = probs[1] # Probability of being a scam
        except Exception as e:
            print(f"⚠️ Local ML inference failed: {e}")

    if not client:
        return {"error": "AI Brain Offline"}

    try:
        # Step 1: Brain Orchestration Instruction
        system_instruction = f"""
        You are the 'Brain' of MyShield 2.0. Your role is to orchestrate scam detection for Malaysians.
        You have access to:
        1. A Local ML 'Sensor' Score (Probability from 0.0 to 1.0). Currently: {local_score}
        2. A Grounded Data Store (BNM/PDRM Alert List).
        
        Your Mission:
        - If the Data Store finds a match, that is FACT. Risk is HIGH.
        - If the Local ML Score is high (>0.8) and you see linguistic red flags, Risk is HIGH.
        - Return ONLY a JSON object with keys: is_scam (bool), risk_level (low/med/high), explanation (string), and recommended_action (string).
        """

        # Step 2: Call Gemini (Fixing the nested syntax error here)
        response = client.models.generate_content(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=[
                    types.Tool(
                        retrieval=types.Retrieval(
                            vertex_ai_search=types.VertexAISearch(
                                datastore=f"projects/{PROJECT_ID}/locations/global/collections/default_collection/dataStores/{DATA_STORE_ID}"
                            )
                        )
                    )
                ],
                temperature=0.1
            ),
            contents=f"Analyze this message: {text}"
        )

        # Step 3: Handle the response (Using manual JSON parsing to avoid the 400 error)
        import json
        # Clean the output in case the model wraps it in markdown code blocks
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)

    except Exception as e:
        print(f"--- BRAIN ERROR ---")
        traceback.print_exc()
        return {
            "is_scam": False, 
            "risk_level": "Error", 
            "explanation": f"Error: {str(e)}",
            "recommended_action": "Check backend logs."
        }