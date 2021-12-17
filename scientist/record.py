"""
    Record / Data set

    Set of manipulable data with results

"""
# import local things
from .user import User
from .collection import Collection

# import python stuff
import logging
from typing import Optional


class Record:
    logger: logging.Logger = None

    # init record
    def __init__(self, searchText: str, data: dict, user: User, ignoredCollectionsIndex=None):
        self.searchText = searchText
        self.data = data
        self.user = user
        self.isResult = False
        self.result = 0
        if ignoredCollectionsIndex is None:
            ignoredCollectionsIndex = []
        self.ignoredCollectionsIndex = ignoredCollectionsIndex

    def setResult(self, index: int) -> bool:
        """
        Set the result
        :param index: index of the result
        :return: is successfully
        """
        if len(self.data) - 1 > index: return False
        self.isResult = True
        self.result = index
        return True

    # delete the result
    def clearResult(self) -> None:
        self.isResult = False
        self.result = 0

    # get the result obj
    def getResult(self) -> Optional[Collection]:
        if not self.isResult: return None
        return self.data[self.result]

    def getUser(self) -> User:
        return self.user

    def setSearchText(self, text: str):
        self.searchText = text

