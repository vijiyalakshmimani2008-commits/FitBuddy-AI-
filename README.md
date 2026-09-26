# FitBuddy – AI Fitness Plan Generator

FitBuddy is an AI-powered web application that generates
personalized 7-day fitness plans using Google Gemini.

## Features

- Personalized 7-day workout plans
- Weight-loss plans
- Muscle-gain plans
- General wellness plans
- Low / Medium / High workout intensity
- Gemini AI workout generation
- Gemini AI nutrition tips
- Feedback-based workout updates
- SQLite database
- SQLAlchemy ORM
- FastAPI backend
- Jinja2 frontend
- Admin / coach dashboard
- FastAPI Swagger documentation
- Local fallback mode when Gemini API is unavailable

---

# Project Structure

FitBuddy/

app/
    __init__.py
    main.py
    config.py
    database.py
    schemas.py
    routes.py
    gemini_generator.py
    gemini_flash_generator.py
    updated_plan.py

templates/
    index.html
    result.html
    all_users.html

static/
    style.css

requirements.txt
.env
.env.example
.gitignore
README.md

---

# Installation

## 1. Create virtual environment

Windows:

python -m venv venv

## 2. Activate

Windows PowerShell:

venv\Scripts\activate

## 3. Install dependencies

pip install -r requirements.txt

## 4. Configure Gemini

Create `.env`.

Add:

GOOGLE_API_KEY=your_api_key

DATABASE_URL=sqlite:///./fitbuddy.db

---

# Run

Run:

uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000

---

# API Documentation

Open:

http://127.0.0.1:8000/docs

---

# Health Check

Open:

http://127.0.0.1:8000/health

---

# Admin Dashboard

Open:

http://127.0.0.1:8000/view-all-users

---

# Main Workflow

1. Open the home page.
2. Enter user information.
3. Select fitness goal.
4. Select workout intensity.
5. Click Generate My Plan.
6. FitBuddy generates a 7-day plan.
7. A nutrition/recovery tip is displayed.
8. Enter feedback.
9. Click Update Plan With AI.
10. The revised plan is stored in SQLite.
11. Open the admin dashboard to view users and plans.

---

# Database

SQLite is automatically created as:

fitbuddy.db

The application creates the database tables automatically
when FastAPI starts.

---

# Gemini Fallback

If GOOGLE_API_KEY is empty or the Gemini API cannot be
reached, FitBuddy uses a local fallback workout plan and
nutrition tip.

This allows the application UI and database workflow to
be tested without an API key.

---

# Important

FitBuddy provides general fitness information and is not
a substitute for professional medical advice.