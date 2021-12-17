"""
Setup categories names

example categories
"""

import logging
from typing import Optional

# 0 is the default category when no is defined or found

categories = {
    "id": range(4),
    "name": ["unidentified", "entertainment", "technology", "learning"]
}


class Category:
    logger: logging.Logger = None

    def __init__(self, data: dict):
        self.logger.debug("Init Categorys")
        self.__data: dict = data

    def getData(self):
        """
        get The Private Data
        :return:
        """
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

