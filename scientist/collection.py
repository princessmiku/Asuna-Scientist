class Collection:
    dataScientist = None
    max_last_relevance = 10

    def __init__(self, name: str, save_under: str = "collection"):
        self.name: str = name
        self.save_under = save_under
        self.count: int = 0
        self.relevance: int = 0
        self.last_relevance: list = []
        self.dataScientist.set(f"{self.save_under}.{self.name}.self", self)

    def get_name(self):
        return self.name.replace("\&!", ".")

    def add_relevance(self, relevance: int) -> int:
        self.relevance += relevance
        self.last_relevance.append(relevance)
        if len(self.last_relevance) > self.max_last_relevance:
            self.last_relevance.pop(0)
        return self.relevance

    def get_last_relevance_count(self) -> int:
        return round(sum(self.last_relevance) / len(self.last_relevance))

    def relevance_count(self) -> int:
        return round(sum([self.relevance, self.count]) / 2)

    def addCount(self, add: int = 1) -> int:
        self.count += add
        self.dataScientist.set(f"{self.save_under}.{self.name}.count", self.count)
        return self.count
