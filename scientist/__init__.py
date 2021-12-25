"""
    Data Scientist V2
    Created by Miku

    Version: 2.0.0 Alpha
    Github: https://github.com/princessmiku
    Project on Github: https://github.com/princessmiku/Scientist

    Example Text generator
    https://www.blindtextgenerator.de/
"""
# Own library's
from .collection import Collection, getBaseCollectionDataDict
from .user import User
from .logSettings import LogSettings
from .record import Record
from .databaseConnector import DatabaseConnector

# import python stuff
import difflib, itertools, sqlite3, threading, re, os, logging, random, time, functools, collections as pyCollections
from typing import Optional

# external added library's
import polars

_version = "2.0.0 Alpha"


# stuff?


def threadsafe_function(fn):
    """
    decorator making sure that the decorated function is thread safe
    Quelle: https://stackoverflow.com/questions/1072821/is-modifying-a-class-variable-in-python-threadsafe
    """

    lock = threading.Lock()

    def new(*args, **kwargs):
        lock.acquire()
        try:
            r = fn(*args, **kwargs)
        except Exception as e:
            raise e
        finally:
            lock.release()
        return r

    return new


class DataScientist:
    # Simple default text for the top of the log
    __defaultLogTextStart = f"> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n" \
                            f"| Data Scientist V2\n" \
                            f"| Created by Miku\n| \n" \
                            f"| Version: {_version}\n" \
                            f"| Github: https://github.com/princessmiku\n" \
                            f"| Project on Github: https://github.com/princessmiku/Scientist\n" \
                            f"> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"

    __defaultIndexStructure = {
        "id": [],
        "name": [],
        "extraSearchs": [],
        "count": [],
        "relevance": [],
        "category": []
    }

    logger: logging.Logger = None

    def __init__(self, _databaseConnector: DatabaseConnector, _logSettings: LogSettings = None,
                 autoRecreateIndex: bool = False):
        """
        Init the brain of Scientist
        :param _logSettings: Log settings, when None it will use the default
        """

        # set vabs
        self.__databaseConnector = _databaseConnector

        # check if not logger set
        if self.logger is None or LogSettings is not None:
            # check if set log settings
            if _logSettings is None:
                # setup default log settings
                _logSettings = LogSettings("s2")
                _logSettings.setFilemode("w")
            # setup the logger
            self.updateLogger(_logSettings)
        self.logger.info("Init DataScientist")

        self.__data: dict = {}
        # generate default structure
        self.__generate_default_structure()

        # init the index
        self.autoRecreateIndex = autoRecreateIndex
        self.__autoRecreateThread = None
        if self.autoRecreateIndex:
            self.__autoRecreateThread = threading.Thread(target=self.__autoRecreateIndexLoop, daemon=True)
            self.__autoRecreateThread.start()
        else:
            self.recreateIndex(self.__defaultIndexStructure)

        # running thread list
        self.runningThreads: list[threading.Thread] = []

        # complete init
        self.logger.info("Init complete")

    def __generate_default_structure(self):
        """
        This function generate the default used structure for saving
        :return:
        """
        self.logger.debug("Generate default structure")
        self.__data["collection"] = {}
        # check if json exists // vorübergehend
        self.__data["index"] = polars.DataFrame()
        self.__data["user"] = {}
        self.__data["searchConnections"] = {}
        self.__data["connectedCategorys"] = {}

    def get(self, location: str) -> [int, str, bool]:
        # get data from a location
        self.logger.debug("Get data from " + location)
        location: list = re.split(r"[.]+\b(?<!\\.)", location)
        data: any = self.__data
        loc: any
        for step in location:
            if not isinstance(data, dict): break
            if not data.__contains__(step): return None
            data = data[step]
        return data

    def set(self, location: str, data: [int, str, bool]):
        # set data on location
        self.logger.debug("Set data at " + location + " data: " + str(data))
        location: list = re.split(r"[.]+\b(?<!\\.)", location)
        save = self.__data
        for count, step in enumerate(location):
            if count != len(location) - 1:
                if not save.__contains__(step): save[step] = {}
                save = save[step]
            else:
                save[step] = data

    def exists(self, location: str) -> bool:
        # check if data exits at location
        self.logger.debug("Check if exists data at " + location)
        location: list = re.split(r"[.]+\b(?<!\\.)", location)
        data: any = self.__data.copy()
        if not data.__contains__(location[0]): return False
        loc: any
        for step in location:
            try:
                if not data.__contains__(step): return False
                data = data[step]
            except AttributeError:
                return False
        return True

    def remove(self, location: str):
        # remove a location with data
        self.logger.debug("Remove location " + location)

        location: list = re.split(r"[.]+\b(?<!\\.)", location)
        data: any = self.__data
        loc: any
        for count, step in enumerate(location):
            if not isinstance(data, dict):
                if count + 1 == len(location):
                    data.pop(step)
                    break
                else:
                    return
            if not data.__contains__(step): return
            if count + 1 == len(location):
                data.pop(step)
                break
            data = data[step]

    @threadsafe_function
    def getNextAvailableID(self, location: str) -> int:
        if not self.exists(location + ".0"):
            dummy = getBaseCollectionDataDict(0, "Dummy")
            dummy["ignore"] = True
            self.set(location + ".0", Collection(dummy))
        lastID: str = list(self.get(location).keys())[-1]
        if not lastID.isnumeric():
            return 0
        self.set(location + "." + str(int(lastID) + 1), 0)
        self.logger.debug(f"Current Last id now " + str(int(lastID) + 1))
        return int(lastID) + 1

    # core

    def insert(self, text: str, startAsThread: bool = False, replacer=None) -> Optional[threading.Thread]:
        """
        Think is useless
        Insert a big text in the search engine, it will separate every word for searching it.
        :param text: insert text
        :param startAsThread: should it start as thread for speed up?
        :param replacer: Replace before insert, like str.replace(), list format is [["a", "b"], ["c", "d"]]
        :return:
        """

        # check if give replace
        if replacer is None:
            replacer = []

        # target thread def
        def run(_text: str):
            self.logger.debug("Insert text width a len of " + str(len(text)) + " characters")
            # replace
            for replace in replacer:
                _text = _text.replace(replace[0], replace[1])
            # setup the word list via split
            words: list = text.split(" ")
            word: str
            for word in words:
                # if a word ends with a point, remove it
                if word.endswith((".", ",", "!", "?")):
                    word = word[:-1]
                word = word.replace(".", "\n")
                _id: int = self.getNextAvailableID("collection")
                self.insertCollection(Collection(getBaseCollectionDataDict(_id, word)))

        # check if should start as thread
        if not startAsThread:
            run(text)
        else:
            self.logger.debug("Start text insertion as a thread")
            thread = threading.Thread(target=run, args=(text,), daemon=True)
            thread.start()
            return thread

    def insertCollection(self, col: Collection):
        """
        Add insert a collection, its overwrite if collection already exists
        :param col:
        :return:
        """
        self.logger.debug("Insert Collection named \"" + col.name + "\" with ID: " + str(col.id))
        # set the collection
        self.set(f"collection.{str(col.id)}", col)

    def addElement(self, name: str, extraSearchs: str = "", count: int = 1, relevance: int = 0,
                   _category: list[str] = None, ignore: bool = False):
        # add a single element to the search
        _id = self.getNextAvailableID("collection")
        if _category is None:
            _category = []
        self.logger.debug(f"Add element with name \"{name}\"")
        element: dict = getBaseCollectionDataDict(_id, name)
        element["extraSearchs"] = extraSearchs
        element["count"] = count
        element["relevance"] = relevance
        element["category"] = _category
        element["ignore"] = ignore
        col: Collection = Collection(element)
        self.insertCollection(col)

    def removeElement(self):
        # remove a single element
        self.logger.debug("Remove element ")
        pass

    # learning
    @threadsafe_function
    def __addSCEntry(self, text: str, chosen: str = None):
        text = text.lower()
        if not self.__data["searchConnections"].__contains__(text):
            self.__data["searchConnections"][text] = {}
        if chosen:
            chosen = chosen.lower()
            if not self.__data["searchConnections"][text].__contains__(chosen):
                self.__data["searchConnections"][text][chosen] = 0
            self.__data["searchConnections"][text][chosen] += 1

    def __existsSCEntry(self, text: str, otherText: str = None) -> bool:
        text = text.lower()
        if otherText is None:
            return self.__data["searchConnections"].__contains__(text)
        otherText = otherText.lower()
        if self.__data["searchConnections"].__contains__(text):
            return self.__data["searchConnections"][text].__contains__(otherText)
        return False

    def __checkSCEntryDiff(self, text: str, otherText: str) -> [str, int]:
        text = text.lower()
        matches = difflib.get_close_matches(text, list(self.__data["searchConnections"].keys()))
        if matches:
            matches2 = difflib.get_close_matches(otherText, list(self.__data["searchConnections"][matches[0]]))
            if matches2:
                return matches2[0], self.__data["searchConnections"][matches[0]][matches2[0]]
        return None, None

    @threadsafe_function
    def __addCCEntry(self, name: str, values: list[str]):
        name = name.lower()
        if not self.__data["connectedCategorys"].__contains__(name):
            self.__data["connectedCategorys"][name] = {}
        v: str
        for v in values:
            v = v.lower()
            if not self.__data["connectedCategorys"][name].__contains__(v):
                self.__data["connectedCategorys"][name][v] = 0
            self.__data["connectedCategorys"][name][v] += 1
            if not self.__data["connectedCategorys"].__contains__(v):
                self.__data["connectedCategorys"][v] = {}
            if not self.__data["connectedCategorys"][v].__contains__(name):
                self.__data["connectedCategorys"][v][name] = 0
            self.__data["connectedCategorys"][v][name] += 1

    def insertRecord(self, _record: Record):
        """
        Insert the finish record for learn the algorithm
        This Function work as a thread for maximum speed
        So is can be that this thread are not finish when you are finish
        :param _record:
        :return: the working thread
        """

        result = _record.getResult()
        # check is a result, for work with it
        if result is None: return
        self.logger.debug("init and start thread in insertRecord for search text \"" +
                          _record.searchText + "\" and the result " + str(result.id)
                          )
        # search Connections, add results for the search
        self.__addSCEntry(_record.searchText, result.name)
        # category connections
        self.__addCCEntry(_record.searchText, result.category)

    # searching
    def match(self, search: str, _user: [User, int] = None) -> Record:
        """
        Search in your data for the best matches, contains self learning
        :param search: Search text
        :param _user: Specific user, only require for user personalisation results
        :return:
        """

        # setup data
        index: polars.DataFrame = self.get("index")
        result: dict = {}
        names: polars.Series = index.name
        extraSearchs: polars.Series = index.extraSearchs
        categorysList: polars.Series = index.category
        # counter
        c: int
        # split the search
        toSearch: list = search.split(" ")
        # split words in name/extra
        n: str
        e: str
        for c in range(len(names)):
            name: list[str] = names[c].split(" ")
            extras: list[str] = extraSearchs[c].split(" ")
            category: list[str] = categorysList[c]
            nC: int = 0
            eC: int = 0
            cC: int = 0
            thisSearchN: list[str] = toSearch.copy()
            thisSearchE: list[str] = toSearch.copy()

            for n in name:
                matches: list = difflib.get_close_matches(n, thisSearchN)
                if matches:
                    nC += difflib.SequenceMatcher(None, n, matches[0]).ratio()
                    # thisSearchN.remove(matches[0])
            for e in extras:
                matches: list = difflib.get_close_matches(e, thisSearchE)
                if matches:
                    eC += difflib.SequenceMatcher(None, e, matches[0]).ratio()
                    # thisSearchE.remove(matches[0])

            usedCats: list[str] = []
            cat: str
            ifBreak: bool = False
            for cat in category:
                matches: list = difflib.get_close_matches(cat, toSearch)
                if matches:
                    cC += difflib.SequenceMatcher(None, cat, matches[0]).ratio()
                    break
                if not self.__data["connectedCategorys"].__contains__(cat.lower()): continue
                subCategorys: list[str] = self.__data["connectedCategorys"][cat.lower()]
                for subC in subCategorys:
                    if usedCats.__contains__(subC): continue
                    usedCats.append(subC)
                    matches: list = difflib.get_close_matches(subC, category)
                    if matches:
                        cC += difflib.SequenceMatcher(None, subC, matches[0]).ratio()
                        ifBreak = True
                        break
                if ifBreak: break
            finalCount: float = nC + eC + cC
            if finalCount > 0:
                joinedName: str = " ".join(name)
                movieCount = difflib.SequenceMatcher(None, joinedName, search).ratio()
                if joinedName.__contains__(search):
                    movieCount += 1
                movieCount += difflib.SequenceMatcher(None, extras, search).ratio()
                movieCount += cC
                matchName, addCount = self.__checkSCEntryDiff(search, joinedName)
                if matchName:
                    matchPercent = difflib.SequenceMatcher(None, joinedName, matchName).ratio()
                    if matchPercent >= 0.72:  # spider percent
                        movieCount += addCount

                if not result.__contains__(movieCount):
                    result[movieCount] = []
                result[movieCount].append(self.get("collection." + str(index.id[c])))
        result = dict(pyCollections.OrderedDict(sorted(result.items(), reverse=True)))
        return Record(search, [item for sublist in result.values() for item in sublist], _user)

    # searching
    def matchNSLD(self, search: str) -> Record:
        """
        NSLD = Not self learning data
        Search in your data for the best matches, without the learning thinks
        :param search: search text
        :return:
        """
        # setup data
        index: polars.DataFrame = self.get("index")
        result: dict = {}
        names: polars.Series = index.name
        extraSearchs: polars.Series = index.extraSearchs
        # counter
        c: int
        # split the search
        toSearch: list = search.split(" ")
        # split words in name/extra
        n: str
        e: str
        for c in range(len(names)):
            name: list[str] = names[c].split(" ")
            extras: list[str] = extraSearchs[c].split(" ")
            nC: int = 0
            eC: int = 0
            thisSearchN: list[str] = toSearch.copy()
            thisSearchE: list[str] = toSearch.copy()
            for n in name:
                matches: list = difflib.get_close_matches(n, thisSearchN)
                if matches:
                    nC += difflib.SequenceMatcher(None, n, matches[0]).ratio()
                    # thisSearchN.remove(matches[0])
            for e in extras:
                matches: list = difflib.get_close_matches(e, thisSearchE)
                if matches:
                    eC += difflib.SequenceMatcher(None, e, matches[0]).ratio()
                    # thisSearchE.remove(matches[0])
            finalCount: float = nC + eC
            if finalCount > 0:
                if not result.__contains__(finalCount):
                    result[finalCount] = []
                result[finalCount].append(self.get("collection." + str(index.id[c])))
        result = dict(pyCollections.OrderedDict(sorted(result.items(), reverse=True)))
        return Record(search, [item for sublist in result.values() for item in sublist], User(user.defaultStructure))

    # index
    @threadsafe_function
    def recreateIndex(self, indexData=None):
        """
        Re create the search index, this index is important for the searchs
        so hold it up to date.

        The Script will update the Index each time when is starting. But long time ago it can be old.

        Or activate auto recreate Indexing on start
        :param indexData: give the index specific data for create a specific index, not recommended!
        :return:
        """
        if indexData is None:
            indexData = {}
        self.logger.info("Recreate the Index")

        # df: polars.DataFrame = self.__data["index"]
        # vorübergehendes speichern

        index: dict = {
            "id": [],
            "name": [],
            "extraSearchs": [],
            "count": [],
            "relevance": [],
            "category": []
        }
        values: dict = self.get("collection").copy()
        if values.__contains__("0"):
            values.pop("0")
        _id: str
        for _id in values:
            col: Collection = values[_id]
            index["id"].append(col.id)
            index["name"].append(col.name)
            index["extraSearchs"].append(col.extraSearchs)
            index["count"].append(float(col.count))
            index["relevance"].append(float(col.relevance))
            index["category"].append(col.category)

        self.__data.__setitem__("index", polars.DataFrame(index))

        self.logger.info("Recreate success")

    def __autoRecreateIndexLoop(self, cooldown: int = 60000):
        """
        Auto recreate index function
        It will recreate all 10 minutes the index
        :param cooldown:
        :return:
        """

        self.logger.debug("Start the auto recreate loop")
        while self.autoRecreateIndex:
            self.recreateIndex()
            time.sleep(cooldown)

    # cleaning
    def cleanUp(self):
        """
        Clean your data, it will remove invalid entry or old data what are no longer in use
        like a deleted element, it will sorting all data new correctly, do not add new element in this time
        it can be deleted!.

        This process can take long time
        :return:
        """
        pass

    # getter setter
    def getData(self) -> dict:
        # get all data of this class
        self.logger.debug("Get ALL data")
        return self.__data

    # extras

    def save(self) -> bool:
        # save all data
        self.logger.info("SAVE")
        return True

    def waitFinish(self, threadList: list):
        """
        This function is a easy way for waiting that the threads are finished
        :param threadList: a list with threads
        :return:
        """
        threadIdentifikator: int = random.randint(100000, 9999999)
        self.logger.debug(f"[{str(threadIdentifikator)}] Start waiting on {str(len(threadList))} threads")
        t: threading.Thread
        # join all thread and listen is finish
        for t in threadList:
            t.join()
        self.logger.debug(f"[{str(threadIdentifikator)}] Finish waiting on threads")

    def updateLogger(self, _logSettings: LogSettings):
        """
        Update the log modul for ALL
        :param _logSettings:
        :return:
        """
        if self.logger is not None:
            self.logger.warning("Setup a new Logging module")

        # get the path of the log
        logPath: str = _logSettings.filepath.rsplit("/", 1)[0]
        # check if the folder exists when not create the folder
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        # check if a logging file exists when not create a default log file layout
        if not os.path.isfile(_logSettings.filepath):
            with open(_logSettings.filepath, mode=_logSettings.filemode) as f:
                f.write(self.__defaultLogTextStart)
                f.close()
        elif _logSettings.filemode == "w":
            with open(_logSettings.filepath, mode=_logSettings.filemode) as f:
                f.write(self.__defaultLogTextStart)
                f.close()
        # init the log config on the logger
        _logSettings.initConfig()
        self.logger = _logSettings.logger
        # open the log file, enter the start of the new beginning, ignore log layout
        with open(_logSettings.filepath, mode='a') as f:
            f.write(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting a new log\n\n")
            f.close()

        # Set the logger
        Collection.logger = self.logger
        DatabaseConnector.logger = self.logger
        Record.logger = self.logger

        # finish
        self.logger.debug("Logging module successfully loaded")
