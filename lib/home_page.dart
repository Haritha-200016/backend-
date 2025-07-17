import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String name = '';
  String userId = '';
  String companyName = '';
  late final WebViewController _webViewController;

  @override
  void initState() {
    super.initState();
    _webViewController = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..setNavigationDelegate(
        NavigationDelegate(
          onWebResourceError: (error) {
            _showErrorDialog('Error loading web resource: ${error.description}');
          },
        ),
      );
    _loadUserData();
  }

  Future<void> _loadUserData() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      name = prefs.getString('name') ?? 'No Name';
      userId = prefs.getString('user_id') ?? 'No User ID';
      companyName = prefs.getString('company_name') ?? 'No Company Name';
    });
  }

  void _showErrorDialog(String message) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Error'),
        content: Text(message),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('OK')),
        ],
      ),
    );
  }

  Future<void> _logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    Navigator.pushReplacementNamed(context, '/');
  }

  /*Future<void> _loadDashboard() async {
    final prefs = await SharedPreferences.getInstance();
    String rawCompany = prefs.getString('company_name') ?? '';
    String normalizedCompany = rawCompany.toLowerCase().trim();

    print('🔍 Raw company name: "$rawCompany"');
    print('🔧 Normalized company name: "$normalizedCompany"');

    String dashboardUrl;

    switch (normalizedCompany) {
      case 'velastra':
        dashboardUrl = 'http://104.154.141.198:3000/public-dashboards/b12ea36ab5404822a38f09cb6fd6fb05';
        break;
      case 'coal india':
        dashboardUrl = 'http://104.154.141.198:3000/public-dashboards/3d5686b96ce1404f954a135cb3d41b2c';
        break;
      case 'geosense':
        dashboardUrl = 'http://104.154.141.198:3000/public-dashboards/8e74b0149aed4246946ff2d8ddcd6742';
        break;
      default:
        _showErrorDialog('No dashboard found for "$rawCompany"');
        return;
    }

    _webViewController.loadRequest(Uri.parse(dashboardUrl));
  }*/
  void _loadDashboard() {
    _webViewController.loadRequest(
      Uri.parse('http://104.154.141.198:3000/public-dashboards/3d5686b96ce1404f954a135cb3d41b2c'),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
        actions: [
          IconButton(icon: const Icon(Icons.exit_to_app), onPressed: _logout),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Text('Hello, $name from $companyName'),
          ),
          ElevatedButton(
            onPressed: _loadDashboard,
            child: const Text('Load Dashboard'),
          ),
          Expanded(child: WebViewWidget(controller: _webViewController)),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: _logout,
            child: const Text('Logout'),
          ),
        ],
      ),
    );
  }
}
