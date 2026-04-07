import 'package:flutter/material.dart';
import 'services/scam_service.dart';

void main() => runApp(const MyShieldApp());

class MyShieldApp extends StatelessWidget {
  const MyShieldApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MyShield AI',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blueAccent),
        useMaterial3: true,
      ),
      home: const ScamScannerScreen(),
    );
  }
}

class ScamScannerScreen extends StatefulWidget {
  const ScamScannerScreen({super.key});

  @override
  State<ScamScannerScreen> createState() => _ScamScannerScreenState();
}

class _ScamScannerScreenState extends State<ScamScannerScreen> {
  final TextEditingController _controller = TextEditingController();
  final ScamService _scamService = ScamService();
  
  Map<String, dynamic>? _result;
  bool _isLoading = false;

  void _analyzeMessage() async {
    if (_controller.text.isEmpty) return;

    setState(() => _isLoading = true);
    
    // This calls your Python Backend!
    final res = await _scamService.checkMessage(_controller.text);
    
    setState(() {
      _result = res;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("MyShield: AI Scam Detector"),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text(
                "Paste a suspicious message, URL, or bank details below:",
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
              ),
              const SizedBox(height: 15),
              TextField(
                controller: _controller,
                maxLines: 4,
                decoration: InputDecoration(
                  hintText: "e.g., Tahniah! Anda memenangi RM5,000 dari PTPTN...",
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12)),
                  filled: true,
                  fillColor: Colors.grey[100],
                ),
              ),
              const SizedBox(height: 20),
              ElevatedButton.icon(
                onPressed: _isLoading ? null : _analyzeMessage,
                icon: _isLoading 
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2))
                    :  const Icon(Icons.shield),
                label: Text(_isLoading ? "Analyzing..." : "Scan for Risks"),
                style: ElevatedButton.styleFrom(padding: const EdgeInsets.symmetric(vertical: 15)),
              ),
              if (_result != null) ...[
                const SizedBox(height: 30),
                _buildResultCard(),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildResultCard() {
    final bool isScam = _result!['is_scam'] ?? false;
    final String risk = _result!['risk_level']?.toString().toUpperCase() ?? "UNKNOWN";
    
    return Card(
      color: isScam ? Colors.red[50] : Colors.green[50],
      shape: RoundedRectangleBorder(
        side: BorderSide(color: isScam ? Colors.red : Colors.green, width: 2),
        borderRadius: BorderRadius.circular(15),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(isScam ? Icons.warning : Icons.check_circle, 
                     color: isScam ? Colors.red : Colors.green),
                const SizedBox(width: 10),
                Text("RISK LEVEL: $risk", 
                     style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              ],
            ),
            const Divider(),
            const Text("AI Explanation:", style: TextStyle(fontWeight: FontWeight.bold)),
            Text(_result!['explanation'] ?? "No explanation provided."),
            const SizedBox(height: 10),
            const Text("Recommended Action:", style: TextStyle(fontWeight: FontWeight.bold)),
            Text(_result!['recommended_action'] ?? "Be cautious."),
          ],
        ),
      ),
    );
  }
}