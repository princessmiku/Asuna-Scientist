"""
    Diese Main ist nur zum testen, die main hat keine verbindung zur eigentlichen lib
"""

import collections
import difflib
import random
import sys
import threading
import time

import polars

import scientist as sc
from scientist import Category, LogSettings, Collection, databaseConnector, Record

start_time = time.time()
scientist = sc.DataScientist(databaseConnector.DatabaseConnector("./log/test.db", True))

theMasterofDicts: dict = {}


#data: list = scientist.getData()["collection"].values()
#col: Collection
#scientist.recreateIndex()
#print(scientist.get("index"))
#for col in data:
#    print(col.name, col.count)
## add data
videos: dict = {
    1: {
        "name": "Learn Flask for Python - Full Tutorial",
        "url": "https://www.youtube.com/watch?v=Z1RJmh_OqeA",
        "category": ["python", "flask", "website", "english", "programming", "webserver"],
        "description": "Flask is a micro web framework written in Python. ",
        "author": ["freeCodeCamp.org", "freeCodeCamp"],
        "relevance": 835000 / 349,
        "watches": 835000
    },
    2: {
        "name": "Java Web Programmierung Teil 1: Http-Requests und Webserver",
        "url": "https://www.youtube.com/watch?v=QYmvV4msjEY",
        "category": ["java", "webserver", "http", "german", "web", "programming", "Technic", "framework"],
        "description": "Lerne Java Programmierung framework framework",
        "author": ["TotalSurpriseException"],
        "relevance": 10200 / 6,
        "watches": 10200
    },
    3: {
        "name": "Für Kinder gut, die Kategorie 18+ ist lächerlich! LEGO® Technic 42126 Ford F-150 Raptor",
        "url": "https://www.youtube.com/watch?v=XfAJHUgM8ao",
        "category": ["Lego", "Technic", "Ford", "Raptor"],
        "description": "Technic - erschienen 2021 - 1379 Teile",
        "author": ["Held der Steine Inh. Thomas Panke", "Held der Steine", "Thomas Panke"],
        "relevance": 200000 / 141,
        "watches": 200000
    },
    4: {
        "name": "Clym & der Held bauen Minecraft! LEGO® 21160 Der Illager Überfall",
        "url": "https://www.youtube.com/watch?v=HU07JtXIOzc",
        "category": ["Lego", "Minecraft", "Clym"],
        "description": "Minecraft - erschienen 2020 - 545 Teile",
        "author": ["Held der Steine Inh. Thomas Panke", "Held der Steine", "Thomas Panke"],
        "relevance": 80000 / 200,
        "watches": 80000
    },
    5: {
        "name": "Lordi - Hard Rock Hallelujah",
        "url": "https://www.youtube.com/watch?v=-6Xl9tBWt54",
        "category": ["music"],
        "description": "Music video by Lordi performing Hard Rock Hallelujah. (C) 2006 SONY BMG MUSIC ENTERTAINMENT (FINLAND) OY",
        "author": ["Lordi"],
        "relevance": 81000000 / 23000,
        "watches": 81000000
    },
    6: {
        "name": "Learn Flusk for Python - Full Tutorial",
        "url": "https://www.youtube.com/watch?v=Z1RJmh_OqeA",
        "category": ["python", "Flusk", "website", "english", "programming", "webserver"],
        "description": "Flusk is a micro web framework written in Python. ",
        "author": ["freeCodeCamp.org", "freeCodeCamp"],
        "relevance": 835000 / 349,
        "watches": 835000
    }
}
catDict = {}
nextAv = 0
for d in videos:
    catIdsHere = []
    for mirGehenDieNamenAus in videos[d]["category"]:
        if not catDict.__contains__(mirGehenDieNamenAus):
            catDict[mirGehenDieNamenAus] = nextAv
            nextAv += 1
        catIdsHere.append(catDict[mirGehenDieNamenAus])
    scientist.addElement(videos[d]["name"], videos[d]["description"] + " " + " ".join(videos[d]["author"]) + " " + " ".join(videos[d]["category"]), videos[d]["watches"], videos[d]["relevance"], catIdsHere)
scientist.recreateIndex()
index: polars.DataFrame = scientist.get("index")
word = "lordi"


def find_it(w, dfSeries):
    w = w.lower()
    return difflib.get_close_matches(w, dfSeries, cutoff=0.125)


def find_itOthers(w, dfSeries):
    w = w.lower()
    return difflib.get_close_matches(w, dfSeries, cutoff=0)

titels = find_it(word, index.name)
others = find_itOthers(word, index.extraSearchs)

#for t in titels:
    #print(t, difflib.SequenceMatcher(None, word, t).ratio())

#for t in others:
    #print(t, difflib.SequenceMatcher(None, word, t).ratio())

#print(titels)
#print(others)

scientist.recreateIndex()
rec: Record = scientist.match("flask")
d: Collection
for d in rec.data:
    print(d.id, d.name)
