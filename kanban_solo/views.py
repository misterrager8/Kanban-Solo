from flask import current_app, render_template, request, url_for, redirect
from kanban_solo.models import Board, Task
import random
import datetime
from kanban_solo.database import Database

db = Database()


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
    db.create(_)

    return redirect(url_for("board", id_=_.id))


@current_app.route("/board")
def board():
    board_ = Board.query.get(int(request.args.get("id_")))
    return render_template("board.html", board_=board_)


@current_app.route("/delete_board")
def delete_board():
    board_ = Board.query.get(int(request.args.get("id_")))

    db.delete_multiple(board_.tasks)
    db.delete(board_)

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
    db.create(_)

    if request.form["subtask"]:
        db.create_multiple(
            [
                Task(
                    description=i.capitalize(),
                    date_added=datetime.datetime.now(),
                    board=int(request.args.get("id_")),
                    parent_task=_.id,
                )
                for i in request.form.getlist("subtask")
            ]
        )

    return redirect(request.referrer)


@current_app.route("/edit_task", methods=["POST"])
def edit_task():
    task_ = Task.query.get(int(request.args.get("id_")))
    task_.status = request.form["status"]
    if task_.status == "Done":
        for i in task_.subtasks:
            i.status = "Done"
    db.update()

    return redirect(request.referrer)


@current_app.route("/mark_task")
def mark_task():
    task_ = Task.query.get(int(request.args.get("id_")))
    task_.status = "Done" if not task_.status == "Done" else "Todo"

    db.update()

    return redirect(request.referrer)


@current_app.route("/delete_task")
def delete_task():
    task_ = Task.query.get(int(request.args.get("id_")))

    db.delete_multiple(task_.subtasks)
    db.delete(task_)

    return redirect(request.referrer)
