# from uuid import uuid4

from sqlalchemy import Column, String, UnicodeText

from bot.sql import BASE, SESSION


class bugs(BASE):
    __tablename__ = 'bug'
    id = Column(String(8), primary_key=True)
    bug = Column(UnicodeText, nullable=False)

    def __init__(self, id, bug):
        self.id = str(id)
        self.bug = bug


def add_bug(id, bug):
    bug = bugs(str(id), bug)
    SESSION.add(bug)
    SESSION.commit()


def get_bugs():
    try:
        return SESSION.query(bugs).all()
    finally:
        SESSION.close()


def get_bug_id(get_id):
    try:
        return SESSION.query(bugs).get(str(get_id))
    finally:
        SESSION.close()


def rem_bugs(id):
    bug = SESSION.query(bugs).get(id)
    SESSION.delete(bug)
    SESSION.commit()


bugs.__table__.create(checkfirst=True)
