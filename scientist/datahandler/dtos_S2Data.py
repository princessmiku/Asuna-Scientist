import sqlalchemy as sq
from .dhSetup import s2Base


class Collection(s2Base):

    __tablename__ = 'collection'

    id: int = sq.Column('id', sq.Integer, autoincrement=True, unique=True, primary_key=True)
    identifier: str = sq.Column('identifier', sq.String(255), default="0")
    name: str = sq.Column('name', sq.String(255), nullable=False)
    category: list[str] = sq.Column('category', sq.JSON, default=[])
    extraSearch: str = sq.Column('extra_search', sq.Text)
    count: int = sq.Column('count', sq.Integer, default=0)
    relevance: int = sq.Column('relevance', sq.Integer, default=0)
    lastRelevance: list[int] = sq.Column('last_relevance', sq.JSON, default=[])
    ignore: bool = sq.Column('ignore', sq.Boolean, default=False)

    def __init__(self, id: int, identifier: str = "0"):
        self.id = id
        self.identifier = identifier

    def addCount(self, count: int = 1):
        self.count += count


class SearchConnections(s2Base):
    __tablename__ = 'search_connections'

    name: str = sq.Column('name', sq.String(127), primary_key=True, unique=True)
    data: dict = sq.Column('data', sq.JSON, default={})


class ConnectedCategorys(s2Base):
    __tablename__ = 'connected_categorys'

    name: str = sq.Column('name', sq.String, primary_key=True, unique=True)
    data: dict = sq.Column('data', sq.JSON, default={})
