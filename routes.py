from pathlib import Path

from fastapi import (
    APIRouter,
    Request,
    Form
)

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from .schemas import UserInput

from .database import (
    save_user,
    save_plan,
    get_user,
    get_plan,
    update_plan,
    get_all_users,
    get_all_plans
)

from .gemini_generator import (
    generate_workout_gemini
)

from .gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)

from .updated_plan import (
    update_workout_plan
)


# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------

router = APIRouter()


# ---------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------

BASE_DIR = Path(
    __file__
).resolve().parent.parent

TEMPLATE_DIR = BASE_DIR / "templates"

templates = Jinja2Templates(
    directory=str(TEMPLATE_DIR)
)


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# ---------------------------------------------------------
# GENERATE WORKOUT
# ---------------------------------------------------------

@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout(
    request: Request,

    username: str = Form(...),

    user_id: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...)
):

    # Validate user input
    user_data = UserInput(
        username=username.strip(),
        user_id=user_id.strip(),
        age=age,
        weight=weight,
        goal=goal.strip(),
        intensity=intensity.strip()
    )

    # Generate workout
    workout_plan = generate_workout_gemini(
        username=user_data.username,
        age=user_data.age,
        weight=user_data.weight,
        goal=user_data.goal,
        intensity=user_data.intensity
    )

    # Generate nutrition tip
    nutrition_tip = (
        generate_nutrition_tip_with_flash(
            user_data.goal
        )
    )

    # Save user
    saved_user = save_user(
        user_data
    )

    # Save plan
    save_plan(
        user_id=user_data.user_id,
        original_plan=workout_plan,
        nutrition_tip=nutrition_tip
    )

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "user": saved_user,
            "workout_plan": workout_plan,
            "nutrition_tip": nutrition_tip,
            "message": "Your 7-day fitness plan has been generated successfully.",
            "error": None
        }
    )


# ---------------------------------------------------------
# SUBMIT FEEDBACK
# ---------------------------------------------------------

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback(
    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...)
):

    user_id = user_id.strip()
    feedback = feedback.strip()

    # Find user
    user = get_user(
        user_id
    )

    if not user:

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "user": None,
                "workout_plan": None,
                "nutrition_tip": None,
                "message": None,
                "error": (
                    "User ID was not found. "
                    "Please enter a valid User ID."
                )
            }
        )

    # Find original plan
    plan = get_plan(
        user_id
    )

    if not plan:

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "user": user,
                "workout_plan": None,
                "nutrition_tip": None,
                "message": None,
                "error": (
                    "No workout plan was found "
                    "for this user."
                )
            }
        )

    # Generate updated plan
    updated_plan = update_workout_plan(
        original_plan=plan.original_plan,
        feedback=feedback,
        username=user.username,
        age=user.age,
        weight=user.weight,
        goal=user.goal,
        intensity=user.intensity
    )

    # Save updated plan
    update_plan(
        user_id=user_id,
        updated_plan=updated_plan,
        feedback=feedback
    )

    # New nutrition tip
    nutrition_tip = (
        generate_nutrition_tip_with_flash(
            user.goal
        )
    )

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "user": user,
            "workout_plan": updated_plan,
            "nutrition_tip": nutrition_tip,
            "message": (
                "Your workout plan has been "
                "updated successfully."
            ),
            "error": None
        }
    )


# ---------------------------------------------------------
# ADMIN / ALL USERS
# ---------------------------------------------------------

@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(
    request: Request
):

    users = get_all_users()

    plans = get_all_plans()

    # Latest plan for every user
    latest_plans = {}

    for plan in plans:

        if plan.user_id not in latest_plans:

            latest_plans[
                plan.user_id
            ] = plan

    return templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,
            "users": users,
            "plans": latest_plans
        }
    )