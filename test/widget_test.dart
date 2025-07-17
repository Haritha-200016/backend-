import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutterapp/main.dart';  // Correct path to main.dart

void main() {
  testWidgets('Test MyApp Widget', (WidgetTester tester) async {
    // Ensure you're using the correct widget name that is defined in main.dart
    await tester.pumpWidget(MaterialApp(
      home: MyApp(),  // Correct the widget name here, it should be 'MyApp' if that's your root widget
    ));

    // Verify that the text "Hello, World!" is displayed.
    expect(find.text('Hello, World!'), findsOneWidget);  // This should match the text in your app.
  });
}
