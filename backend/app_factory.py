import os
from dotenv import load_dotenv
from flask import Flask

# Load environment variables from .env file
load_dotenv()

def create_app() -> Flask:
    app = Flask(__name__)
    
    # Configuration from environment variables
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
    # Add other configurations here as needed later (e.g., database settings)

    # Register blueprints/routes
    from backend.api_routes.routes import register_routes
    register_routes(app)
    
    return app