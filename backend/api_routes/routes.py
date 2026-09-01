from flask import Blueprint, jsonify

# Define the main blueprint for API routes
api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Backend is running successfully"}), 200

def register_routes(app):
    """Registers all API blueprints with the Flask application."""
    app.register_blueprint(api_bp, url_prefix='/')
