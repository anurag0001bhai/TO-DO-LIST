from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import uuid

app = Flask(__name__)

# ============================================================
# DATABASE CONFIGURATION
# ============================================================

database_url = os.environ.get("DATABASE_URL")

# Render/PostgreSQL compatibility
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )

if database_url:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
else:
    # Local development database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ============================================================
# DATABASE MODEL
# ============================================================

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    title = db.Column(
        db.String(500),
        nullable=False
    )

    completed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

with app.app_context():
    db.create_all()


# ============================================================
# USER IDENTIFICATION
# ============================================================

def get_user_id():
    """
    Give each browser a unique ID.

    This allows different users/browsers to have
    separate to-do lists without requiring accounts.
    """

    from flask import session

    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())

    return session["user_id"]


app.secret_key = os.environ.get(
    "SECRET_KEY",
    "development-secret-key-change-this"
)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():

    user_id = get_user_id()

    tasks = Task.query.filter_by(
        user_id=user_id
    ).order_by(
        Task.id.desc()
    ).all()

    completed = sum(
        1 for task in tasks if task.completed
    )

    pending = len(tasks) - completed

    return render_template(
        "index.html",
        tasks=tasks,
        completed=completed,
        pending=pending,
        total=len(tasks)
    )


# ============================================================
# ADD TASK
# ============================================================

@app.route("/add", methods=["POST"])
def add_task():

    title = request.form.get("title", "").strip()

    if title:

        task = Task(
            user_id=get_user_id(),
            title=title,
            completed=False
        )

        db.session.add(task)
        db.session.commit()

    return redirect(url_for("index"))


# ============================================================
# COMPLETE / UNCOMPLETE TASK
# ============================================================

@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=get_user_id()
    ).first_or_404()

    task.completed = not task.completed

    db.session.commit()

    return redirect(url_for("index"))


# ============================================================
# DELETE TASK
# ============================================================

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=get_user_id()
    ).first_or_404()

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for("index"))


# ============================================================
# EDIT TASK
# ============================================================

@app.route("/edit/<int:task_id>", methods=["POST"])
def edit_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=get_user_id()
    ).first_or_404()

    title = request.form.get("title", "").strip()

    if title:
        task.title = title
        db.session.commit()

    return redirect(url_for("index"))


# ============================================================
# SEARCH
# ============================================================

@app.route("/search")
def search():

    user_id = get_user_id()

    keyword = request.args.get(
        "q",
        ""
    ).strip()

    if keyword:

        tasks = Task.query.filter(
            Task.user_id == user_id,
            Task.title.ilike(f"%{keyword}%")
        ).order_by(
            Task.id.desc()
        ).all()

    else:

        tasks = Task.query.filter_by(
            user_id=user_id
        ).order_by(
            Task.id.desc()
        ).all()

    completed = sum(
        1 for task in tasks if task.completed
    )

    pending = len(tasks) - completed

    return render_template(
        "index.html",
        tasks=tasks,
        completed=completed,
        pending=pending,
        total=len(tasks),
        search=keyword
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
