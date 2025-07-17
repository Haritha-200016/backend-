import 'package:flutter/material.dart';
import 'package:intl_phone_field/intl_phone_field.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';

class SignUpPage extends StatefulWidget {
  @override
  _SignUpPageState createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  String _completePhone = '';
  String? _selectedSector;
  List<String> _sectors = [];

  String? _selectedCompany;
  List<String> _companies = [];

  bool _isPasswordVisible = false;

  @override
  void initState() {
    super.initState();
    fetchSectors();
  }

  Future<void> fetchSectors() async {
    try {
      final resp = await http.get(Uri.parse('http://104.154.141.198:5001/sectors'));
      if (resp.statusCode == 200) {
        final List<dynamic> data = json.decode(resp.body);
        setState(() {
          _sectors = data
              .map((s) => s['sector_name'].toString())
              .map((name) => name[0].toUpperCase() + name.substring(1))
              .toList();
        });
      } else {
        _showAlert('Failed to load sectors.');
      }
    } catch (e) {
      _showAlert('Unexpected error fetching sectors.');
    }
  }

  Future<void> fetchCompaniesBySector(String sector) async {
    try {
      final resp = await http.get(Uri.parse('http://104.154.141.198:5001/getcompanies?sector=$sector'));
      if (resp.statusCode == 200) {
        final List<dynamic> data = json.decode(resp.body);
        setState(() {
          _companies = data.map((c) => c['company_name'].toString()).toList();
          _selectedCompany = null;
        });
      } else {
        _showAlert('Failed to load companies.');
      }
    } catch (e) {
      _showAlert('Unexpected error fetching companies.');
    }
  }

  Future<void> signUp() async {
    final name = _nameController.text.trim();
    final phone = _completePhone;
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();
    final sector_name = _selectedSector ?? '';
    final company_name = _selectedCompany ?? '';

    if ([name, phone, email, password, sector_name, company_name].any((e) => e.isEmpty)) {
      _showAlert('Please fill in all fields.');
      return;
    }

    final url = Uri.parse('http://104.154.141.198:5001/register');
    try {
      final resp = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'name': name,
          'phone_no': phone,
          'email': email,
          'password': password,
          'sector_name': sector_name,
          'company_name': company_name,
        }),
      );

      final data = json.decode(resp.body);
      if (resp.statusCode == 201 && data['status'] == 'success') {
        // ✅ Save user data to SharedPreferences
        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('name', data['name']);
        await prefs.setString('user_id', data['user_id'].toString());
        await prefs.setString('company_name', data['company_name']);

        _showAlert('User successfully registered. You will get access once verified.',
        onOk: () {
          Navigator.pushReplacementNamed(context, '/');},);
      } else {
        final message = data['message'] ?? 'An error occurred.';
        _showAlert(message);
      }
    } catch (_) {
      _showAlert('Something went wrong. Try again later.');
    }
  }

  void _showAlert(String msg, {VoidCallback? onOk}) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        content: Text(msg),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(ctx);
              if (onOk != null) onOk();
            },
            child: Text('OK'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext ctx) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(colors: [Colors.pink, Colors.blue]),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            children: [
              SizedBox(height: 80),
              _buildTextField(_nameController, 'Name'),
              SizedBox(height: 10),
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
                  ),
                  initialCountryCode: 'IN',
                  style: TextStyle(color: Colors.white),
                  onChanged: (phone) {
                    _completePhone = phone.completeNumber;
                  },
                ),
              ),
              SizedBox(height: 10),
              _buildTextField(_emailController, 'Email'),
              SizedBox(height: 10),
              _buildPasswordField(),
              SizedBox(height: 10),
              DropdownButton<String>(
                value: _selectedSector,
                hint: Text('Select Sector', style: TextStyle(color: Colors.white)),
                dropdownColor: Colors.white,
                onChanged: (v) {
                  setState(() {
                    _selectedSector = v;
                    _companies = [];
                    _selectedCompany = null;
                  });
                  if (v != null) fetchCompaniesBySector(v);
                },
                items: _sectors.map((s) {
                  return DropdownMenuItem(
                    value: s,
                    child: Text(s, style: TextStyle(color: Colors.black)),
                  );
                }).toList(),
              ),
              if (_companies.isNotEmpty)
                DropdownButton<String>(
                  value: _selectedCompany,
                  hint: Text('Select Company', style: TextStyle(color: Colors.white)),
                  dropdownColor: Colors.white,
                  onChanged: (v) => setState(() => _selectedCompany = v),
                  items: _companies.map((c) {
                    return DropdownMenuItem(
                      value: c,
                      child: Text(c, style: TextStyle(color: Colors.black)),
                    );
                  }).toList(),
                ),
              SizedBox(height: 20),
              ElevatedButton(
                onPressed: signUp,
                style: ElevatedButton.styleFrom(backgroundColor: Colors.white),
                child: Text('Sign Up', style: TextStyle(color: Colors.black)),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTextField(TextEditingController ctl, String label) => TextField(
        controller: ctl,
        style: TextStyle(color: Colors.white),
        decoration: InputDecoration(
          labelText: label,
          labelStyle: TextStyle(color: Colors.white),
          enabledBorder: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white)),
          focusedBorder: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white)),
        ),
      );

  Widget _buildPasswordField() => TextField(
        controller: _passwordController,
        obscureText: !_isPasswordVisible,
        style: TextStyle(color: Colors.white),
        decoration: InputDecoration(
          labelText: 'Password',
          labelStyle: TextStyle(color: Colors.white),
          enabledBorder: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white)),
          focusedBorder: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white)),
          suffixIcon: IconButton(
            icon: Icon(
              _isPasswordVisible ? Icons.visibility : Icons.visibility_off,
              color: Colors.white,
            ),
            onPressed: () => setState(() => _isPasswordVisible = !_isPasswordVisible),
          ),
        ),
      );
}
