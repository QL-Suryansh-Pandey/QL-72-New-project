from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Backend is running successfully"}), 200

if __name__ == '__main__':
    # Note: When using 'flask run', this block is usually bypassed,
    # but it's useful for local testing.
    app.run(debug=True)
