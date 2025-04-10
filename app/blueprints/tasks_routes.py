from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from app.database import get_db_session
from flask import current_app

# Import Task model
from app.modules.tasks.models import Task

# Import Task repository
from app.modules.tasks import repository as tasks_repo

# For created_at / completed_at
from datetime import datetime, timezone

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/tasks")
def tasks():

    # Fetch Tasks & pass into template
    session = get_db_session()
    # Column names for Task model
    task_column_names = [
        Task.COLUMN_LABELS.get(col, col)
        for col in Task.__table__.columns.keys()
    ]

    tasks = tasks_repo.get_all_tasks(session)

    return render_template("tasks/tasks.html",
                           task_column_names = task_column_names,
                           tasks = tasks)

# Create a new task
@tasks_bp.route("/add_task", methods=["GET", "POST"])
def add_task():

    # Process form data and add new task to db
    if request.method == "POST":

        # Parse & sanitize form data
        task_data = {
            "title": request.form.get("title"),
            "type": request.form.get("type"),
            # Value for checkbox is irrelevant
            # If checked, then value is not None, so bool=True (ie, it exists)
            # Otherwise it is None, in which case bool=False 
            "is_anchor": bool(request.form.get("is_anchor"))
        }
        # Creating new task Task object
        new_task = Task(
            title=task_data["title"],
            type=task_data["type"],
            is_done=False,
            is_anchor=task_data["is_anchor"],
            created_at=datetime.now(timezone.utc),
            completed_at=None
        )

        # Add new_task to db
        session = get_db_session()
        session.add(new_task)
        session.commit()

        return render_template("tasks/tasks.html")
    else:
        return render_template("tasks/add_task.html")
    
@tasks_bp.route("/complete_task/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    session = get_db_session()
    #print(f"Session in route: {id(session)}")
    # Get corresponding task from db  
    task = session.get(Task, task_id)

    # Update task to be completed, incl. completed_at
    task.is_done = True
    task.completed_at = datetime.now(timezone.utc)
    session.commit()

    return jsonify(success=True)