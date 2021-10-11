"""
    Example Text
    https://www.blindtextgenerator.de/
"""
import collections
import difflib
import itertools, sqlite3, threading, re

from .collection import Collection


class DatabaseConnector:

    def __init__(self, location: str, autoCommit: bool = True):
        self.database: sqlite3.Connection = sqlite3.connect(location)
        self.autoCommit: bool = autoCommit

    def get(self, table: str, columns: [str, list], where: list[str, (str, int)] = False) -> list:
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

    def set(self, table: str, columns: [str, list], values: [str, list], where: list[str, (str, int)] = False):
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

    def __init__(self, connector: DatabaseConnector, saveDataLocal: bool = True):
        """
        :param connector: connector of the database
        :param saveDataLocal: Daten werden beim starten einmal geladen und
        anschließend immer in einem Dict abgespeichert, daten werden nicht erneut aus der datenbank gezogen
        """
        self.connector: DatabaseConnector = connector
        self.data: dict = {}
        self.Collection = Collection
        self.Collection.dataScientist = self

    def pointLocationConverter(self, step: str):
        return step.replace(".", "\&!")

    def get(self, location: str) -> [int, str, bool]:
        """
        Get Data
        :param location: data path
        :return: returns data
        """
        location: list = re.split(r"[.]+\b(?<!\\.)", location)
        data: any = self.data
        loc: any
        for step in location:
            if not isinstance(data, dict): break
            if not data.__contains__(step): return None
            data = data[step]
        return data

    def set(self, location: str, data: [int, str, bool]):
        """
        Set specific data
        :param location:
        :param data:
        :return:
        """
        location: list = re.split(r"[.]+\b(?<!\\.)", location)
        save = self.data
        for count, step in enumerate(location):
            if count != len(location) - 1:
                if not save.__contains__(step): save[step] = {}
                save = save[step]
            else:
                save[step] = data

    def exists(self, location: str) -> bool:
        """
        Get Data
        :param location: data path
        :return: returns data
        """
        location: list = re.split(r"[.]+\b(?<!\\.)", location)
        data: any = self.data.copy()
        if not data.__contains__(location[0]): return False
        loc: any
        for step in location:
            if not data.__contains__(step): return False
            data = data[step]
        return True

    def save(self) -> bool:
        """
        Save your data
        :return: is successful
        """
        return True

    def insert(self, text: str, save_under: str = "collection", replacer: list = [], startAsThread: bool = False) -> [None, threading.Thread]:
        """

        :param startAsThread:
        :param replacer:
        :param save_under:
        :param text:
        :return:
        """

        def run(text):
            for re in replacer:
                text = text.replace(re[0], re[1])
            words: list = text.split(" ")
            for word in words:
                word = word.replace(".", "\.")
                if not self.exists(f"{save_under}.{word}"):
                    col = self.Collection(word, save_under)
                else:
                    col = self.get(f"{save_under}.{word}.self")
                col.addCount()
        if not startAsThread:
            run(text)
            return None
        else:
            thread = threading.Thread(target=run, args=(text,), daemon=True)
            thread.start()
            return thread

    def addAInsert(self, text: str, save_under: str = "collection", **kwargs) -> Collection:
        word = text.replace(".", "\.")
        if not self.exists(f"{save_under}.{word}"):
            col = self.Collection(word, save_under, **kwargs)
        else:
            col = self.get(f"{save_under}.{word}.self")
        col.addCount()
        return col

    def getMatch(self, search: str, location: [str, list], max_matches: int = 1) -> [bool, str]:
        """
        Suche nach einen Match in der angegeben location, die suche muss nicht einstimmig geschrieben sein,
        es wird ein passendes ergebnis zu finden. Um ein absolutes match zu finden sollte man exists nutzen.

        :param search:
        :param location:
        :return: Das Match oder None wenn nix gefunden wurde
        """
        if isinstance(location, str):
            get_dict: dict = self.get(location)
            if not isinstance(get_dict, dict): return []
            search_match: list = difflib.get_close_matches(search, get_dict.keys(), max_matches)
            if search_match:
                return_list = []
                for match in search_match:
                    return_list.append(get_dict[match])
                return return_list
        elif isinstance(location, list):
            get_dict: dict = {}
            col: Collection
            for col in location:
                get_dict[col.name] = col
            search_match: list = difflib.get_close_matches(search, get_dict.keys(), max_matches)
            if search_match:
                return_list = []
                for match in search_match:
                    return_list.append(get_dict[match])
                return return_list
        return []

    def getCollectionsByRelevanceHigherThen(self, relevance: int, location: [str, list]) -> list:
        is_relevance: list = []
        if isinstance(location, str):
            if not self.exists(location): return []
            objects: dict = self.get(location)
            for o in objects:
                if not self.exists(f"{location}.{o}.self"): continue
                col: Collection = self.get(f"{location}.{o}.self")
                if col.relevance >= relevance: is_relevance.append(col)
        elif isinstance(location, list):
            col: Collection
            for col in location:
                if col.relevance >= relevance: is_relevance.append(col)
        return is_relevance

    def getCollectionsByLastRelevanceCount(self, relevance: int, location: [str, list]) -> list:
        is_relevance: list = []
        if isinstance(location, str):
            if not self.exists(location): return []
            objects: dict = self.get(location)
            is_relevance: list = []
            for o in objects:
                if not self.exists(f"{location}.{o}.self"): continue
                col: Collection = self.get(f"{location}.{o}.self")
                if col.get_last_relevance_count() >= relevance: is_relevance.append(col)
        elif isinstance(location, list):
            col: Collection
            for col in location:
                if col.get_last_relevance_count() >= relevance: is_relevance.append(col)
        return is_relevance

    def getCollectionsByCategory(self, category: [str, list], location: [str, list]) -> list:
        category_objects: list = []
        if isinstance(location, str):
            if not self.exists(location): return []
            objects: dict = self.get(location)
            if isinstance(category, str): category = [category]
            for o in objects:
                if not self.exists(f"{location}.{o}.self"): continue
                col: Collection = self.get(f"{location}.{o}.self")
                if col.have_category(category): category_objects.append(col)
        elif isinstance(location, list):
            if isinstance(category, str): category = [category]
            col: Collection
            for col in location:
                if col.have_category(category): category_objects.append(col)
        return category_objects

    def getSearchCollections(self, to_search: str, location: [str, list]) -> dict:
        """
        Diese funktion sucht aus angegeben den parametern das passende ergebnis
        - name
        - category
        - search text

        Sortiert nach der Allgemeinen Relevanz des Produktes und angeschlagen den Suchkriterien

        Sollte ein Produkt auf ignore stehen wird dieses Systematisch ausgeschlossen
        :param to_search:
        :param location:
        :return: eine liste mit den gefundenen Collections
        """

        if isinstance(location, list):
            data = location
        else:
            get_dict = self.get(location)
            data = []
            for x in get_dict:
                if self.exists(f"{location}.{x}.self"): data.append(self.get(f"{location}.{x}.self"))

        matches = {
            "name": [],
            "category": [],
            "other": []
        }
        col: Collection
        threads = []
        for col in data:
            def run():
                searched = set(to_search.split(" "))
                split_name = col.name.split(" ")
                search_text = col.get_search_text()
                founded_names = []
                founded_category = []
                founded_others = []
                for s in searched:
                    match = difflib.get_close_matches(s, split_name)  # search in name
                    if match:
                        founded_names += match
                    if col.have_category_searching(s):  # search in category
                        founded_category.append(s)
                    match = difflib.get_close_matches(s, search_text)  # search in search text
                    if match:
                        founded_others.append(match)
                if len(founded_names) / len(split_name) >= 0.5:
                    matches["name"].append(col)
                if founded_category:
                    matches["category"].append(col)
                if len(founded_others) / len(search_text) >= 0.15:
                    matches["other"].append(col)
            # Starten als Thread für die schnellere suche
            thread = threading.Thread(target=run, daemon=True)
            thread.start()
            threads.append(thread)
        self.waitFinish(threads)
        relevance_one = []
        relevance_two = []
        relevance_three = []

        threads.clear()

        def matches_for_name():
            for col in matches["name"]:
                if matches["name"].__contains__(col) and matches["category"].__contains__(col) and matches["other"].__contains__(col):
                    relevance_one.append(col)
                elif matches["name"].__contains__(col) and matches["category"].__contains__(col) and not matches["other"].__contains__(col):
                    relevance_one.append(col)
                elif matches["name"].__contains__(col):
                    relevance_two.append(col)
        threads.append(threading.Thread(target=matches_for_name, daemon=True))

        def matches_for_category():
            for col in matches["category"]:
                if not matches["name"].__contains__(col) and matches["category"].__contains__(col) and matches["other"].__contains__(col):
                    relevance_two.append(col)
                elif not matches["name"].__contains__(col) and matches["category"].__contains__(col) and not matches["other"].__contains__(col):
                    relevance_two.append(col)
        threads.append(threading.Thread(target=matches_for_category, daemon=True))

        def matches_for_other():
            for col in matches["other"]:
                if not matches["name"].__contains__(col) and not matches["category"].__contains__(col) and not matches["other"].__contains__(col):
                    relevance_three.append(col)
        threads.append(threading.Thread(target=matches_for_other, daemon=True))
        for thread in threads:
            thread.start()
        self.waitFinish(threads)

        def sortFunc(col: Collection):
            return col.relevance_count()
        relevance_one.sort(key=sortFunc, reverse=True)
        relevance_two.sort(key=sortFunc, reverse=True)
        relevance_three.sort(key=sortFunc, reverse=True)
        sorted_return: list = relevance_one + relevance_two + relevance_three
        return sorted_return

    def waitFinish(self, threadList: list):
        """
        :param threadList:
        :return:
        """
        t: threading.Thread
        for t in threadList:
            t.join()