import sqlalchemy as sq
from .dhSetup import userBase


class User(userBase):
    __tablename__ = 'user'

    id: int = sq.Column('id', sq.Integer, primary_key=True, unique=True)
    identifier: str = sq.Column('identifier', sq.String(255))
    likes: dict = sq.Column('likes', sq.JSON, default={})
    dislikes: dict = sq.Column('dislikes', sq.JSON, default={})
    interested: dict = sq.Column('interested', sq.JSON, default={})
    uninterested: dict = sq.Column('uninterested', sq.JSON, default={})
    ignored: list = sq.Column('ignored', sq.JSON, default=[])

    def __init__(self, id: int, identifier: str = None):
        self.id = id
        self.identifier = identifier
