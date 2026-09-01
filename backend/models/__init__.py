from datetime import datetime

class BMIRecord:
    """Represents a record of a calculated BMI for a user, including metadata."""
    def __init__(self, record_id: int, user_id: int, height: float, height_unit: str, weight: float, weight_unit: str, bmi: float, category: str, creation_timestamp: datetime):
        self.record_id = record_id
        self.user_id = user_id
        self.height = height
        self.height_unit = height_unit
        self.weight = weight
        self.weight_unit = weight_unit
        self.calculated_bmi = bmi
        self.bmi_category = category
        self.calculation_date = creation_timestamp

    def to_dict(self):
        """Returns a dictionary representation suitable for API response."""
        return {
            "record_id": self.record_id,
            "user_id": self.user_id,
            "height": self.height,
            "height_unit": self.height_unit,
            "weight": self.weight,
            "weight_unit": self.weight_unit,
            "bmi": self.calculated_bmi,
            "category": self.bmi_category,
            "calculation_date": self.calculation_date.isoformat()
        }

class User:
    """Represents a registered user in the system."""
    def __init__(self, user_id: int, name: str, email: str, age: int, gender: str, hashed_password: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.age = age
        self.gender = gender
        self.hashed_password = hashed_password

    def to_dict(self):
        """Returns a dictionary representation, excluding sensitive data."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "gender": self.gender,
        }
