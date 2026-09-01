import pytest
from backend.business.services.bmi_service import calculate_bmi

# --- Test Cases for Successful Calculation and Conversions ---

def test_bmi_kg_m_success():
    # Example: 70kg, 1.75m -> BMI approx 22.86
    bmi = calculate_bmi(70, 'kg', 70, 'm')
    assert bmi == 22.86

def test_bmi_lbs_ft_in_success():
    # Example: 154 lbs, 5 ft 10 in (177.8 cm) -> BMI approx 24.2
    # We test feet as the primary unit for height here
    # 5ft = 5 * 0.3048 = 1.524m
    # 10in = 10 * 0.0254 = 0.254m
    # Total height = 1.778m
    # 154 lbs = 70 kg
    bmi = calculate_bmi(154, 'lbs', 177.8, 'cm') # Using cm for height to simplify the test case to a known value
    # Let's use the provided units: lbs and ft
    # 154 lbs = 70 kg. 5 feet = 1.524 m. BMI = 70 / (1.524^2) = 29.82
    bmi_ft_lbs = calculate_bmi(154, 'lbs', 5, 'ft')
    # Note: Since the provided unit support in bmi_service.py only handles one height unit at a time
    # (e.g., height_unit='ft' OR height_unit='cm'), we test the primary support.
    # Test using lbs and ft:
    assert bmi_ft_lbs == 29.82

def test_bmi_cm_lbs_success():
    # Example: 60 kg -> 132.28 lbs. 170 cm = 1.7m. BMI = 60 / (1.7^2) = 20.76
    bmi = calculate_bmi(132.28, 'lbs', 170, 'cm')
    assert bmi == 20.76

def test_bmi_decimal_values_handling():
    # Test with fractional inputs
    bmi = calculate_bmi(65.5, 'kg', 1.78, 'm')
    # 65.5 / (1.78^2) = 20.71
    assert bmi == 20.71

# --- Test Cases for Unit Conversion Accuracy ---

def test_unit_conversion_cm_to_m():
    # 150 cm should be 1.5 m
    assert calculate_bmi(10, 'kg', 150, 'cm') == 2.86

def test_unit_conversion_ft_to_m():
    # 6 ft should be 1.8288 m
    # Test a conversion that results in a known BMI value
    # 70 kg / (1.8288^2) = 22.82
    bmi = calculate_bmi(70, 'kg', 6, 'ft')
    assert bmi == 22.82

def test_unit_conversion_lbs_to_kg():
    # 150 lbs should be 68.0388 kg
    # 150 lbs = 68.0388 kg. Height 1.8m (3.53 ft)
    # BMI = 68.0388 / (1.8^2) = 22.23
    bmi = calculate_bmi(150, 'lbs', 1.8, 'm')
    assert bmi == 22.23

# --- Test Cases for Invalid Inputs and Edge Cases ---

def test_invalid_input_missing_value():
    # Missing weight value
    with pytest.raises(ValueError, match="Missing input values or units."):
        calculate_bmi(170, 'cm', None, 'kg')

def test_invalid_input_zero_height():
    # Zero height
    with pytest.raises(ValueError, match="Height must be a positive value."):
        calculate_bmi(0, 'cm', 70, 'kg')

def test_invalid_input_negative_weight():
    # Negative weight
    with pytest.raises(ValueError, match="Weight must be a positive value."):
        calculate_bmi(170, 'cm', -70, 'kg')

def test_invalid_input_non_numeric_value():
    # Non-numeric height
    with pytest.raises(ValueError, match="Height and weight values must be numeric."):
        calculate_bmi('abc', 'cm', 70, 'kg')

def test_invalid_unit_height():
    # Unsupported height unit
    with pytest.raises(ValueError, match="Unsupported height unit: km"): 
        calculate_bmi(170, 'km', 70, 'kg')

def test_invalid_unit_weight():
    # Unsupported weight unit
    with pytest.raises(ValueError, match="Unsupported weight unit: g"):
        calculate_bmi(170, 'cm', 70, 'g')
