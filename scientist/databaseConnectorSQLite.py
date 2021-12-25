"""
customisable database connector

Allows you to create the storage behavior completely yourself

"""
from os import PathLike
from typing import Union

from .databaseConnector import DatabaseConnector
import sqlite3, logging


class DCSqlite(DatabaseConnector):

    def __init__(self, location: str):
        super().__init__()
        self.database: sqlite3.Connection = sqlite3.connect(location)

    def get(self, table: str, columns: list[str], where: [list[int], list[str]] = None, fromWhere: str = "id") -> [list[list[any]]]:
        # build the sql str
        sql_str: str = "SELECT "
        sql_str += ", ".join(columns)
        sql_str += " FROM " + table
        if where:
            if isinstance(where[0], int):

                sql_str += f" WHERE {fromWhere} IN ({', '.join([str(aint) for aint in where])})"
            else:
                sql_str += f" WHERE {fromWhere} IN ('" + "', '".join(where) + "')"
        return self.database.execute(sql_str).fetchall()

    def set(self, table: str, columns: list[str], values: list[list[any]], where: [list[int], list[str]], fromWhere: str = "id"):
        # build the sql str
        sql_str: str = ""
        c: int
        w: [int, str]
        for c, w in enumerate(where):
            sql_str += f"UPDATE {table} SET "
            saving_values: list[str] = []
            for z in zip(columns, values[c]):
                if isinstance(z[1], int):
                    saving_values.append(f"{z[0]} = {z[1]}")
                else:
                    saving_values.append(f"{z[0]} = '{z[1]}'")
            sql_str += ", ".join(saving_values)
            if isinstance(w, int):
                sql_str += f" WHERE {fromWhere} = {w}"
            else:
                sql_str += f" WHERE {fromWhere} = '{w}'"
            sql_str += ";\n"
        self.database.executescript(sql_str)
        self.commit()



    def exists(self, table: str, _id: list[int, str]) -> list[bool]:
        pass

    def insert(self, table: str, columns: list[str], values: list[list[any]]):
        # build the sql string
        sql_str = ""
        for entry in values:
            sql_str += f"INSERT OR IGNORE INTO '{table}' ('" + "', '".join(columns) + "') VALUES ("
            entry: list[any]
            insertData = []
            for v in entry:
                if isinstance(v, int):
                    insertData.append(str(v))
                else:
                    insertData.append(f"'{v}'")
            sql_str += ", ".join(insertData)
            sql_str += ");\n"
        print(sql_str)
        self.database.executescript(sql_str)
        self.commit()

    def commit(self):
        self.database.commit()


class DCSqliteOLD(DatabaseConnector):


    logger: logging.Logger = None

    def __init__(self, location: str, autoCommit: bool = True):
        super().__init__()
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

    def exists(self, table: str, _id: int) -> bool:
        pass

    def insert(self, **kwargs):
        pass

