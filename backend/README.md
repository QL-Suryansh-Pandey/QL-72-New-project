# Backend Project

This project serves as the backend for the BMI Calculator application.

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Linux/macOS
   # venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   export FLASK_APP=app.py
   flask run
   ```

## Endpoints

*   `/health`: Health check endpoint. Returns a status indicating the backend is running successfully.