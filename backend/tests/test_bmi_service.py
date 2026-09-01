import pytest
from backend.business.services.bmi_service import calculate_bmi

# --- Test Cases for Successful Calculation and Conversions ---

def test_bmi_kg_m_success():
    # Example: 70kg, 1.75m -> BMI approx 22.86
    result = calculate_bmi(70, 'kg', 1.75, 'm')
    assert result['bmi'] == 22.86
    assert result['category'] == 'Normal Weight'

def test_bmi_lbs_ft_in_success():
    # Example: 154 lbs, 5 ft (1.524m) -> BMI approx 29.82
    result = calculate_bmi(154, 'lbs', 5, 'ft')
    assert result['bmi'] == 29.82
    assert result['category'] == 'Overweight'

def test_bmi_cm_lbs_success():
    # Example: 132.28 lbs, 170 cm (1.7m). BMI = 20.76
    result = calculate_bmi(132.28, 'lbs', 170, 'cm')
    assert result['bmi'] == 20.76
    assert result['category'] == 'Normal Weight'

def test_bmi_decimal_values_handling():
    # Test with fractional inputs: 65.5 kg, 1.78 m -> 20.71
    result = calculate_bmi(65.5, 'kg', 1.78, 'm')
    assert result['bmi'] == 20.71
    assert result['category'] == 'Normal Weight'

# --- Test Cases for Unit Conversion Accuracy ---

def test_unit_conversion_cm_to_m():
    # 10 kg, 150 cm (1.5 m) -> BMI = 10 / (1.5^2) = 4.44
    # Note: Original test case 2.86 seems incorrect for 10kg/1.5m. Using calculated value.
    result = calculate_bmi(10, 'kg', 150, 'cm')
    assert result['bmi'] == 4.44
    assert result['category'] == 'Underweight'

def test_unit_conversion_ft_to_m():
    # 70 kg, 6 ft (1.8288 m) -> BMI = 22.82
    result = calculate_bmi(70, 'kg', 6, 'ft')
    assert result['bmi'] == 22.82
    assert result['category'] == 'Normal Weight'

def test_unit_conversion_lbs_to_kg():
    # 150 lbs (68.04 kg), 1.8m -> BMI = 22.23
    result = calculate_bmi(150, 'lbs', 1.8, 'm')
    assert result['bmi'] == 22.23
    assert result['category'] == 'Normal Weight'

# --- Boundary Case Tests (Required by Issue #15) ---

def test_bmi_boundary_18_49_underweight():
    # 18.49 < 18.5 -> Underweight
    # Using 60 kg / (1.8^2) = 18.52. Let's use a value that results in 18.49.
    # 60 / (H^2) = 18.49 => H = 1.806
    result = calculate_bmi(60, 'kg', 1.806, 'm')
    assert result['bmi'] == 18.49
    assert result['category'] == 'Underweight'

def test_bmi_boundary_18_50_normal_weight():
    # 18.5 >= 18.5 -> Normal Weight
    # Using 60 kg / (1.806^2) = 18.49. Let's use a value that results in 18.50.
    # 60 / (H^2) = 18.50 => H = 1.803
    result = calculate_bmi(60, 'kg', 1.803, 'm')
    assert result['bmi'] == 18.50
    assert result['category'] == 'Normal Weight'

def test_bmi_boundary_24_99_normal_weight():
    # 24.99 < 25 -> Normal Weight
    # Using 70 kg / (H^2) = 24.99 => H = 1.678
    result = calculate_bmi(70, 'kg', 1.678, 'm')
    assert result['bmi'] == 24.99
    assert result['category'] == 'Normal Weight'

def test_bmi_boundary_25_00_overweight():
    # 25.00 >= 25 -> Overweight
    # Using 70 kg / (H^2) = 25.00 => H = 1.673
    result = calculate_bmi(70, 'kg', 1.673, 'm')
    assert result['bmi'] == 25.00
    assert result['category'] == 'Overweight'

def test_bmi_boundary_29_99_overweight():
    # 29.99 < 30 -> Overweight
    # Using 70 kg / (H^2) = 29.99 => H = 1.530
    result = calculate_bmi(70, 'kg', 1.530, 'm')
    assert result['bmi'] == 29.99
    assert result['category'] == 'Overweight'

def test_bmi_boundary_30_00_obesity():
    # 30.00 >= 30 -> Obesity
    # Using 70 kg / (H^2) = 30.00 => H = 1.527
    result = calculate_bmi(70, 'kg', 1.527, 'm')
    assert result['bmi'] == 30.00
    assert result['category'] == 'Obesity'

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
