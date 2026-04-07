import json

def parse_response(raw_text):
    try:
        return json.loads(raw_text)
    except:
        return {
            "is_scam": None,
            "scam_type": "unknown",
            "risk_level": "medium",
            "confidence": 0.0,
            "explanation": "Parsing failed",
            "recommended_action": "Manual review required"
        }