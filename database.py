from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime
)

from sqlalchemy.orm import declarative_base, sessionmaker

from .config import DATABASE_URL


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# ---------------------------------------------------------
# USER TABLE
# ---------------------------------------------------------

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    username = Column(
        String(100),
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    weight = Column(
        Float,
        nullable=False
    )

    goal = Column(
        String(100),
        nullable=False
    )

    intensity = Column(
        String(20),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ---------------------------------------------------------
# PLAN TABLE
# ---------------------------------------------------------

class Plan(Base):

    __tablename__ = "plans"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String(100),
        index=True,
        nullable=False
    )

    original_plan = Column(
        Text,
        nullable=False
    )

    updated_plan = Column(
        Text,
        nullable=True
    )

    nutrition_tip = Column(
        Text,
        nullable=True
    )

    feedback = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ---------------------------------------------------------
# CREATE TABLES
# ---------------------------------------------------------

def init_db():

    Base.metadata.create_all(
        bind=engine
    )


# ---------------------------------------------------------
# SAVE USER
# ---------------------------------------------------------

def save_user(data):

    db = SessionLocal()

    try:

        existing_user = (
            db.query(User)
            .filter(
                User.user_id == data.user_id
            )
            .first()
        )

        if existing_user:

            existing_user.username = data.username
            existing_user.age = data.age
            existing_user.weight = data.weight
            existing_user.goal = data.goal
            existing_user.intensity = data.intensity

            db.commit()
            db.refresh(existing_user)

            return existing_user

        new_user = User(
            user_id=data.user_id,
            username=data.username,
            age=data.age,
            weight=data.weight,
            goal=data.goal,
            intensity=data.intensity
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user

    finally:

        db.close()


# ---------------------------------------------------------
# SAVE PLAN
# ---------------------------------------------------------

def save_plan(
    user_id,
    original_plan,
    nutrition_tip
):

    db = SessionLocal()

    try:

        new_plan = Plan(
            user_id=user_id,
            original_plan=original_plan,
            nutrition_tip=nutrition_tip
        )

        db.add(new_plan)

        db.commit()

        db.refresh(new_plan)

        return new_plan

    finally:

        db.close()


# ---------------------------------------------------------
# GET USER
# ---------------------------------------------------------

def get_user(user_id):

    db = SessionLocal()

    try:

        return (
            db.query(User)
            .filter(
                User.user_id == user_id
            )
            .first()
        )

    finally:

        db.close()


# ---------------------------------------------------------
# GET LATEST PLAN
# ---------------------------------------------------------

def get_plan(user_id):

    db = SessionLocal()

    try:

        return (
            db.query(Plan)
            .filter(
                Plan.user_id == user_id
            )
            .order_by(
                Plan.id.desc()
            )
            .first()
        )

    finally:

        db.close()


# ---------------------------------------------------------
# GET ORIGINAL PLAN
# ---------------------------------------------------------

def get_original_plan(user_id):

    plan = get_plan(user_id)

    if plan:

        return plan.original_plan

    return None


# ---------------------------------------------------------
# UPDATE PLAN
# ---------------------------------------------------------

def update_plan(
    user_id,
    updated_plan,
    feedback
):

    db = SessionLocal()

    try:

        plan = (
            db.query(Plan)
            .filter(
                Plan.user_id == user_id
            )
            .order_by(
                Plan.id.desc()
            )
            .first()
        )

        if plan:

            plan.updated_plan = updated_plan
            plan.feedback = feedback

            db.commit()
            db.refresh(plan)

        return plan

    finally:

        db.close()


# ---------------------------------------------------------
# GET ALL USERS
# ---------------------------------------------------------

def get_all_users():

    db = SessionLocal()

    try:

        return (
            db.query(User)
            .order_by(
                User.id.desc()
            )
            .all()
        )

    finally:

        db.close()


# ---------------------------------------------------------
# GET ALL PLANS
# ---------------------------------------------------------

def get_all_plans():

    db = SessionLocal()

    try:

        return (
            db.query(Plan)
            .order_by(
                Plan.id.desc()
            )
            .all()
        )

    finally:

        db.close()