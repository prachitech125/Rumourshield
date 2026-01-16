# Rumourshield 🛡️

Rumourshield is a full-stack rumour detection and verification web application.
It checks content from social media posts, news articles, and blogs using basic NLP and Google Fact Check Tools API.

---
# ✅ BACKEND README.md
📍 Path: `backend/README.md`

```md
# Rumourshield Backend (Flask API)

This is the backend service for Rumourshield.
It provides REST APIs to process input text, predict rumour risk, verify claims using Google Fact Check Tools API, and store results in SQLite.

## Tech Used
- Python
- Flask + Flask-CORS
- Google Fact Check Tools API
- SQLite database
- python-dotenv

## Setup

### Install dependencies
```bash
pip install -r requirements.txt
