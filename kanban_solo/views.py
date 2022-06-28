from flask import current_app, render_template, request, url_for, redirect
from kanban_solo.models import Board, Task
import random
import datetime
from kanban_solo import db


@current_app.context_processor
def get_boards():
    return {"boards": Board.query.all()}


@current_app.route("/")
def index():
    return render_template("index.html")


@current_app.route("/create_board", methods=["POST"])
def create_board():
    _ = Board(
        name=request.form["name"].title(),
        date_added=datetime.datetime.now(),
        color="#{:06x}".format(random.randint(0, 0xFFFFFF)),
    )
    db.session.add(_)
    db.session.commit()

    return redirect(url_for("board", id_=_.id))


@current_app.route("/board")
def board():
    board_ = Board.query.get(int(request.args.get("id_")))
    return render_template("board.html", board_=board_)


@current_app.route("/delete_board")
def delete_board():
    board_ = Board.query.get(int(request.args.get("id_")))

    for i in board_.tasks:
        db.session.delete(i)
    db.session.delete(board_)
    db.session.commit()

    return redirect(url_for("index"))


@current_app.route("/create_task", methods=["POST"])
def create_task():
    _ = Task(
        description=request.form["description"].capitalize(),
        status=request.form["status"],
        note=request.form["note"],
        date_added=datetime.datetime.now(),
        board=int(request.args.get("id_")),
    )
    db.session.add(_)
    db.session.commit()

    if request.form["subtask"]:
        _sub = Task(
            description=request.form["subtask"].capitalize(),
            date_added=datetime.datetime.now(),
            board=int(request.args.get("id_")),
            parent_task=_.id,
        )
        db.session.add(_sub)
        db.session.commit()

    return redirect(request.referrer)


@current_app.route("/edit_task", methods=["POST"])
def edit_task():
    task_ = Task.query.get(int(request.args.get("id_")))
    task_.description = request.form["description"]
    task_.status = request.form["status"]
    db.session.commit()

    return redirect(request.referrer)


@current_app.route("/mark_task")
def mark_task():
    task_ = Task.query.get(int(request.args.get("id_")))
    task_.status = "DONE" if not task_.status == "DONE" else "TODO"

    db.session.commit()

    return redirect(request.referrer)


@current_app.route("/delete_task")
def delete_task():
    task_ = Task.query.get(int(request.args.get("id_")))

    for i in task_.subtasks:
        db.session.delete(i)
    db.session.delete(task_)
    db.session.commit()

    return redirect(request.referrer)
