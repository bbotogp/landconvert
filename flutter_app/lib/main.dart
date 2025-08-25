import 'package:flutter/material.dart';
import 'land_units_converter.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    final converter = LandUnitsConverter({
      'u1': const Unit(id: 'u1', m2Value: 1.0, displayName: 'Unit 1'),
      'u2': const Unit(id: 'u2', m2Value: 10.0, displayName: 'Unit 2'),
    });
    final result = converter.convert(2, 'u1', 'u2');
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: const Text('Land Units Converter')),
        body: Center(
          child: Text('2 u1 = ${result.result} u2'),
        ),
      ),
    );
  }
}
