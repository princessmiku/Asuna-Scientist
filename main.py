import collections
import difflib
import random
import sys
import threading

import scientist as sc


scientist = sc.DataScientist(None)
#replace = [["\n", " "]]
#t = scientist.insert(open("./example.txt", mode='r').read(), replacer=replace, startAsThread=True)
col: scientist.Collection = scientist.addAInsert("youtube", "streaming", category=["video"])
col.add_relevance(random.randint(0, 100))
o1 = scientist.addAInsert("twitch", "streaming", category=["live"])
o1.add_relevance(random.randint(0, 100))
o2 = scientist.addAInsert("amazon prime", "streaming", category=["video"])
o2.add_relevance(random.randint(0, 100))
o3 = scientist.addAInsert("netflix", "streaming", category=["video"])
o3.add_relevance(random.randint(0, 100))
o6 = scientist.addAInsert("netflixe", "streaming", category=["video"])
o6.add_relevance(random.randint(0, 100))
o4 = scientist.addAInsert("sky", "streaming", category=["video", "live"])
o4.add_relevance(random.randint(0, 100))
o5 = scientist.addAInsert("Crunchyroll", "streaming", category=["anime"])
o5.add_relevance(random.randint(0, 100))

match = scientist.getCollectionsByLastRelevanceCount(80, [o1, o2, o3, o4, o5, col, o6])
print(match)
x: scientist.Collection
if match:
    for x in match:
        print(x.get_name())
        print(x.get_last_relevance_count())
else:
    print("nothing found")