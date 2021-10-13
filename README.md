# Scientist

Ein Script welches später Daten analysieren und passende ergebnisse sowie matches für Nutzer ausgeben soll


### Speichern

Aktuell funktioniert das Speichern der daten nicht, dieses müsste man selber unternehmen 

# Funktion

## Setup

```python
import scientist as SC

scientist = SC.DataScientist(None)
```


## Daten einlesen

#### Einlesen eines Textes
```python
for_insert = "" # alles möglches solange es ein strng ist
scientist.insert(for_insert, save_under="collection", startAsThread=False, replacer=[])
```
beim Einlesen eines textes über die funktion wird immer bei einem Leerzeichen getrennt. Werden leerzeichen benötigt
sollte man `.addAInsert()` nutzen.

#### Optionale Variabeln

`save_under` = Setze den  Speicherpunkt der Daten die gelesen werden

`startAsThread` = Startet den Insert als Thread, dies ist geigend wenn man mehrere datenmengen hinzufügen möchte.
Wenn man diese Funktion nutzt bekommt man den laufenden Thread zurück.

`replacer` = Eine möglichkeit nachträglich beim Einlesen Teile des Strings zu replacen, folgender aufbaue wird erwartet `[[".", ".."]]`,
mehrfach repleace sind möglich, füge einfach mehr list objekte hinzu, z.b. `[[".", ".."], ["n", "m"]]`


#### Starten als Thread
```python
# starten als Thread

thread_list = []
thread = scientist.insert(for_insert, startAsThread=True)
thread_list.append(thread)
thread = scientist.insert(for_insert, startAsThread=True)
thread_list.append(thread)

# sobald threads erstellt worden sind kann das programm warten bis diese fertig sind
scientist.waitFinish(thread_list)
```

`.waitFinish()` wartet auf das beenden aller Threads in einer Thread List

#### Hinzufügen eines einzelnen Datensatzes

Es ist auch möglichkeiten einzelne Datensätze einzupflegen, dieses ist um einiges genauer und personalisierbarer

```python
scientist.addAInsert(for_insert, save_under="collection", **kwargs)

# diese funktion gibt eine Collection zurück
col = scientist.addAInsert(for_insert, save_under="collection", **kwargs)
```

`**kwargs` = Alle extra angaben möglich wie in einer Collection `category ` und `id`

Wenn man eine category zuteilt, wird diese automatisch beim Erstellen hinzugefügt, sollte ein eintrag doppelt exestieren
wird diese dann am vorhandenen eintrag hinzugefügt, wenn sie nicht vorhanden ist.

## Generelle Daten nutzung

Das allgemeine daten System läuft über die Funktionen `get(location)` `set(location, data)` `exists(location)` und `remove(location)`

`location` = Der Ort wo die daten gespeichert wurden oder sollen. Location funktioniert mit Punkten als weg angabe.

Beispiel

`collection.user.self` die punkte trennen die einzelne speicher abschnitte ab, wenn in einem wort ein punkt benötigt wird
kann man einfach `\.` machen um diesen ignorieren zu lassen. Bei einem Insert werden alle punkte automatisch so gesetzt damit es nicht
zu fehlern kommt.

`get` = frage die daten an, rückgabe ist entweder ein `dict` oder die gespeicherten daten

`set` = setze daten am angegebenen punkt, falsches setzen kann auch daten überschreiben.

`exists` = frage ab ob an der angegebenen positions sich daten befinden

`remove` = lösche die daten an der angegebenen position

## Funktionen

in allen aufgelisteten Funktionen hier kann eine location auch durch eine liste mit Collections genutzt werden,
es ist nicht nötig immer zwangsweise eine position anzugeben. Da viele Funktionen eine Liste mit den Collections zu rück geben

---

#### Variablen

`search: str` / `to_search: str` = Such Strings, kann ein Wort oder auch ein Text sein, je nach dem was gesucht wird

`location: [str, list]` = Je nach angabe, `str` nutzt daten aus der angegebenen position, `list` wird
die Collections nutzen die in der Liste angegeben sind

`max_matches: int` = Wie viele matches maximal zurück gegeben werden sollen

*weitere folgen*

---

| Funktion | Return | Genauigkeit | Tut genau |
| :------- |:-------: |:-------: | -------: |
| `.getMatch(search, location, max_matches)` | `list` mit matches | ungefähr | Passende machtes suchen |
| `.getCollectionsByRelevanceHigherThen(relevance, location)` | `list` mit matches | genau | Collections mit höherer relevance suchen |
| `.getCollectionsByLastRelevanceCount(relevance, location)` | `list` mit matches | genau | Collections mit einer höherer aktuellen relevance suchen |
| `.getCollectionsByCategory(category, location)` | `list` mit matches | genau | Collections mit den angegebenen Kategorien suchen |
| `.getSearchCollections(to_search, location)` | `list` mit matches | ungefähr | Sucht die angegebenen Collections ab, wie eine Suchmaschine |
| `.getSearchCollectionsWithCounterCheck(to_search, location_one, location_two)` | `list` mit matches | ungefähr | Nutzt Ergebnisse die in beiden Location vorhanden sind und sucht damit. |

Genauigkeit erklärt

`genau` = findet ergebnisse die den anforderungen entsprechen

`ungefähr` = findet ergebnisse die in das Such Schema passen könnten

## Collection

Eine Collection ist das eigentliche Speicher Modul jedes abschnittes.

eine Collection ist wie folgt aufgebaut

#### Initialisierung


mit einer Initialisierung hat man normal nix am hut, darum wird hier nicht genauer drauf eingegangen 
```python
import scientist

Collection = scientist.Collection

col = Collection(name, save_under, category, id)
```

### Funktionen

| Funktion | Was sie tut |
| :------- | :------- |
| `.add_search_text(text)` | fügt such text für die Such funktion hinzu |
| `.get_search_text()` | gibt den suchtext als split zurück |
| `.set_id(id)` | Setze eine ID um später eine einfacher möglichkeit der zuordnung zu haben. |
| `.has_id()` | Frage ab ob eine ID vorhanden ist |
| `.get_id()` | Bekomme die ID |
| `.add_category(category_name)` | Füge eine Kategorie hinzu |
| `.remove_category(category_name)` | Entferne eine Kategorie |
| `.have_category(category_name)` | Frage ab ob die Kategorie/en vorhanden ist/sind |
| `.is_forced_relevance()` | *nicht angeschlossen* |
| `.get_name()` | bekomme den namen im richtigen Format |
| `.add_relevance(relevance)` | füge relevance der Collection hinzu |
| `.set_relevance(relevance)` | setze die relevance auf einen bestimmten wert |
| `.get_last_relevance_count` | Gibt dir den durchschnitt der letzten relevancen wieder |
| `.relevance_count(weight)` | Bekomme die Relevance mit der angegeben gewichtung `0 = count ` oder `100 = relevance`, angaben von `1 - 100` möglich |
| `.add_count(add)` | füge einen count hinzu |

Andere Funktionen sind auf eigene gefahr zu nutzen, sie werden aber deine daten im regel fall nicht extends vernichtend
beschädigen bei falscher nutzung.

In späterer Zeit wird auch hier genauer eingegangen auf alles



.

.

.

.

.

.

.

.

.
.