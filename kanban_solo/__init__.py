from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    with app.app_context():
        from . import views

        #        db.drop_all()
        db.session.execute("CREATE DATABASE IF NOT EXISTS kanban_solo")
        db.create_all()

        return app
