import collections


class Collection:
    dataScientist = None
    max_last_relevance = 10

    def __init__(self, name: str, save_under: str = "collection"):
        self.name: str = name
        self.save_under = save_under
        self.count: int = 0
        self.relevance: int = 0
        self.all_delivered_relevance: int = 0
        self.last_relevance: list = []
        self.dataScientist.set(f"{self.save_under}.{self.name}.self", self)

    def get_name(self):
        return self.name.replace("\.", ".")

    def add_relevance(self, relevance: int) -> int:
        self.relevance += relevance
        self.all_delivered_relevance += 1
        self.last_relevance.append(relevance)
        if len(self.last_relevance) > self.max_last_relevance:
            self.last_relevance.pop(0)
        return self.relevance

    def get_last_relevance_count(self) -> int:
        try:
            return round(sum(self.last_relevance) / len(self.last_relevance))
        except ZeroDivisionError:
            return 0

    def relevance_count(self, weight: int = 50) -> int:
        if weight > 100: weight = 100
        elif weight < 0: weight = 0
        return round(sum([self.relevance * weight / 100, self.count * (100 - weight) / 100]) / 2)

    def addCount(self, add: int = 1) -> int:
        self.count += add
        self.dataScientist.set(f"{self.save_under}.{self.name}.count", self.count)
        return self.count

