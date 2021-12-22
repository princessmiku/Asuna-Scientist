"""
Collections

"""
import difflib, logging

defaultStructure = {
    "id": [0],
    "like": [0],
    "dislike": [0],
    "category": [0]
}


def getBaseCollectionDataDict(_id: int, name: str) -> dict:
    return {
        "id": _id,
        "name": name,
        "extraSearchs": "",
        "count": 0,
        "relevance": 0,
        "lastRelevance": [],
        "category": [],
        "identifikator": 0,
        "ignore": False
    }


class Collection:
    logger: logging.Logger = None

    def __init__(self, data: dict):
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.extraSearchs: str = data["extraSearchs"]
        self.count: int = data["count"]
        self.relevance: int = data["relevance"]
        self.last_relevance: list[int] = data["lastRelevance"]
        self.category: list[int] = data["category"]
        self.identifikator: int = data["identifikator"]
        self.ignore: bool = data["ignore"]

    def addCount(self, count: int = 1):
        self.count += count
