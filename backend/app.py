# NOTE: This file is generally superseded by the factory pattern when using Flask.
# We keep it minimal for basic execution if not using the factory pattern directly.
from flask import Flask, jsonify
from backend.app_factory import create_app

app = create_app()

if __name__ == '__main__':
    # Use the factory created app instance
    app.run(debug=True)
