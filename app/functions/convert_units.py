
def convert_units(value, from_unit, to_unit):
    conversion_factors = {
        # Length Conversions
        ("Meter", "Füsse"): 3.28084,
        ("Füsse", "Meter"): 1 / 3.28084,
        ("Kilometer", "Meilen"): 0.621371,
        ("Meilen", "Kilometer"): 1 / 0.621371,
        ("Meter", "Kilometer"): 0.001,
        ("Kilometer", "Meter"): 1000,
        ("Meter", "Meilen"): 0.000621371,
        ("Meilen", "Meter"): 1609.344,
        ("Füsse", "Kilometer"): 0.0003048,
        ("Kilometer", "Füsse"): 3280.84,
        ("Füsse", "Meilen"): 0.000189394,
        ("Meilen", "Füsse"): 5280,
        ("Zentimeter", "Zoll"): 0.393701,
        ("Zoll", "Zentimeter"): 2.54,
        ("Meter", "Zentimeter"): 100,
        ("Zentimeter", "Meter"): 0.01,
        ("Kilometer", "Zentimeter"): 100000,
        ("Zentimeter", "Kilometer"): 0.00001,
        ("Zoll", "Füsse"): 1 / 12,
        ("Füsse", "Zoll"): 12,
        ("Yards", "Meter"): 0.9144,
        ("Meter", "Yards"): 1 / 0.9144,
        ("Yards", "Füsse"): 3,
        ("Füsse", "Yards"): 1 / 3,
        ("Yards", "Meilen"): 1 / 1760,
        ("Meilen", "Yards"): 1760,
        ("Yards", "Zoll"): 36,
        ("Zoll", "Yards"): 1 / 36,

        # Volume Conversions
        ("Liter", "Gallonen"): 0.264172,
        ("Gallonen", "Liter"): 3.78541,
        ("Milliliter", "Unzen"): 0.033814,
        ("Unzen", "Milliliter"): 29.5735,
        ("Milliliter", "Liter"): 0.001,
        ("Liter", "Milliliter"): 1000,
        ("Liter", "Unzen"): 33.8140226,
        ("Unzen", "Liter"): 1 / 33.8140226,
        ("Gallonen", "Unzen"): 128,
        ("Unzen", "Gallonen"): 1 / 128,

        # Weight Conversions
        ("Kilogramm", "Pfund"): 2.20462,
        ("Pfund", "Kilogramm"): 1 / 2.20462,
        ("Gramm", "Unzen"): 0.035274,
        ("Unzen", "Gramm"): 1 / 0.035274,
        ("Gramm", "Kilogramm"): 0.001,
        ("Kilogramm", "Gramm"): 1000,
        ("Pfund", "Unzen"): 16,
        ("Unzen", "Pfund"): 1 / 16,
    }

    if (from_unit, to_unit) in conversion_factors:
        return round(value * conversion_factors[(from_unit, to_unit)], 4)
    elif from_unit == "Celsius" and to_unit == "Fahrenheit":
        return round((value * 9/5) + 32, 2)
    elif from_unit == "Fahrenheit" and to_unit == "Celsius":
        return round((value - 32) * 5/9, 2)
    elif from_unit == "Celsius" and to_unit == "Kelvin":
        return round(value + 273.15, 2)
    elif from_unit == "Kelvin" and to_unit == "Celsius":
        return round(value - 273.15, 2)
    elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
        return round((value - 32) * 5/9 + 273.15, 2)
    elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
        return round((value - 273.15) * 9/5 + 32, 2)
    else:
        return "Ungültige Umrechnung"