# services/scam_service.py
from ai.scam_detector import detect_scam
import json

def analyze_message(text: str) -> dict:
    """
    Calls the AI detector and returns parsed JSON.
    If AI fails or returns invalid JSON, fallback rules apply.
    """
    # raw is already a dictionary returned by detect_scam()
    result = detect_scam(text) 
    
    try:
        # Check if it's already a dict or needs parsing
        if isinstance(result, str):
            result = json.loads(result)
            
        required_keys = ["is_scam", "risk_level", "explanation", "recommended_action"]
        for key in required_keys:
            if key not in result:
                # Provide a default value if key is missing to avoid crashing the Flutter UI
                result[key] = "N/A"
        return result
    except Exception as e:
        print("Parsing or AI fallback triggered:", e)
        # Simple rule-based fallback
        text_lower = text.lower()
        if any(word in text_lower for word in ["free", "click", "win", "giveaway", "rm"]):
            return {
                "is_scam": True,
                "risk_level": "high",
                "explanation": "Contains giveaway/clickbait language",
                "recommended_action": "Do not click links or share info"
            }
        return {
            "is_scam": False,
            "risk_level": "low",
            "explanation": "Normal text",
            "recommended_action": "No action needed"
        }