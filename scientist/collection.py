import collections
import difflib


class Collection:
    dataScientist = None
    max_last_relevance = 10

    def __init__(self, name: str, save_under: str = "collection", category: list = [], id: int = 0):
        self.name: str = name
        self.id = id
        self.save_under = save_under
        self.count: int = 0
        self.relevance: int = 0
        self.forced_relevance: bool = False
        self.ignore: bool = False
        self.all_delivered_relevance: int = 0
        self.last_relevance: list = []
        self.category: list = category
        self.dataScientist.set(f"{self.save_under}.{self.name}.self", self)
        self.search_text = ""

    def add_search_text(self, text: str):
        self.search_text += " " + text

    def get_search_text(self) -> list:
        return self.search_text.split(" ")

    def set_id(self, id: int):
        self.id = id

    def has_id(self) -> bool:
        return self.id > 0

    def get_id(self) -> int:
        return self.id

    def add_category(self, category_name: str):
        if not self.category.__contains__(category_name): self.category.append(category_name)

    def remove_category(self, category_name: str):
        if self.category.__contains__(category_name): self.category.remove(category_name)

    def have_category(self, category_names: [str, list]) -> bool:
        if isinstance(category_names, str): return self.category.__contains__(category_names)
        for item in category_names:
            if not self.category.__contains__(item): return False
        return True

    def have_category_searching(self, category_names: [str, list]) -> bool:
        if isinstance(category_names, str):
            if difflib.get_close_matches(category_names, self.category):
                return True
            return False
        for name in category_names:
            if not difflib.get_close_matches(name, self.category):
                return False
        return True

    def is_forced_relevance(self) -> bool:
        return self.forced_relevance

    def get_name(self):
        return self.name.replace("\.", ".")

    def add_relevance(self, relevance: int) -> int:
        self.relevance += relevance
        self.all_delivered_relevance += 1
        self.last_relevance.append(relevance)
        if len(self.last_relevance) > self.max_last_relevance:
            self.last_relevance.pop(0)
        return self.relevance

    def set_relevance(self, relevance: int):
        self.relevance = relevance

    def get_last_relevance_count(self) -> int:
        try:
            return round(sum(self.last_relevance) / len(self.last_relevance))
        except ZeroDivisionError:
            return 0

    def relevance_count(self, weight: int = 50) -> int:
        if weight > 100:
            weight = 100
        elif weight < 0:
            weight = 0
        return round(sum([self.relevance * weight / 100, self.count * (100 - weight) / 100]) / 2)

    def addCount(self, add: int = 1) -> int:
        self.count += add
        self.dataScientist.set(f"{self.save_under}.{self.name}.count", self.count)
        return self.count
