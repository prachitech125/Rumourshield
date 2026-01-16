import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from src.preprocess import clean_text
from src.predict import simple_rumour_signal, extract_factcheck_results
from src.factcheck_api import search_fact_checks
from src.utils import safe_strip, build_response

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # allow React frontend to call backend

# Get API key from .env
API_KEY = os.getenv("GOOGLE_FACTCHECK_API_KEY")



@app.route("/api/health", methods=["GET"])
def health():
    """Check if backend is running"""
    return jsonify({"status": "ok"})


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

    # Step 4: save result in SQLite DB
    save_check(
        input_text=text,
        prediction=signal["label"],
        confidence=signal["confidence"],
        keywords=signal["matched_keywords"],
        factchecks=factchecks
    )

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
    
    limit = request.args.get("limit", default=10, type=int)
    return jsonify({"history": get_history(limit)})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
