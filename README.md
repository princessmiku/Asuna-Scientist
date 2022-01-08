# Scientist V2


Scientist is a self-learning search engine library. It offers the possibility to enter search elements, which it then evaluates. It has a self-learning algorithm to determine results on their revelance to improve them afterwards.

Currently it is still a bit slow, but improvements are already planned.
At the beginning, the results might not be correct, but they will improve over time. Suitable results are also delivered unlearned. These may not always correspond to the best

Features
- Simple handling & clear Desgin
- Possible with all storage methods, for example MySQL, Json, Sqlite
- Easy self learning
- The learning process can be shared

Example found in `./examples`

----

# Installation

### PIP
Currently it is not possible to install it via PIP

### Insert directory
Add the folder ``scienntist`` to your project folder and import it

----
# First steps

### Database

In the examples the database SQLite is used, but it is not necessary.

- Create a database connection with ``databaseConnector`` or use an existing one. More details can be found further down in the text.
- Set up the database with the correct tables, described in ``databaseTables.md``.

Before starting the script, the database must already have been created.

### Include the library in the code

````python
import scientist
from scientist.databaseConnectorSQLite import DCSqlite # example database connector

dbConnector = DCSqlite("./mydb.db")
sc = scientist.DataScientist(dbConnector)
````

### Logging

The whole system has a logger, by default it logs to a file ``s2.log`` in overwrite mode.

To create your own logger, use ``LogSettings``.
In this you can configure the logger as you want it.
A detailed description will follow. It uses the Python module ``logging``.

Only one logger per Python script is possible in the library, if you change it, all will be changed.

**Example**

````python
from scientist.logSettings import LogSettings
import logging
logSet = LogSettings(
    loggerName = "logger scientist",
    filepath = "./s2.log", 
    filemode="a",
    textFmt="[%(asctime)s] [%(levelname)s]: %(message)s >> %(pathname)s:%(lineno)d",
    dateFmt="%Y-%m-%d %H:%M:%S", 
    level=logging.DEBUG
)
````

**Adding the logger at init**

``sc = scientist.DataScientist(dbConnector, logSet)``

**Modify the logger later**

``sc.updateLogger(logSet)``

# Functions

## Load

The library loads all data once at startup, currently it is not possible to force a reload.

## Save

Currently there is no automatic saving, use for it

``sc.save()``

## Update index

The system works with an index, in which it stores important things for searching. This index must always be kept up to date. Since otherwise new realizations are not incorporated.

The library can do this automatically. Initialize it then with the addition ``autoRecreateIndex = True``.

**Example**

```python
sc = scientist.DataScientist(dbConnector, autoRecreateIndex = True)
```

or do it manually with ``sc.recreateIndex()``. Since this function is thread-safe you can also use it with ``autoReCreateIndex``

## Reading results

Results are stored in ``collection``'s. But these are not created directly.
A collection is a class for better handling of the data.

There are two possibilities

### Add Element

The best way to add something to the system. Use ``.addElement()`` to create an entry, the following parameters can be passed.

**Parameters**
- ``name: str (Importand)`` give the entry a name.
- ``extraSearchs: str`` add extra text to the entry, which will be considered in the search. Like a description.
- ``count: int`` add how often the entry has been called. (Currently not connected)
- relevance: int`` add how relevant the entry is. (Currently not connected)
- ``_category: list[str]`` categorize the entry. The input is a list containing the categories.
- ``identifikator: int`` give your entry a recognizable ID to be able to assign the entry to your data, this is not important for the functions or the search.
- ``ignore: bool`` should the entry be invisible?

**Example**
````python
sc.addElement(
    name="Cars", 
    extraSearchs="Cars is a 2006 American computer-animated sports comedy film produced by Pixar Animation Studios and released by Walt Disney Pictures. (Wikipedia)",
    _category=["cars", "disney", "pixar", "route 66", "Lightning McQueen", "Matter"],
    identifikator=1,
)
````

In this example all important entries are present. Even if not all parameters have been used.

### Insert

Use ``.insert()`` to insert a whole text into collections, but this is very inaccurate and will be
will surely be removed soon, because this system only separates words and inserts them, without any

**Parameters**

- ``text: str`` Text to read.
- ``startAsThread: bool`` Should the function start as a thread? If enabled a thread will be returned.
- ``replacer: list[list[str, str]]`` characters to replace on read, example structure `[["a", "b"], [".", " "], ["\n", " "]]`.

**Return**

- ``thread`` returns the running thread if used.

## Search

### Match

Now to use the search function, use ``.match()``. This returns the result based on what was learned.

**Parameters**

- ``search: str`` What is searched for.
- ``user: [User, int]`` Pass the searching user or its ID to personalize the result (Not implemented).

**Return**

- ``Record`` After a search a record is returned which contains the results and is important for the learning progress, so don't lose it.

**Example**
````python
rec = sc.match("Cars")
````

## Evaluate & Display

### Record

A record contains all found results sorted by importance, this is also important for the learning progress

**Important & Interesting Functions**

| Function | Description | Optional parameters
| ---- | ---- | ---- | 
| `setResult(index)` | Set which result was selected |
| `clearResult()` | Set the result back to 0 | |
| `getResult()` | Get the result as `Collection` | |
| `getUser()` | Get the user of the record | |
| `setSearchText()` | Overwrite the text searched with `match > search` |
| `getAsDRec()` | Get the record as `DRec` to display it user friendly | `maxShows = int`


### DRec - Display Record

DRec is a way of displaying the record data nicely, it helps to create a user friendly display. You can think of it like a book.

It displays 25 elements per page by default.

**INIT**

It is possible to initialize using one of the 4 options.

- ``rec.getAsDRec()`` get it directly from the record
- ``rec.getAsDRec(maxShows)`` specify the elements per page
- ``DRec(rec)`` initialize it with the record
- ``DRec(rec, maxShows)`` specify the elements per page


**Functions**

| function | description | optional parameters | return |
| ---- | ---- | ---- | ---- |
| `get()` | Get the current page elements | | list with collections |
| `nextPage()` ` Go to the next page | `amount = 1` specify how many pages to skip | `bool`
| `previousPage()` | Go to the page before | `amount = 1` specify how many pages to skip | `bool` |
| `addIndex()` | - | `amount = 1` how much to add | `bool` |
| `removeIndex()` | - | `amount = 1` how much to remove | `bool` |


The index is the number of the first element from which the displayed elements will be counted, it is possible to move it.


## Insert the result

After something has been selected for the result, it must be inserted into the system.

example for setting the result ``rec.setResult(1)``

The insertion is very simple, this works by simply giving the record back to the library.

``sc.insertRecord(rec)``

The insert can sometimes take a little longer, because it works thread-safe.



----
Used translator for the english version

Translated with www.DeepL.com/Translator (free version)
