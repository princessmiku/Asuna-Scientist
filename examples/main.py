"""
    Example main
"""
import scientist
from scientist import LogSettings, Record, Collection
from scientist.databaseConnectorSQLite import DCSqlite

dbConnector = DCSqlite("mydb.db")
logSet = LogSettings("logger scientist", filemode="w")

sc = scientist.DataScientist(dbConnector, logSet, True)
# scientist.DataScientist(_databaseConnector=dbConnector, _logSettings=logSet, autoRecreateIndex=True)

# run it often it will add it more, so be careful and not confused

# add element
sc.addElement(
    name="Cars",
    extraSearchs="Cars is a 2006 American computer-animated sports comedy film produced by Pixar Animation"
                 " Studios and released by Walt Disney Pictures. (Wikipedia)",
    _category=["cars", "disney", "pixar", "route 66", "Lightning McQueen", "Matter"],
    identifikator=1,
)

# add element
sc.addElement(
    name="Iron Man",
    extraSearchs="Iron Man is a 2008 American superhero film based on the Marvel Comics character of the same name. "
                 "Produced by Marvel Studios and distributed by Paramount Pictures, "
                 "it is the first film in the Marvel Cinematic Universe (MCU).",
    _category=["iron man", "marvel", "disney", "tony stark", "superhero", "American superhero film"],
    identifikator=2,
)
# create a index with current data
sc.recreateIndex()
# search
rec: Record = sc.match("Cars")
# display record results
dRec = rec.getAsDRec()
res: Collection
for res in dRec.get():
    print(res.name)

# choose
rec.setResult(0)

# give it back
sc.insertRecord(rec)

# save it
# sc.save()
