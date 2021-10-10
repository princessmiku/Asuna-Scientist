import collections
import difflib
import random
import sys
import threading

import scientist as sc


scientist = sc.DataScientist(None)
#replace = [["\n", " "]]
#t = scientist.insert(open("./example.txt", mode='r').read(), replacer=replace, startAsThread=True)
col: scientist.Collection = scientist.addAInsert("youtube", "streaming")
col.add_relevance(random.randint(0, 100))
scientist.addAInsert("twitch", "streaming").add_relevance(random.randint(0, 100))
scientist.addAInsert("amazon prime", "streaming").add_relevance(random.randint(0, 100))
scientist.addAInsert("netflix", "streaming").add_relevance(random.randint(0, 100))
scientist.addAInsert("sky", "streaming").add_relevance(random.randint(0, 100))

match = scientist.getCollectionsByLastRelevanceCount(50, "streaming")
x: scientist.Collection
for x in match:
    print(x.get_name())
    print(x.get_last_relevance_count())
