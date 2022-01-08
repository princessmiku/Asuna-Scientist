"""
    Abstract Class for a database connector sample

    create your own database connector for your system

    Its possible to use all possible saving systems with a personal Connector

    Its use the sql structure


    you will get any time the structure of a multi request and you must return the result like a multi request.
    Its easy and better to handle
"""
from abc import ABC, abstractmethod


class DatabaseConnector(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get(self, table: str, columns: list[str], where: [list[int], list[str]] = None, fromWhere: str = "id") -> [list[list[any]]]:
        """
        Get data from your saving system
        :param table:
        :param columns:
        :param where: set of ids
        :param fromWhere:
        :return:
        """

    @abstractmethod
    def set(self, table: str, columns: list[str], values: list[list[any]], where: [list[int], list[str]], fromWhere: str = "id"):
        """
        Set data in your saving system
        :param table:
        :param columns:
        :param values:
        :param where: set of ids
        :param fromWhere:
        :return:
        """
        pass

    @abstractmethod
    def exists(self, table: str, _id: list[int, str]) -> list[bool]:
        """
        Check if data exists
        :param table:
        :param _id: id of the checked objekt
        :return: return true or fasle
        """
        pass

    @abstractmethod
    def exitsTable(self, table: str) -> bool:
        """
        Check if the table exists in the database
        :param table:
        :return:
        """
        pass


    @abstractmethod
    def insert(self, table: str, columns: list[str], values: list[list[any]]):
        """
        :param table:
        :param columns:
        :param values:
        :return:
        """
        pass


    @abstractmethod
    def insertOrUpdate(self, table: str, columns: list[str], values: list[list[any]], where: [list[int], list[str]], fromWhere: str = "id"):
        """

        :param table:
        :param columns:
        :param values:
        :param where:
        :param fromWhere:
        :return:
        """
        pass

    @abstractmethod
    def commit(self):
        """
        Commit your data
        if don't needed, pass it
        :return:
        """
        pass
