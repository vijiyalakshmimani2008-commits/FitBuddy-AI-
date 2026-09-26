from .config import GOOGLE_API_KEY


def fallback_nutrition_tip(goal):

    goal_lower = goal.lower()

    if "muscle" in goal_lower:

        return (
            "Include a protein source in your meals, "
            "stay hydrated, and combine protein with "
            "carbohydrate-rich foods around workouts."
        )

    if "weight" in goal_lower or "loss" in goal_lower:

        return (
            "Focus on balanced meals with vegetables, "
            "fruit, protein-rich foods, whole grains, "
            "adequate water, and sensible portions."
        )

    return (
        "Build balanced meals around vegetables or fruit, "
        "a protein source, whole grains or other carbohydrates, "
        "healthy fats, and adequate water."
    )


def generate_nutrition_tip_with_flash(goal):

    if not GOOGLE_API_KEY:

        return fallback_nutrition_tip(
            goal
        )

    try:

        import google.generativeai as genai

        genai.configure(
            api_key=GOOGLE_API_KEY
        )

        model = genai.GenerativeModel(
            "gemini-1.5-flash"
        )

        prompt = f"""
You are FitBuddy's nutrition assistant.

Fitness goal:
{goal}

Give ONE concise and practical
nutrition or recovery tip.

The response should be easy to understand.

Avoid extreme dieting advice.

Avoid medical diagnosis.

Return only the tip.
"""

        response = model.generate_content(
            prompt
        )

        if response and response.text:

            return response.text

        return fallback_nutrition_tip(
            goal
        )

    except Exception as error:

        print(
            "Gemini nutrition error:",
            error
        )

        return fallback_nutrition_tip(
            goal
        )