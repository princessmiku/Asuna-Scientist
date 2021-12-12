"""
Setup categories names

example categories
"""
from typing import Optional

# 0 is the default category when no is defined or found
import pandas

categories = {
    0: "unidentified",
    1: "entertainment",
    2: "technology",
    3: "learning"
}


class Category:

    def __init__(self, data: pandas.DataFrame):
        self.__data: pandas.DataFrame = data

    def getData(self):
        return self.__data

    def addCategory(self, name: str) -> int:
        pass

    def getIdByName(self, name: str) -> int:
        """
        Get the category id by the category name
        :param name: category name
        :return: id of the category
        """
        try:
            return list(categories.keys())[list(categories.values()).index(name)]
        except KeyError:
            return 0

    def getNameById(self, id: int) -> str:
        """
        Get the category name with the id
        :param id: id of the category
        :return: category name
        """
        try:
            return categories[id]
        except KeyError:
            return categories[0]

