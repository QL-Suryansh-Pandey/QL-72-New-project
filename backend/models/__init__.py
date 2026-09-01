from datetime import datetime

class BMIRecord:
    """Represents a record of a calculated BMI for a user."""
    def __init__(self, user_id: int, height: float, height_unit: str, weight: float, weight_unit: str, bmi: float, category: str):
        self.user_id = user_id
        self.height = height
        self.height_unit = height_unit
        self.weight = weight
        self.weight_unit = weight_unit
        self.calculated_bmi = bmi
        self.bmi_category = category
        self.creation_timestamp = datetime.utcnow()