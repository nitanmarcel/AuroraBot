# from uuid import uuid4

from sqlalchemy import Column, String, UnicodeText

from bot.sql import BASE, SESSION


class suggs(BASE):
    __tablename__ = 'suggestions'
    id = Column(String(8), primary_key=True)
    suggestion = Column(UnicodeText, nullable=False)

    def __init__(self, id, suggestion):
        self.id = str(id)
        self.suggestion = suggestion


def add_suggestion(id, suggestion):
    suggestion = suggs(str(id), suggestion)
    SESSION.add(suggestion)
    SESSION.commit()


def get_suggestions():
    try:
        return SESSION.query(suggs).all()
    finally:
        SESSION.close()


def get_suggestions_id(get_id):
    try:
        return SESSION.query(suggs).get(str(get_id))
    finally:
        SESSION.close()


def rem_suggestions(id):
    suggestion = SESSION.query(suggs).get(id)
    SESSION.delete(suggestion)
    SESSION.commit()


suggs.__table__.create(checkfirst=True)
