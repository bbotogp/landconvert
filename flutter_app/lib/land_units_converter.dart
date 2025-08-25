import 'dart:collection';

/// Represents a single land measurement unit.
class Unit {
  final String id;
  final double m2Value;
  final String? displayName;
  final String? country;
  final String? region;

  const Unit({
    required this.id,
    required this.m2Value,
    this.displayName,
    this.country,
    this.region,
  });
}

/// Result of a conversion between two units.
class ConversionResult {
  final double inputValue;
  final String fromUnit;
  final String toUnit;
  final String? region;
  final double conversionFactor;
  final double result;
  final DateTime timestamp;

  ConversionResult({
    required this.inputValue,
    required this.fromUnit,
    required this.toUnit,
    this.region,
    required this.conversionFactor,
    required this.result,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();

  Map<String, dynamic> toMap() => {
        'input_value': inputValue,
        'from_unit': fromUnit,
        'to_unit': toUnit,
        'region': region,
        'conversion_factor': conversionFactor,
        'result': result,
        'timestamp': timestamp.toIso8601String(),
      };
}

/// In-memory implementation of the land units converter.
class LandUnitsConverter {
  final Map<String, Unit> _units;

  LandUnitsConverter(Map<String, Unit> units) : _units = HashMap.of(units);

  double _fetchM2(String unitId, [String? region]) {
    final unit = _units[unitId];
    if (unit == null) {
      throw ArgumentError('الوحدة غير موجودة: $unitId');
    }
    return unit.m2Value;
  }

  ConversionResult convert(double value, String fromUnit, String toUnit,
      {String? region}) {
    final fromM2 = _fetchM2(fromUnit, region);
    final toM2 = _fetchM2(toUnit, region);
    final factor = fromM2 / toM2;
    return ConversionResult(
      inputValue: value,
      fromUnit: fromUnit,
      toUnit: toUnit,
      region: region,
      conversionFactor: factor,
      result: value * factor,
    );
  }

  List<Unit> listUnits({String? country}) {
    return _units.values
        .where((u) => country == null || u.country == country)
        .toList();
  }
}
