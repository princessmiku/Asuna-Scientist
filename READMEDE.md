# Scientist V2 - Asuna

Scientist ist eine selbstlernende suchmaschinen Library. Diese bietet die Möglichkeit Such elemente einzupflegen, welche sie dann auswertet. Sie verfügt über einen selbstlernenden Algorytmus um ergebnisse auf ihre Revelanz zu bestimmen um sie anschließend zu verbessern.

Aktuell ist sie noch etwas langsam, verbesserungen sind aber bereits geplant.
Am Anfang könnten ergebnisse nicht richtig sein, diese werden mit laufe der Nutzung besser. Passende ergebnisse werden aber auch unangelernt geliefert. Diese könnten aber nicht immer dem besten entsprechen

Features
- Einfache handhabung & Übersichtliches Desgin
- Möglich mit allen speichermethoden, beispiel MySQL, Json, Sqlite
- Einfaches selbstlernen
- Der Lernprozzes kan geteilt werden

Beispiel in ``./example``

----

# Installation

### PIP
Aktuell ist es nicht möglich es per PIP zu installieren

### Verzeichnis einfügen
Füge den Ordner ``scienntist`` in dein Projekt Ordner ein und importiere es

----
# Erste Schritte

### Datenbank

In den Beispielen wird mit der Datenbank SQLite gearbeitet, diese ist aber nicht notwendig

- Erstelle eine Datenbank verbindung mit ``databaseConnector`` oder nutze bereits vorhandene. Genaueres findet sich weiter unten im Text.
- Richte die Datenbank ein mit den richtigen werden, beschrieben in ``databaseTables.md``

Vor dem Starten des Scripts muss die Datenbank bereits erstellt worden sein.

### Einbinden der Library in den Code

````python
import scientist
from scientist.databaseConnectorSQLite import DCSqlite # example database connector

dbConnector = DCSqlite("./mydb.db")
sc = scientist.DataScientist(dbConnector)
````

### Logging

Das ganze System besitzt einen Logger, standardmäßig loggt es in eine Datei ``s2.log`` im Überschreiben Modus.

Um einen eigenen Logger zu erstellen, nutzt man ``LogSettings``.
In diesem kann man sich den Logger dann Konfigurieren wie man ihn haben möchte.
Eine Genaue Beschreibung wird noch folgen. Es nutzt das Python modul ``logging``

Es ist nur ein Logger pro Python Script möglich in der Library, beim Ändern werden alle geändert

**Beispiel**

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

**Hinzufügen des Loggers beim Init**

``sc = scientist.DataScientist(dbConnector, logSet)``

**Nachträgliches ändern des Loggers**

``sc.updateLogger(logSet)``

# Funktionen

## Laden

Die Library lädt einmal alle Daten beim Start, aktuell ist es nicht möglich ein nochmaliges laden zu erzwingen

## Speichern

Aktuell gibt es kein automatisches Speichern, nutze dafür

``sc.save()``

## Index aktualisieren

Das System arbeitet mit einem Index, in dem er wichtige Sachen für das Suchen speichert. Dieser muss immer aktuell gehalten werden. Da sonst neue Erkenntnisse nicht mit eingearbeitet werden.

Dieses kann das Library auch automatisch übernehmen. Initialisiere sie dann mit dem Zusatz ``autoRecreateIndex = True``.

**Beispiel**

```python
sc = scientist.DataScientist(dbConnector, autoRecreateIndex = True)
```

oder mache es Manuell mit ``sc.recreateIndex()``. Da diese Funktion Thread-Safe kann man diese auch mit dem `autoReCreateIndex` nutzen

## Einlesen von Ergebnissen

Ergebnisse werden in ``Collection``'s gespeichert. Diese werden aber nicht direkt erstellt.
Eine Collection ist eine Klasse zur besseren handhabung der Daten.

Es gibt zwei möglichkeiten

### Add Element

Die beste Methode etwas ins System hinzuzufügen. Nutze ``.addElement()`` um einen Eintrag zu erstellen, folgende Parameter können übergeben werden.

**Parameter**
- ``name: str (Importand)`` gebe dem Eintrag einen Namen.
- ``extraSearchs: str`` füge extra Text dem Eintrag hinzu, welches in der Suche berücksichtigt wird. Wie eine Beschreibung.
- ``count: int`` füge an wie oft der Eintrag bereits aufgerufen wurde. (Aktuell nicht angeschlossen)
- ``relevance: int`` füge an wie Relevant der Eintrag ist. (Aktuell nicht angeschlossen)
- ``_category: list[str]`` kategorisiere den Eintrag. Die Eingabe erfolgt durch eine Liste in dem die Kategorien enthalten sind.
- ``identifikator: int`` gebe deinem Eintrag eine für dich erkennbare Wiedererkennung ID um somit den Eintrag deiner Daten zuordnen zu können, diese ist nicht wichtig für die Funktionen oder der Suche.
- ``ignore: bool`` soll der Eintrag unsichtbar sein?

