"""
customisable database connector

Allows you to create the storage behavior completely yourself

"""
import sqlite3, logging


class DatabaseConnector:
    logger: logging.Logger = None

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
