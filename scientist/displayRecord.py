"""
    A simple Class for display records

"""
# Own Stuff
from .record import Record
from .collection import Collection

# python stuff
import math


class DRec:

    def __init__(self, _record: Record, maxShows: int = 25):
        """
        Init a display lib
        :param _record:
        :param maxShows: set the amount of shows which you get with "get"
        """
        self._record: Record = _record
        self.maxShows: int = maxShows
        self.currentIndex: int = 0
        self.lenOfData: int = len(self._record.data)
        self.currentPage: int = 0
        self.maxPages: int = math.ceil(self.lenOfData / maxShows)

    # get values in the range of the maxShows
    def get(self) -> list[Collection]:
        """
        Get Content of the record in the current range
        :return: the list with collection in the range of the show
        """
        showUp: int = self.currentIndex + self.maxShows
        if self.lenOfData > showUp:
            showUp -= showUp - self.lenOfData
        return self._record.data[self.currentIndex:showUp]

    # next page, or next page with skip xxx pages
    def nextPage(self, amount: int =1) -> bool:
        """
        Go to the next page, with or without skip pages
        :param amount: amount of skips, normal 1, 1 = next page
        :return: is successful, nice to have but it can be useless
        """
        if self.currentPage + amount > self.maxPages: return False
        self.currentPage += amount
        self.currentIndex += self.maxShows * amount
        if self.currentIndex > self.lenOfData: self.currentIndex = self.lenOfData
        return True

    # previous page, or previous page with skip xxx pages
    def previousPage(self, amount: int = 1) -> bool:
        """
        Go to the previous page, with or without skip pages
        :param amount: amount of skips, normal 1, 1 = next page
        :return: is successful, nice to have but it can be useless
        """
        if self.currentPage + amount < 0: return False
        self.currentPage -= amount
        self.currentIndex -= self.maxShows * amount
        if self.currentIndex < 0: self.currentIndex = 0
        return True

    # count the index up
    def addIndex(self, amount: int = 1) -> bool:
        """
        Add a amount on the index
        :param amount:
        :return: is successful, nice to have but it can be useless
        """
        if self.lenOfData > self.currentIndex + amount: return False
        self.currentIndex += amount
        return True

    # count the index down
    def removeIndex(self, amount: int = 1) -> bool:
        """
        Remove a amount on the index
        :param amount:
        :return: is successful, nice to have but it can be useless
        """
        if self.currentIndex - amount < 0: return False
        self.currentIndex -= amount
        return True
