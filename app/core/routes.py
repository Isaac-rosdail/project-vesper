from flask import Blueprint, render_template, redirect, url_for
from app.core.database import db_session
from app.modules.tasks import repository as tasks_repo

# For reset_db route
from sqlalchemy import text
from flask import jsonify, flash, request
from app.seed_db import seed_db
from app.core.database import get_engine
from app.core.db_base import Base
from flask import current_app

# Date/Time-related imports
from datetime import datetime, timezone, time
from zoneinfo import ZoneInfo

main_bp = Blueprint('main', __name__, template_folder="templates")

@main_bp.route("/", methods=["GET"])
def home():

    try:
        # Set reference time once
        now = datetime.now(ZoneInfo("Europe/London"))

        # Today's 00:00 in Europe/London time
        start_of_day_local = datetime.combine(now.date(), time.min, tzinfo=ZoneInfo("Europe/London"))

        # Convert to UTC for DB comparison
        start_of_day_utc = start_of_day_local.astimezone(timezone.utc)
        
        # Get Tasks to pass Anchor Habits to display
        session = db_session()

        # Get all tasks
        tasks = tasks_repo.get_all_tasks(session)
        # List comprehension to filter anchor habits from tasks list
        anchor_habits = [
            task for task in tasks
            if task.type == "habit" and task.is_anchor
        ]

        return render_template(
            "index.html",
            tasks=tasks,
            now=now,
            start_of_day_utc=start_of_day_utc,
            anchor_habits = anchor_habits
        )
    finally:
        session.close()

@main_bp.route('/reset_db', methods=["POST"])
def reset_db():

    # See database.py for further comments here, but basically we need to add .remove() here.
    # Otherwise the session may:
    # - Be holding on to ORM mappings that are now invalid
    # - Think certain tables/metadata still exist
    # - Will definitely not be aware of drop_all() happening underneath it
    db_session.remove() # Closes current "converation" the db, but:
    # - other connections might still be open
    # - PostgreSQL won't let you drop tables if anyone is still "talking" to them
    # Since this .remove() didn't fix our issue of hanging/breaking our DB somehow, then the scoped session wasn't the primary cause
    # print("Reset db triggered.")
    # TO-DO: Lock this down after adding auth // maybe extract it into a utility function later too
    engine = get_engine(current_app.config) # Current app gives us access to the config within a request context

    # Drop all tables
    # Tries to delete all tables, but:
    # - If any connection is still using those tables, PostgreSQL will wait
    # - If it waits too long, it looks like your app is frozen/hanging
    Base.metadata.drop_all(bind=engine)

    # Recreate all tables
    Base.metadata.create_all(bind=engine)

    # Re-seed the database with seed_db function
    seed_db()

    # Add confirmation message via flash
    flash('Database has been reset successfully!', 'success')

    return redirect(request.referrer or url_for('index'))