import os
from functools import wraps
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")

def api_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        provided_key = request.headers.get("X-API-Key")
        if not provided_key or provided_key != API_KEY:
            return jsonify({"error": "Unauthorized: Invalid or missing API Key"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route("/health", methods=["GET"])
@api_key_required
def health():
    return jsonify({"status": "ok", "message": "API is healthy"}), 200

@app.route("/models", methods=["GET"])
@api_key_required
def list_models():
    return jsonify({"message": "Stub: List of available classification models"}), 200

@app.route("/models/register", methods=["POST"])
@api_key_required
def register_model():
    return jsonify({"message": "Stub: Model registration endpoint"}), 200

@app.route("/models/query", methods=["POST"])
@api_key_required
def query_model():
    return jsonify({"message": "Stub: Model query endpoint"}), 200

@app.route("/models/refresh", methods=["POST"])
@api_key_required
def refresh_model():
    return jsonify({"message": "Stub: Model refresh endpoint"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
