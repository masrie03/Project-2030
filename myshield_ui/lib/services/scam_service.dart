import 'dart:convert';
import 'package:http/http.dart' as http;

class ScamService {
  // Use 10.0.2.2 if testing on Android Emulator
  // Use your computer's IP (e.g., 192.168.x.x) if testing on a real phone
  final String apiUrl = "http://127.0.0.1:8000/detect_scam"; 

  Future<Map<String, dynamic>> checkMessage(String userText) async {
    try {
      final response = await http.post(
        Uri.parse(apiUrl),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"text": userText}), 
      );

      if (response.statusCode == 200) {
        return jsonDecode(response.body);
      } else {
        return {
          "is_scam": false,
          "risk_level": "error",
          "explanation": "Server error: ${response.statusCode}",
          "recommended_action": "Try again later"
        };
      }
    } catch (e) {
      return {
        "is_scam": false,
        "risk_level": "offline",
        "explanation": "Could not connect to MyShield AI server.",
        "recommended_action": "Check if your Python backend is running!"
      };
    }
  }
}