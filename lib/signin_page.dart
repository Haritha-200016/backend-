import 'package:flutter/material.dart';
import 'package:intl_phone_field/intl_phone_field.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:package_info_plus/package_info_plus.dart';

class SignInPage extends StatefulWidget {
  @override
  _SignInPageState createState() => _SignInPageState();
}

class _SignInPageState extends State<SignInPage> {
  String completePhone = '';
  final TextEditingController _passwordController = TextEditingController();
  bool isPasswordVisible = false;
  String appVersion = '';

  @override
  void initState() {
    super.initState();
    _loadAppVersion();
  }

  void _loadAppVersion() async {
    final info = await PackageInfo.fromPlatform();
    setState(() {
      appVersion = '${info.version}+${info.buildNumber}';
    });
  }

  Future<void> signIn(String phone, String password) async {
    if (phone.isEmpty || password.isEmpty) {
      _showError('Please fill in both fields.');
      return;
    }

    final url = Uri.parse('http://104.154.141.198:5001/signin');
    bool isPhone = phone.length >= 6 && phone.length <= 15;
    if (!isPhone) {
      _showError('Invalid phone number format.');
      return;
    }

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'phone_no': phone, 'password': password}),
      );

      final data = json.decode(response.body);

      if (response.statusCode == 200) {
        final user = data['user'];
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('name', user['name']);
        await prefs.setString('user_id', user['user_id'].toString());
        await prefs.setString('company_name', user['company_name']);
        await prefs.setString('sector_name', user['sector_name']);
         Navigator.pushReplacementNamed(context, '/home');
      } else {
        _showError(data['message'] ?? 'An error occurred');
      }
    } catch (e) {
      print('Sign-in error: $e');
      _showError('Something went wrong. Please try again later.');
    }
  }

  void _showError(String msg) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Error'),
        content: Text(msg),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx), child: Text('OK')),
        ],
      ),
    );
  }

 /* void _showSuccess() {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        title: Text('Success'),
        content: Text('Login Successful'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pushReplacementNamed(context, '/home'),
            child: Text('Go to Home'),
          ),
        ],
      ),
    );
  }*/

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(colors: [Colors.pink, Colors.blue]),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              SizedBox(height: 100),

              /// 📞 Phone input
              Theme(
                data: Theme.of(context).copyWith(
                  primaryColor: Colors.white,
                  hintColor: Colors.white,
                  inputDecorationTheme: InputDecorationTheme(
                    enabledBorder: UnderlineInputBorder(
                      borderSide: BorderSide(color: Colors.white),
                    ),
                    focusedBorder: UnderlineInputBorder(
                      borderSide: BorderSide(color: Colors.white),
                    ),
                  ),
                ),
                child: IntlPhoneField(
                  decoration: InputDecoration(
                    labelText: 'Phone Number',
                    labelStyle: TextStyle(color: Colors.white),
                    border: UnderlineInputBorder(
                      borderSide: BorderSide(color: Colors.white),
                    ),
                  ),
                  initialCountryCode: 'IN',
                  style: TextStyle(color: Colors.white),
                  onChanged: (phone) {
                    completePhone = phone.completeNumber;
                  },
                ),
              ),

              SizedBox(height: 10),

              /// 🔒 Password input
              TextField(
                controller: _passwordController,
                obscureText: !isPasswordVisible,
                style: TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: 'Password',
                  labelStyle: TextStyle(color: Colors.white),
                  enabledBorder: UnderlineInputBorder(
                    borderSide: BorderSide(color: Colors.white),
                  ),
                  focusedBorder: UnderlineInputBorder(
                    borderSide: BorderSide(color: Colors.white),
                  ),
                  suffixIcon: IconButton(
                    icon: Icon(
                      isPasswordVisible
                          ? Icons.visibility
                          : Icons.visibility_off,
                      color: Colors.white,
                    ),
                    onPressed: () {
                      setState(() {
                        isPasswordVisible = !isPasswordVisible;
                      });
                    },
                  ),
                ),
              ),

              SizedBox(height: 20),

              /// 🔘 Sign In button
              ElevatedButton(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.white),
                onPressed: () =>
                    signIn(completePhone, _passwordController.text.trim()),
                child: Text('Sign In', style: TextStyle(color: Colors.black)),
              ),

              /// 🔗 Forgot password
              TextButton(
                onPressed: () => Navigator.pushNamed(context, '/forgot'),
                child: Text(
                  "Forgot Password?",
                  style: TextStyle(
                    color: Colors.white,
                    decoration: TextDecoration.underline,
                  ),
                ),
              ),

              SizedBox(height: 20),

              /// 🔗 Sign Up link
              TextButton(
                onPressed: () => Navigator.pushNamed(context, '/signup'),
                child: Text(
                  "Don't have an account? Sign Up",
                  style: TextStyle(color: Colors.white),
                ),
              ),

              SizedBox(height: 10),

              /// ✅ App Version
              Text(
                'App Version: $appVersion',
                style: TextStyle(color: Colors.white, fontSize: 12),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
