from sqlalchemy import text

from kanban_solo import db


class Database:
    def __init__(self):
        pass

    @staticmethod
    def create(object_):
        db.session.add(object_)
        db.session.commit()

    @staticmethod
    def create_multiple(objects):
        for i in objects:
            db.session.add(i)
        db.session.commit()

    @staticmethod
    def get(type_, id_: int):
        return db.session.query(type_).get(id_)

    @staticmethod
    def search(type_, filter_: str = "", order_by: str = ""):
        return db.session.query(type_).filter(text(filter_)).order_by(text(order_by))

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(object_):
        db.session.delete(object_)
        db.session.commit()

    @staticmethod
    def delete_multiple(objects: list):
        for i in objects:
            db.session.delete(i)
        db.session.commit()

    @staticmethod
    def execute_stmt(stmt: str):
        db.session.add(stmt)
        db.session.commit()
