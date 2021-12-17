"""
    Logging Module

    log your system

"""
import logging
from logging import FileHandler, Formatter
import time


class LogSettings:

    def __init__(self, loggerName: str, filepath: str = "./log/s2.log", filemode="a",
                 textFmt="[%(asctime)s] [%(levelname)s]: %(message)s >> %(pathname)s:%(lineno)d",
                 dateFmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG):
        self.loggerName = loggerName
        self.filepath = filepath
        self.filemode = filemode
        self.textFmt = textFmt
        self.dateFmt = dateFmt
        self.level = level
        self.logger = logging.getLogger(loggerName)

    def setFilePath(self, filepath: str):
        """
        Set the name of the file in which it should be saved
        :param filepath: Name of file, with ending (.log, .txt, and more)
        :return:
        """
        self.filepath = filepath

    def setFilemode(self, filemode: str):
        """
        Set the file mode
        :param filemode: w = write | a = append
        :return:
        """
        self.filemode = filemode

    def setTextFmt(self, textFmt: str):
        """
        Set the format of the log text
        :param textFmt: custom string with values
        :return:
        """
        self.textFmt = textFmt

    def setDateFmt(self, dateFmt: str):
        """
        Set the format of the logged date with your custom string
        except all values from time.strftime()
        :param dateFmt:
        :return:
        """
        self.dateFmt = dateFmt

    def setLevel(self, level: [logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG, logging.NOTSET]):
        """
        Set the level of the log
        except Critical, Error, Warning, Info, Debug, NotSet
        :param level:
        :return:
        """
        self.level = level

    def initConfig(self):
        """
        Init the config to the logger
        :return:
        """
        fileHandler = FileHandler(self.filepath)
        fileHandler.mode = self.filemode
        fileHandler.setLevel(self.level)
        formatter = Formatter(self.textFmt)
        formatter.datefmt = self.dateFmt
        fileHandler.setFormatter(formatter)
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(self.level)
