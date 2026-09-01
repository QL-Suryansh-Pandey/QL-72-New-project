from flask import Blueprint, jsonify, request
from backend.business.services.bmi_service import calculate_bmi

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
    """Calculates BMI and returns the category."""
    data = request.get_json()
    
    # Assuming request body contains: height_value, height_unit, weight_value, weight_unit
    try:
        bmi_result = calculate_bmi(
            data.get('height_value'), 
            data.get('height_unit'), 
            data.get('weight_value'), 
            data.get('weight_unit')
        )
        return jsonify(bmi_result), 200
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

def register_routes(app):
    """Registers all API blueprints with the Flask application."""
    # Note: We use the blueprint name 'api' and url_prefix '/' to match the original structure.
    app.register_blueprint(api_bp, url_prefix='/')
