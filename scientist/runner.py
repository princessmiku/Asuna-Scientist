"""

    Diese Klasse ist eine mögliche start möglichkeiten.
    Diese ermöglicht ein einfaches Starten des ganzen systems für eine globale config

"""
from .search import DataScientist, LogSettings


class S2setup:

    def __init__(self, port: int):
        self.user_database: list = []
        self.s2data_databases: dict[str, list] = {}

    # add a database handler for users
    def addUserDB(self, servs=1):
        pass

    # add a search server
    def add2DSearchEngine(self, servs=1):
        pass

    def checkAlive(self) -> bool:
        return True

    # start all
    def run(self):
        pass

