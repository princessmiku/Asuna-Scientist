"""
Collections

"""
from .category import Category

import difflib, logging

defaultStructure = {
    "id": [0],
    "like": [0],
    "dislike": [0],
    "category": [0]
}


def getBaseCollectionDataDict(name: str) -> dict:
    return {
        "name": name,
        "count": 0,
        "relevance": 0,
        "lastRelevance": [],
        "category": [],
        "ignore": False
    }


class Collection:
    logger: logging.Logger = None

    def __init__(self, data: dict):
        self.name: str = data["name"]
        self.count: int = data["count"]
        self.relevance: int = data["relevance"]
        self.last_relevance: list[int] = data["lastRelevance"]
        self.category: list[int] = data["category"]
        self.ignore: bool = data["ignore"]


    def getCategorys(self) -> list[Category]:
        self.category = []
        return self.category

    def addCount(self, count: int = 1):
        self.count += count
