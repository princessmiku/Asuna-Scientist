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
from .category import Category
from .record import Record
from .databaseConnector import DatabaseConnector

# import python stuff
import difflib, itertools, sqlite3, threading, re, os, logging, random, time
from typing import Optional

# external added library's


_version = "2.0.0 Alpha"


class DataScientist:

    # Simple default text for the top of the log
    __defaultLogTextStart = f"> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n" \
                            f"| Data Scientist V2\n" \
                            f"| Created by Miku\n| \n" \
                            f"| Version: {_version}\n" \
                            f"| Github: https://github.com/princessmiku\n" \
                            f"| Project on Github: https://github.com/princessmiku/Scientist\n" \
                            f"> - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n"
    logger: logging.Logger = None

    def __init__(self, _databaseConnector: DatabaseConnector, _logSettings: LogSettings = None, autoRecreateIndex: bool = False):
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
            self.recreateIndex()

        # complete init
        self.logger.info("Init complete")

    def __generate_default_structure(self):
        """
        This function generate the default used structure for saving
        :return:
        """
        self.logger.debug("Generate default structure")
        self.__data["collection"] = {}
        self.__data["user"] = {}

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

    # core

    def insert(self, text: str, startAsThread: bool = False, replacer=None) -> Optional[threading.Thread]:
        """
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
                if not self.exists(f"collection.{word}"):
                    self.insertCollection(Collection(getBaseCollectionDataDict(word)))
                col = self.get(f"collection.{word}")
                col.addCount()

        # check if should start as thread
        if not startAsThread:
            run(text)
        else:
            self.logger.debug("Start text insertion as a thread")
            thread = threading.Thread(target=run, args=(text, ), daemon=True)
            thread.start()
            return thread

    def insertCollection(self, col: Collection):
        """
        Add insert a collection, its overwrite if collection already exists
        :param col:
        :return:
        """
        self.logger.debug("Insert Collection named \"" + col.name + "\"")
        # set the collection
        self.set(f"collection.{col.name}", col)

    def addElement(self):
        # add a single element to the search
        self.logger.debug("Add element ")
        pass

    def removeElement(self):
        # remove a single element
        self.logger.debug("Remove element ")
        pass

    def insertRecord(self, _record: Record) -> threading.Thread:
        """
        Insert the finish record for learn the algorithm
        This Function work as a thread for maximum speed
        :param _record:
        :return: the working thread
        """

        def run(_record: Record):
            pass

        self.logger.debug("init and start thread in insertRecord for search text \"" + _record.searchText + "\"")
        thread = threading.Thread(target=run, args=(_record, ), daemon=True)
        thread.start()
        return thread

    def recreateIndex(self):
        """
        Re create the search index, this index is important for the searchs
        so hold it up to date.

        The Script will update the Index each time when is starting. But long time ago it can be old.

        Or activate auto recreate Indexing on start
        :return:
        """
        self.logger.debug("Recreate the Index")

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
        Category.logger = self.logger
        Collection.logger = self.logger
        DatabaseConnector.logger = self.logger
        Record.logger = self.logger

        # finish
        self.logger.debug("Logging module successfully loaded")
