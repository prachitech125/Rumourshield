import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from src.preprocess import clean_text
from src.predict import simple_rumour_signal, extract_factcheck_results
from src.factcheck_api import search_fact_checks
from src.utils import safe_strip, build_response
from src.db import save_check, get_history

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # allow React frontend to call backend

# Get API key from .env
API_KEY = os.getenv("GOOGLE_FACTCHECK_API_KEY")
print("API KEY LOADED:", bool(API_KEY))

@app.route("/", methods=["GET"])
def index():
    """Root endpoint - API documentation"""
    return jsonify({
        "message": "🛡️ Rumourshield API is running",
        "version": "1.0.0",
        "endpoints": {
            "health": {
                "url": "/api/health",
                "method": "GET",
                "description": "Check if backend is running"
            },
            "check": {
                "url": "/api/check",
                "method": "POST",
                "description": "Check if text is a rumour",
                "body": {"text": "your text here"}
            },
            "history": {
                "url": "/api/history",
                "method": "GET",
                "description": "Get check history",
                "params": "?limit=10"
            }
        }
    })

@app.route("/api/health", methods=["GET"])
def health():
    """Check if backend is running"""
    return jsonify({"status": "ok", "message": "Backend is healthy"})

@app.route("/api/check", methods=["POST"])
def check():
    """Main API endpoint to check rumour + fact-check verification"""
    data = request.get_json() or {}
    text = safe_strip(data.get("text"))

    if not text:
        return jsonify({"error": "Text is required"}), 400

    # Step 1: clean text
    cleaned = clean_text(text)

    # Step 2: rumour prediction (basic rule-based)
    signal = simple_rumour_signal(cleaned)

    # Step 3: Google fact-check lookup
    factchecks = []
    if API_KEY:
        api_data = search_fact_checks(text, API_KEY)
        if api_data and "claims" in api_data:
            factchecks = extract_factcheck_results(api_data)
    else:
        print("⚠️  Warning: No API key found. Fact-checking disabled.")

    # Step 4: save result in SQLite DB
    try:
        save_check(
            input_text=text,
            prediction=signal["label"],
            confidence=signal["confidence"],
            keywords=signal["matched_keywords"],
            factchecks=factchecks
        )
    except Exception as e:
        print(f"❌ Error saving to database: {e}")

    # Step 5: build final response
    result = build_response(
        input_text=text,
        prediction=signal["label"],
        confidence=signal["confidence"],
        keywords=signal["matched_keywords"],
        factchecks=factchecks
    )
    return jsonify(result)


@app.route("/api/history", methods=["GET"])
def history():
    """Get check history from database"""
    limit = request.args.get("limit", default=10, type=int)
    try:
        return jsonify({"history": get_history(limit)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "message": "Visit / for available endpoints"
    }), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": str(e)
    }), 500

if __name__ == "__main__":
    # Print available routes before starting server
    print("\n✅ Available Routes:")
    for rule in app.url_map.iter_rules():
        methods = ', '.join(rule.methods - {'HEAD', 'OPTIONS'})
        print(f"  {rule.rule:30s} [{methods}]")
    
    print("\n🚀 Starting Flask server on http://127.0.0.1:5000")
    print("📖 Visit http://127.0.0.1:5000/ for API documentation\n")
    app.run(debug=True, port=5000)