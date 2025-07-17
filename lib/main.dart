import 'package:flutter/material.dart';
import 'signin_page.dart.';  // Ensure this matches the location of sign_in_page.dart
import 'home_page.dart.';     // Ensure this matches the location of home_page.dart
import 'signup_page.dart';   // Ensure this matches the location of signup_page.dart
import 'forgot_password_page.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter App',
      initialRoute: '/',
      routes: {
        '/': (context) => SignInPage(), // The SignInPage widget is used here
        '/home': (context) => HomePage(),
        '/signup': (context) => SignUpPage(),
        '/forgot': (context) => ForgotPasswordPage(),
      },
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
    );
  }
}
