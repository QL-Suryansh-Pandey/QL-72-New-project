from backend.api_routes.routes import register_routes
from backend.app_factory import create_app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Note: When using 'flask run', this block is usually bypassed,
    # but it's useful for local testing.
    app.run(debug=True)