from kanban_solo import db


class Board(db.Model):
    __tablename__ = "boards"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    color = db.Column(db.Text)
    date_added = db.Column(db.DateTime)
    tasks = db.relationship("Task", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)

    def get_todo(self):
        return self.tasks.filter(Task.parent_task == None, Task.status == "Todo")

    def get_doing(self):
        return self.tasks.filter(Task.parent_task == None, Task.status == "Doing")

    def get_done(self):
        return self.tasks.filter(Task.parent_task == None, Task.status == "Done")


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    note = db.Column(db.Text)
    status = db.Column(db.Text, default="Todo")
    date_added = db.Column(db.DateTime)
    board = db.Column(db.Integer, db.ForeignKey("boards.id"))
    parent_task = db.Column(db.Integer, db.ForeignKey("tasks.id"))
    subtasks = db.relationship("Task", lazy="dynamic")

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)

    def get_subtasks(self, filter_: str = None):
        return self.subtasks.filter(db.text(filter_))

    def get_subtasks_progress(self):
        done = self.subtasks.filter(Task.status == "Done").count()
        total = self.subtasks.count()
        return "%s of %s subtasks" % (done, total)
