from flask import Flask

def create_app() -> Flask:
    app = Flask(__name__)
    
    # Register blueprints/routes
    from backend.api_routes.routes import register_routes
    register_routes(app)
    
    return app