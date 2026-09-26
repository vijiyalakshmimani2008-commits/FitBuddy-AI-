from .config import GOOGLE_API_KEY


def update_workout_plan(
    original_plan,
    feedback,
    username="",
    age=30,
    weight=70,
    goal="general wellness",
    intensity="medium"
):

    # -----------------------------------------------------
    # FALLBACK
    # -----------------------------------------------------

    if not GOOGLE_API_KEY:

        return f"""
UPDATED FITBUDDY WORKOUT PLAN

The original plan has been updated based on
the following user feedback:

"{feedback}"


ORIGINAL PLAN
=============

{original_plan}


UPDATE INSTRUCTION
==================

Please apply the user's requested changes
while keeping the plan safe and practical.

The application is currently running without
a Gemini API key, so this fallback response
is being displayed for testing.
"""

    # -----------------------------------------------------
    # GEMINI
    # -----------------------------------------------------

    try:

        import google.generativeai as genai

        genai.configure(
            api_key=GOOGLE_API_KEY
        )

        model = genai.GenerativeModel(
            "gemini-1.5-pro"
        )

        prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Update an existing 7-day workout plan
according to user feedback.

USER

Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}


ORIGINAL PLAN

{original_plan}


USER FEEDBACK

{feedback}


TASK

Create a complete revised 7-day workout plan.

Keep useful parts of the original plan.

Apply the requested changes.

Maintain:

- Warm-up
- Main workout
- Sets/reps or duration
- Rest
- Cooldown/recovery
- Appropriate rest days

Do not diagnose medical conditions.

Return only the revised plan.
"""

        response = model.generate_content(
            prompt
        )

        if response and response.text:

            return response.text

        return original_plan

    except Exception as error:

        print(
            "Gemini update error:",
            error
        )

        return original_plan