from .config import GOOGLE_API_KEY


# ---------------------------------------------------------
# FALLBACK PLAN
# ---------------------------------------------------------

def fallback_workout_plan(
    username,
    age,
    weight,
    goal,
    intensity
):

    return f"""
FITBUDDY - 7 DAY FITNESS PLAN

Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}


DAY 1 - FULL BODY
-----------------
Warm-up:
5-10 minutes of light walking and mobility.

Main Workout:
- Bodyweight Squats: 3 sets x 10 reps
- Push-ups: 3 sets x 8 reps
- Glute Bridges: 3 sets x 12 reps
- Plank: 3 x 30 seconds

Rest:
60-90 seconds between sets.

Cooldown:
5 minutes of gentle stretching.


DAY 2 - CARDIO
--------------
Warm-up:
5-10 minutes easy walking.

Main Workout:
- Brisk walking: 20-30 minutes
- Light jogging if comfortable

Cooldown:
5 minutes easy walking and stretching.


DAY 3 - LOWER BODY
------------------
Warm-up:
5-10 minutes.

Main Workout:
- Squats: 3 x 10
- Reverse Lunges: 3 x 8 each leg
- Glute Bridges: 3 x 12
- Calf Raises: 3 x 15

Cooldown:
5-10 minutes stretching.


DAY 4 - RECOVERY
----------------
Active recovery day.

Suggested activities:
- Gentle walking
- Light stretching
- Mobility exercises

Duration:
20-30 minutes.


DAY 5 - UPPER BODY
------------------
Warm-up:
5-10 minutes.

Main Workout:
- Push-ups: 3 x 8
- Resistance/Band Rows: 3 x 10
- Shoulder Press: 3 x 10
- Biceps Curls: 3 x 12

Cooldown:
5-10 minutes.


DAY 6 - CARDIO + CORE
---------------------
Warm-up:
5-10 minutes.

Cardio:
20 minutes moderate activity.

Core:
- Plank: 3 x 30 seconds
- Dead Bug: 3 x 10
- Bird Dog: 3 x 10 each side

Cooldown:
5-10 minutes.


DAY 7 - REST
------------
Rest and recovery.

Optional:
- Gentle walking
- Light stretching
- Mobility work


SAFETY NOTE
-----------
Adjust exercise intensity to your ability.
Stop exercise if you experience pain, dizziness,
or unusual symptoms.
"""


# ---------------------------------------------------------
# GEMINI WORKOUT GENERATOR
# ---------------------------------------------------------

def generate_workout_gemini(
    username,
    age,
    weight,
    goal,
    intensity
):

    # If API key is not available,
    # use local fallback.
    if not GOOGLE_API_KEY:

        return fallback_workout_plan(
            username,
            age,
            weight,
            goal,
            intensity
        )

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

Create a personalized 7-day workout plan.

USER INFORMATION

Name: {username}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

REQUIREMENTS

Create exactly 7 days.

For every day provide:

1. Day name
2. Workout focus
3. Warm-up
4. Main exercises
5. Sets and repetitions OR duration
6. Suggested rest
7. Cooldown/recovery

Include variety.

Possible workout categories:

- Full body
- Upper body
- Lower body
- Cardio
- Core
- Flexibility
- Recovery
- Rest

Make the plan practical and easy to understand.

Do not diagnose medical conditions.

Do not claim that the plan is medical treatment.

Return only the workout plan.
"""

        response = model.generate_content(
            prompt
        )

        if response and response.text:

            return response.text

        return fallback_workout_plan(
            username,
            age,
            weight,
            goal,
            intensity
        )

    except Exception as error:

        print(
            "Gemini workout error:",
            error
        )

        return fallback_workout_plan(
            username,
            age,
            weight,
            goal,
            intensity
        )