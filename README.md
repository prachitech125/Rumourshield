# Rumourshield 🛡️

Rumourshield is a full-stack rumour detection and verification web application.
It checks content from social media posts, news articles, and blogs using basic NLP and Google Fact Check Tools API.

## Tech Stack
- Frontend: React
- Backend: Python (Flask REST API)
- Verification: Google Fact Check Tools API
- Database: SQLite (stores history)

## Features
- Paste any post/news/blog text and check rumour risk
- Get prediction label + confidence score
- Fetch fact-check sources (if available)
- Store and view previous checks (history)

## Project Structure
```bash
Rumourshield/
  frontend/
  backend/
