import math

def _to_meters(height_value: float, height_unit: str) -> float:
    """Converts height to meters."""
    if height_unit.lower() == 'cm':
        return height_value / 100.0
    elif height_unit.lower() in ['ft', 'feet']: # Assuming 'ft' is used for feet
        # 1 foot = 0.3048 meters
        return height_value * 0.3048
    elif height_unit.lower() in ['in', 'inches']:
        # 1 inch = 0.0254 meters
        return height_value * 0.0254
    else:
        raise ValueError(f"Unsupported height unit: {height_unit}")

def _to_kilograms(weight_value: float, weight_unit: str) -> float:
    """Converts weight to kilograms."""
    if weight_unit.lower() == 'kg':
        return weight_value
    elif weight_unit.lower() == 'lbs':
        # 1 pound = 0.453592 kilograms
        return weight_value * 0.453592
    else:
        raise ValueError(f"Unsupported weight unit: {weight_unit}")

def calculate_bmi(height_value, height_unit, weight_value, weight_unit) -> float:
    """Calculates BMI after converting inputs to meters and kilograms."""
    
    # 1. Validation
    if height_value is None or height_unit is None or weight_value is None or weight_unit is None:
        raise ValueError("Missing input values or units.")

    try:
        # Check for non-numeric or impossible values
        if not isinstance(height_value, (int, float)) or not isinstance(weight_value, (int, float)):
             raise TypeError("Height and weight values must be numeric.")

        if height_value <= 0:
            raise ValueError("Height must be a positive value.")
        if weight_value <= 0:
            raise ValueError("Weight must be a positive value.")

    except TypeError as e:
        raise ValueError(f"Invalid data type provided: {e}")
    except ValueError as e:
        # Re-raise specific domain errors
        raise e

    # 2. Conversion to base units (meters and kilograms)
    try:
        height_m = _to_meters(height_value, height_unit)
        weight_kg = _to_kilograms(weight_value, weight_unit)
    except ValueError as e:
        # Catch unsupported units from conversion helpers
        raise ValueError(f"Conversion error: {e}")

    # 3. Calculation (BMI = weight / height^2)
    # Height is already validated to be > 0, so division by zero is prevented
    bmi = weight_kg / (height_m ** 2)

    # 4. Rounding
    return round(bmi, 2)
