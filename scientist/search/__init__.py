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
import json

from ..datahandler.dtos_S2Data import Collection, SearchConnections, ConnectedCategorys
from ..datahandler.dtos_users import User
from ..datahandler.dhSetup import s2Session, userSession, get_or_create
from ..search.logSettings import LogSettings
from ..search.record import Record
from sqlalchemy.orm.attributes import flag_modified

# import python stuff
import difflib, threading, re, os, logging, random, time, collections as pyCollections
from typing import Optional


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

    def __init__(self, _logSettings: LogSettings = None,
                 autoRecreateIndex: bool = False):
        """
        Init the brain of Scientist
        :param _logSettings: Log settings, when None it will use the default
        """

        # set vabs
        self.__s2season = s2Session

        # check if not logger set
        if self.logger is None or LogSettings is not None:
            # check if set log settings
            if _logSettings is None:
                # setup default log settings
                _logSettings = LogSettings("s2.log")
                _logSettings.setFilemode("w")
            # setup the logger
            self.updateLogger(_logSettings)
        self.logger.info("Init DataScientist")

        self.__data: dict = {}
        # generate default structure
        self.__generate_default_structure()
        # load data in the default structure
        self.__load()

        # init the index
        self.recreateIndex(self.__defaultIndexStructure)
        self.autoRecreateIndex = autoRecreateIndex
        self.__autoRecreateThread = None
        if self.autoRecreateIndex:
            self.__autoRecreateThread = threading.Thread(target=self.__autoRecreateIndexLoop, daemon=True)
            self.__autoRecreateThread.start()
        else:
            self.recreateIndex()
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
        self.__data["index"] = {}
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
            dummy: Collection = get_or_create(self.__s2season, Collection, id=0)
            dummy.name = "Dummy"
            dummy.ignore = True
            self.set(location + ".0", dummy)
            self.save()
        lastID: str = list(self.get(location).keys())[-1]
        if not lastID.isnumeric():
            return 0
        self.set(location + "." + str(int(lastID) + 1), 0)
        self.logger.debug(f"Current Last id now " + str(int(lastID) + 1))
        return int(lastID) + 1


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
                   _category: list[str] = None, identifier: str = '0', ignore: bool = False):
        # add a single element to the search
        _id = self.getNextAvailableID("collection")
        if _category is None:
            _category = []
        self.logger.debug(f"Add element with name \"{name}\"")
        col: Collection = Collection(_id, identifier)
        col.name = name
        col.extraSearch = extraSearchs
        col.count = count
        col.relevance = relevance
        col.category = _category
        col.ignore = ignore
        self.__s2season.add(col)
        self.insertCollection(col)
        self.save()

    def removeElement(self):
        # remove a single element
        self.logger.debug("Remove element ")
        pass

    # learning
    @threadsafe_function
    def __addSCEntry(self, text: str, chosen: str = None):
        text = text.lower()
        if not self.__data["searchConnections"].__contains__(text):
            self.__data["searchConnections"][text] = get_or_create(self.__s2season, SearchConnections, name=text)
        if chosen:
            chosen = chosen.lower()
            if not self.__data["searchConnections"][text].data.__contains__(chosen):
                self.__data["searchConnections"][text].data[chosen] = 0
            self.__data["searchConnections"][text].data[chosen] += 1
            flag_modified(self.__data["searchConnections"][text], 'data')

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
            matches2 = difflib.get_close_matches(otherText, list(self.__data["searchConnections"][matches[0]].data))
            if matches2:
                return matches2[0], self.__data["searchConnections"][matches[0]].data[matches2[0]]
        return None, None

    @threadsafe_function
    def __addCCEntry(self, name: str, values: list[str]):
        name = name.lower()
        if not self.__data["connectedCategorys"].__contains__(name):
            self.__data["connectedCategorys"][name] = get_or_create(self.__s2season, ConnectedCategorys, name=name)
        v: str
        for v in values:
            v = v.lower()
            if not self.__data["connectedCategorys"][name].data.__contains__(v):
                self.__data["connectedCategorys"][name].data[v] = 0
            self.__data["connectedCategorys"][name].data[v] += 1
            flag_modified(self.__data["connectedCategorys"][name], 'data')
            if not self.__data["connectedCategorys"].__contains__(v):
                self.__data["connectedCategorys"][v] = get_or_create(self.__s2season, ConnectedCategorys, name=v)
            if not self.__data["connectedCategorys"][v].data.__contains__(name):
                self.__data["connectedCategorys"][v].data[name] = 0
            self.__data["connectedCategorys"][v].data[name] += 1
            flag_modified(self.__data["connectedCategorys"][v], 'data')

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
    def match(self, search: str, _user: [User, int] = None, needCount: int = 0) -> Record:
        """
        Search in your data for the best matches, contains self learning
        :param search: Search text
        :param _user: Specific user, only require for user personalisation results
        :return:
        """
        search = search.lower()
        # setup data
        index: dict = self.get("index")
        result: dict = {}
        names: list[str] = index["name"]
        extraSearchs: list[str] = index["extraSearchs"]
        categorysList: list[list[str]] = index["category"]
        # counter
        c: int
        # split the search
        toSearch: list = search.lower().split(" ")
        # split words in name/extra
        n: str
        e: str
        for c in range(len(names)):
            name: list[str] = names[c].lower().split(" ")
            extras: list[str] = extraSearchs[c].lower().split(" ")
            category: list[str] = categorysList[c]
            nC: int = 0
            eC: int = 0
            cC: int = 0
            thisSearchN: list[str] = toSearch.copy()
            thisSearchE: list[str] = toSearch.copy()

            for n in name:
                matches: list = difflib.get_close_matches(n, thisSearchN)
                if matches:
                    nameChance = difflib.SequenceMatcher(None, n, matches[0]).ratio()
                    if nameChance > 0.85:
                        nC += nameChance * 4
                    else:
                        nC += nameChance * 2
                    break
                if difflib.SequenceMatcher(None, n, search).ratio() > 0.9:
                    nC += 2

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
                subCategorys: list[str] = self.__data["connectedCategorys"][cat.lower()].data
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
            if finalCount > 0.2:
                joinedName: str = " ".join(name)
                movieCount = difflib.SequenceMatcher(None, search, joinedName).ratio()
                if movieCount > 0.85:
                    movieCount *= 2
                if joinedName.__contains__(search):
                    movieCount += 1
                movieCount += difflib.SequenceMatcher(None, extras, search).ratio()
                movieCount += cC
                matchName, addCount = self.__checkSCEntryDiff(search, joinedName)
                if matchName:
                    matchPercent = difflib.SequenceMatcher(None, joinedName, matchName).ratio()
                    if matchPercent >= 0.72:  # spider percent
                        movieCount += addCount * matchPercent


                if eC > 0.5:
                    cloudBe = difflib.SequenceMatcher(None, search, extraSearchs[c].lower()).get_matching_blocks()
                    addeC = 0
                    for m in cloudBe:
                        addeC += m.size if m.size > 5 else 0
                    addeC /= len(extraSearchs[c])
                    addeC *= 4
                    if addeC >= 1.1:
                        movieCount += addeC
                    else:
                        movieCount += eC if eC < 1.2 else 1
                else:
                    movieCount += eC if eC <= 0.4 else 0.3
                if movieCount < needCount: continue
                if not result.__contains__(movieCount):
                    result[movieCount] = []
                result[movieCount].append(self.get("collection." + str(index["id"][c])))
        highestMovCou = max(result.keys())
        result = dict(pyCollections.OrderedDict(sorted(result.items(), reverse=True)))
        return Record(
            search,
            [item for sublist in result.values() for item in sublist],
            _user,
            highestRevel=highestMovCou
        )

    # searching
    def matchNSLD(self, search: str) -> Record:
        """
        NSLD = Not self learning data
        Search in your data for the best matches, without the learning thinks
        :param search: search text
        :return:
        """
        # setup data
        index: dict = self.get("index")
        result: dict = {}
        names: list[str] = index["name"]
        extraSearchs: list[str] = index["extraSearchs"]
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
                result[finalCount].append(self.get("collection." + str(index["id"][c])))
        result = dict(pyCollections.OrderedDict(sorted(result.items(), reverse=True)))
        return Record(search, [item for sublist in result.values() for item in sublist], None)

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
            index["extraSearchs"].append(col.extraSearch)
            index["count"].append(float(col.count))
            index["relevance"].append(float(col.relevance))
            index["category"].append(col.category)

        self.__data.__setitem__("index", index)

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

    # save and load
    def save(self) -> bool:
        # save all data
        self.logger.info("SAVE")

        self.__s2season.commit()

        self.logger.info("SAVING COMPLETE")
        return True

    def __load(self):
        """
        Load the data from the database
        :return:
        """
        self.logger.info("Load data from database")

        # collection
        data: list[Collection] = self.__s2season.query(Collection).all()
        col: Collection
        for col in data:
            self.insertCollection(col)

        data: list[SearchConnections] = self.__s2season.query(SearchConnections).all()
        searchCon: SearchConnections
        for searchCon in data:
            self.__data["searchConnections"][searchCon.name] = searchCon

        data: list[ConnectedCategorys] = self.__s2season.query(ConnectedCategorys).all()
        connectedCat: ConnectedCategorys
        for connectedCat in data:
            self.__data["connectedCategorys"][connectedCat.name] = connectedCat

    def __firstDataLoad(self):
        pass

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
        Record.logger = self.logger

        # finish
        self.logger.debug("Logging module successfully loaded")
