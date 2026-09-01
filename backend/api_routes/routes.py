from flask import Blueprint, jsonify, request
from pydantic import BaseModel, ValidationError, Field
from backend.business.services.bmi_service import calculate_and_save_bmi

# 4. Define the API request schema using Pydantic
class BMIRequest(BaseModel):
    height: float = Field(..., description="Height value")
    height_unit: str = Field(..., description="Height unit (e.g., m, cm, ft)")
    weight: float = Field(..., description="Weight value")
    weight_unit: str = Field(..., description="Weight unit (e.g., kg, lbs)")

# Define the main blueprint for API routes
api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Backend is running successfully"}), 200

@api_bp.route('/db/status', methods=['GET'])
def database_status_check():
    """Verifies database connection and lists accessible tables."""
    try:
        # Assuming db_module is imported correctly and available
        from backend.database import __init__ as db_module
        # Use the reusable context manager to get a connection
        with db_module.DB_CONTEXT as connection:
            if connection:
                cursor = connection.cursor()
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                
                return jsonify({
                    "status": "ok",
                    "message": "Database connection verified successfully.",
                    "tables": tables
                }), 200
            else:
                return jsonify({"status": "error", "message": "Could not establish database connection."}), 503
    except ConnectionError as e:
        # Handle connection failure gracefully
        return jsonify({"status": "error", "message": f"Database connection failed: {e}"}), 500
    except Exception as e:
        # Handle other unexpected database errors (e.g., permissions, query syntax)
        return jsonify({"status": "error", "message": f"An unexpected database error occurred: {e}"}), 500

@api_bp.route('/calculate-bmi', methods=['POST'])
def calculate_bmi_route():
    """Calculates BMI, saves the result, and returns the category."""
    data = request.get_json()
    
    # 1. Validate the incoming request payload using the Pydantic schema.
    try:
        validated_data = BMIRequest(**data)
    except ValidationError as e:
        # Handle Pydantic validation errors (missing fields, wrong types)
        error_messages = [f"Field {err['loc'][0]}: {err['msg']}" for err in e.errors()]
        return jsonify({"status": "error", "message": "Invalid input format: " + ", ".join(error_messages)}), 400

    # 2. Extract User ID (Mocked via header for demonstration)
    user_id_str = request.headers.get('X-User-ID')
    try:
        user_id = int(user_id_str)
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Authentication required: Missing or invalid User ID."}), 401

    # 3. Call the combined BMI/Persistence service
    try:
        bmi_result = calculate_and_save_bmi(
            user_id=user_id,
            height_value=validated_data.height, 
            height_unit=validated_data.height_unit, 
            weight_value=validated_data.weight, 
            weight_unit=validated_data.weight_unit
        )
        # 4. Return the result (BMI and category) as JSON with HTTP 200 OK status.
        return jsonify(bmi_result), 200
    except ValueError as e:
        # Handle validation errors from the service (e.g., unsupported units, zero values)
        return jsonify({"status": "error", "message": str(e)}), 400
    except ConnectionError as e:
        # Handle database connection/persistence failure
        return jsonify({"status": "error", "message": f"Persistence error: {e}"}), 503
    except RuntimeError as e:
        # Handle other unexpected service errors
        return jsonify({"status": "error", "message": str(e)}), 500

def register_routes(app):
    """Registers all API blueprints with the Flask application."""
    # Note: We use the blueprint name 'api' and url_prefix '/' to match the original structure.
    app.register_blueprint(api_bp, url_prefix='/')