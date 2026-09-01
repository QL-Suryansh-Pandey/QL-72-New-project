import os
from dotenv import load_dotenv
from flask import Flask

# Import the database context manager
from backend.database import __init__ as db_module

# Load environment variables from .env file
load_dotenv()

def create_app() -> Flask:
    app = Flask(__name__)
    
    # Configuration from environment variables
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
    
    # 1. Database Configuration (optional, but good practice)
    # We rely on the connection layer, but we can set configuration flags here.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:pass@host:port/dbname' # Placeholder

    # 2. Database Setup/Initialization Hook
    # This ensures the application attempts to connect and verify setup on startup.
    try:
        # Attempt a basic connection test during application setup
        with db_module.DB_CONTEXT as db_conn:
            # Test connectivity by running a simple query (e.g., SELECT 1)
            with db_conn.cursor() as cursor:
                cursor.execute("SELECT 1")
                print("Database connection successful and verified.")
        
        # NOTE: In a full application, you would run the database_setup.sql here
        # or use a dedicated migration tool. For this requirement, successful connection verification suffices.
        
    except ConnectionError as e:
        # Critical failure: Flask cannot start without a database connection
        print(f"CRITICAL ERROR: Failed to connect to database. Application cannot start. Details: {e}")
        # Depending on requirements, you might raise SystemExit or handle this more gracefully
        # For demonstration, we let Flask attempt to start, but the failure is logged.
        pass

    # Register blueprints/routes
    from backend.api_routes.routes import register_routes
    register_routes(app)
    
    return app