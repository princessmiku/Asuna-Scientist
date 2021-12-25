import time

import scientist as sc
from scientist import LogSettings, Collection, databaseConnector, Record
from scientist.displayRecord import DRec

import csv

scientist = sc.DataScientist(databaseConnector.DatabaseConnector("./log/test.db", True))

with open("./data/dataset.csv", 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for line in csv_reader:
        name = line[11]
        extras = line[1] + " " + " ".join(line[16].split("|")) + " " + line[19]
        categorys: list[str] = line[9].split("|")
        scientist.addElement(name=name, extraSearchs=extras, _category=categorys)
scientist.recreateIndex()
print("-------------------------------")
startTime = time.time()
rec: Record = scientist.match("Begins")
endTime = time.time()
disp = DRec(rec)
for r in disp.get():
    print(r.name)

print("Searched in", endTime - startTime, "s, in ", len(scientist.get("index")), " different data")
