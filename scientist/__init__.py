"""
    Example Text
    https://www.blindtextgenerator.de/
"""
# Own library's
from . import collection, user
# external library's
import difflib, itertools, sqlite3, threading, re, pandas as pd

import pandas


class DatabaseConnector:

    def __init__(self, location: str, autoCommit: bool = True):
        self.database: sqlite3.Connection = sqlite3.connect(location)
        self.autoCommit: bool = autoCommit

    def get(self, table: str, columns: [str, list], where: list = False) -> list:
        # build the sql str
        sql_str: str = f"SELECT "
        if isinstance(columns, list):
            sql_str += ", ".join(columns)
        else:
            sql_str += columns
        sql_str += f" FROM {table}"
        if where:
            if isinstance(where[1], str):
                sql_str += f" WHERE '{where[1]}'"
            else:
                sql_str += f" WHERE {str(where[1])}"
        return self.database.execute(sql_str).fetchall()

    def set(self, table: str, columns: [str, list], values: [str, list], where: list = False):
        # build the sql str
        sql_str: str = f"UPDATE {table} SET "
        if isinstance(columns, list):
            saving_values: list = []
            for z in zip(columns, values):
                if isinstance(z[0], str):
                    saving_values.append(f"{z[0]} = '{z[1]}'")
                else:
                    saving_values.append(f"{z[0]} = {z[1]}")
            sql_str += ", ".join(saving_values)
        else:
            sql_str += columns + ", " + values
        sql_str += f" FROM {table}"
        if where:
            if isinstance(where[1], str):
                sql_str += f" WHERE '{where[1]}'"
            else:
                sql_str += f" WHERE {str(where[1])}"
        self.database.execute(sql_str).fetchall()

        # commit automatically new data
        if self.autoCommit: self.commit()

    def commit(self):
        self.database.commit()


class DataScientist:

    def __init__(self):
        self.__data: dict = {}
        self.__generate_default_structure()

    def __generate_default_structure(self):
        """
        This function generate the default used structure for saving
        :return:
        """

        self.__data["collection"] = pandas.DataFrame(collection.defaultStructure)
        self.__data["user"] = pandas.DataFrame(user.defaultStructure)

    def newSaveLocation(self, name: str, data: dict = None) -> None:
        self.__data[name] = pandas.DataFrame(data)

    # data manager

    def get(self, location: str) -> [int, str, bool]:
        #location: list = re.split(r"[.]+\b(?<!\\.)", location)
        pass

    def set(self, location: str, data: [int, str, bool]):
        #location: list = re.split(r"[.]+\b(?<!\\.)", location)
        pass

    def exists(self, location: str) -> bool:
        #location: list = re.split(r"[.]+\b(?<!\\.)", location)
        pass


    def remove(self, location: str):
        #location: list = re.split(r"[.]+\b(?<!\\.)", location)
        pass

    # core

    def insert(self):
        pass

    def addElement(self):
        pass

    def removeElement(self):
        pass

    # getter setter
    def getData(self) -> dict:
        return self.__data

    # extras

    def save(self) -> bool:
        pass

    @staticmethod
    def waitFinish(threadList: list):
        """
        This function is a easy way for waiting that the threads are finished
        :param threadList: a list with threads
        :return:
        """
        t: threading.Thread
        for t in threadList:
            t.join()
