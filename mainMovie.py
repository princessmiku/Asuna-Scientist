import scientist as sc
from scientist.record import Record
from scientist.displayRecord import DRec
from scientist.databaseConnectorSQLite import DCSqlite
import time, csv

scientist = sc.DataScientist(DCSqlite("./log/test.db"))

rec: Record = scientist.match("Superman")
disp = rec.getAsDRec()
for r in disp.get():
    print(r.name)



#with open("./data/dataset.csv", 'r', encoding='utf-8') as csv_file:
#   csv_reader = csv.reader(csv_file)
#   next(csv_reader)
#   for line in csv_reader:
#       name = line[11]
#       extras = line[1] + " " + " ".join(line[16].split("|")) + " " + line[19]
#       categorys: list[str] = line[9].split("|")
#       scientist.addElement(name=name, extraSearchs=extras, _category=categorys)
#scientist.recreateIndex()

#print("-------------------------------")
#rec: Record = scientist.match("Spider")
#rec.setResult(6)
#scientist.insertRecord(rec)
#startTime = time.time()
#rec: Record = scientist.match("Spider")
#endTime = time.time()
#disp = DRec(rec)
#for r in disp.get():
#   print(r.name)
#
#print("Searched in", endTime - startTime, "s, in ", len(scientist.get("index")), " different data")
#scientist.save()