**Beispiel**

````python
sc.addElement(
    name="Cars", 
    extraSearchs="Cars is a 2006 American computer-animated sports comedy film produced by Pixar Animation Studios and released by Walt Disney Pictures. (Wikipedia)",
    _category=["cars", "disney", "pixar", "route 66", "Lightning McQueen", "Matter"],
    identifikator=1,
)
````

In diesem Beispiel sind alle wichtigen Einträge vorhanden. Auch wenn nicht alle Parameter verwendet worden.

### Insert

Nutze ``.insert()`` für das Einlesen eines ganzen Textes in Collections, dieses ist aber sehr ungenau und
wird sicherlich bald entfernt, da dieses System nur wörter trennt und diese einpflegt, ohne drum her rum.

**Parameter**

- ``text: str`` Einzulesender Text.
- ``startAsThread: bool`` Soll die Funktion als Thread starten? Wenn aktiviert wird ein Thread zurückgegeben.
- ``replacer: list[list[str, str]]`` zu ersetzende zeichen beim Einlesen, beispiel aufbau `[["a", "b"], [".", " "], ["\n", " "]]`.

**Rückgabe**
- ``Thread`` gibt wenn genutzt den laufenden Thread zurück.

## Suchen

### Match

Um nun die Such funktion zu verwenden, nutzt man ``.match()``. Dieses gibt einen das Ergebnis anhand des gelerntens zurück.

**Parameter**
- ``search: str`` Was wird gesucht.
- ``user: [User, int]`` Übergebe den Suchenden User oder seine ID um das Ergebnis zu personalisieren (Nicht implementiert)

**Rückgabe**

- ``Record`` Nach einer Suche wird ein Record zurückgegeben der die Ergebnisse beinhaltet und für den Lern fortschritt wichtig ist, also verliere ihn nicht.

**Beispiel**
````python
rec = sc.match("Cars")
````

## Auswerten & Anzeigen

### Record

Ein Record beinhaltet alle gefundenen Ergebnisse sortiert nach Wichtigkeit, dieser ist auch wichtig für den Lernfortschritt

**Wichtige & Interessante Funktionen**

| Funktion | Beschreibung | Optionale Parameter
| ---- | ---- | ---- | 
| `setResult(index)` | Setze welches Ergebnis gewählt wurde | |
| `clearResult()` | Setze das Ergebnis wieder auf 0 | |
| `getResult()` | Bekomme das Ergebnis als `Collection` | |
| `getUser()` | Bekomme den User des Records | |
| `setSearchText()` | Überschreibe den Text mit dem man gesucht hatte `match > search` | |
| `getAsDRec()` | Bekomme den Record als `DRec` um dieses benutzerfreundlich anzuzeigen | `maxShows = int`


### DRec - Display Record

DRec ist eine Möglichkeit der schönen Anzeige der Record Daten, es hilft einen nutzerfreundliche anzeigen zu erstellen. Man kann es sich wie ein Buch vorstellen.

Es werden standardmäßig 25 Elemente pro Seite angezeigt.

**INIT**

Es ist möglich über ein der 4 Möglichkeiten zu initialisieren.

- ``rec.getAsDRec()`` bekomme es direkt über den Record
- ``rec.getAsDRec(maxShows)`` gebe die Elemente pro Seite an
- ``DRec(rec)`` initialisiere es mit dem Record
- ``DRec(rec, maxShows)`` gebe die Elemente pro Seite an


**Funktionen**

| Funktion | Beschreibung | optionale Parameter | Rückgabe |
| ---- | ---- | ---- | ---- |
| `get()` | Bekomme die aktuelle Seiten Elemente | | Liste mit Collections |
| `nextPage()` | Gehe auf die Nächste Seite | `amount = 1` gebe an wie viele Seiten geskippt werden sollen | `bool`
| `previousPage()` | Gehe auf die Seite davor | `amount = 1` gebe an wie viele Seiten geskippt werden sollen | `bool` |
| `addIndex()` | - | `amount = 1` wie viel soll hinzugefügt werden | `bool` |
| `removeIndex()` | - | `amount = 1` wie viel soll entfernt werden | `bool` |


Der Index ist die Zahl des ersten Elementes ab den dann die angezeigten Elemente abgezählt werden, es ist möglich diesen zu versetzten.


## Einpflegen das Ergebnis

Nach dem etwas zum Ergebnis gewählt wurde muss es noch in das System eingepflegt werden.

_beispiel für das Setzen des Ergebnisses ``rec.setResult(1)``_

Das Einpflegen ist sehr einfach, dieses Funktioniert in dem man der Library einfach den Record wieder gibt.

``sc.insertRecord(rec)``

Das einpflegen kann manchmal etwas länger dauern, da diese Thread-Safe arbeitet.


----

Genutzter übersetzer für die englische Version

Translated with www.DeepL.com/Translator (free version)