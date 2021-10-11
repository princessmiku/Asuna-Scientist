import collections
import difflib
import random
import sys
import threading

import scientist as sc


scientist = sc.DataScientist(None)

# add data
videos: dict = {
    1: {
        "name": "Learn Flask for Python - Full Tutorial",
        "url": "https://www.youtube.com/watch?v=Z1RJmh_OqeA",
        "category": ["python", "flask", "website", "english", "programming", "webserver"],
        "description": "Flask is a micro web framework written in Python. "
                       "It is classified as a microframework because it does not require particular tools or libraries."
                       "Learn how to use it in this crash course tutorial.",
        "author": ["freeCodeCamp.org", "freeCodeCamp"],
        "relevance": 835000 / 349,
        "watches": 835000
    },
    2: {
        "name": "Java Web Programmierung Teil 1: Http-Requests und Webserver",
        "url": "https://www.youtube.com/watch?v=QYmvV4msjEY",
        "category": ["java", "webserver", "http", "german", "web", "programming", "Technic"],
        "description": "",
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
    }
}


for o in videos:
    video = videos[o].copy()
    col: scientist.Collection = scientist.addAInsert(video["name"], save_under="video", category=video["category"])
    col.set_relevance(video["relevance"])
    col.addCount(video["watches"])
    for author in video["author"]:
        col.add_category(author)
    col.add_search_text(video["description"])
    col.set_id(o)


matches = scientist.getSearchCollections("Programmieren", "video")
m: scientist.Collection
print("------------------------------------------------------------------------")
for m in matches:
    print("Video Title", m.get_name())
    print("URL", videos[m.get_id()]["url"])
    print("------------------------------------------------------------------------")
