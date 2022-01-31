# Datenbank Tables

Hier werden einmal alle benötigten datenbank tabels gelistet mit namen und typen

Es werden allgemein verständliche typen genutzt, da datenbank vielleicht spezielle typen nicht unterstützen könnten.

Nebenbei wird geschrieben wie folgendes auch in python genutzt wird.

Im Laufe der Zeit wird die möglichkeit der Personalisierung aller Variablen in diesem System nachgerüstet, 
somit kann man dann eigene Table Namen und Column Namen vergeben, womit das system arbeitet.

### Collection

Name: `collection`

| name | type | type in python |
| ---- | ---- | ---- |
| id | integer | int |
| identifier | integer | int |
| name | string | str |
| category | string | json / list |
| extraSearch | string | str |
| count | integer | int |
| ignore | string | bool |

### User

Name: `user`

| name | type | type in python |
| ---- | ---- | ---- |
| noch | nicht | eingefügt |

_in entwicklung_


### Search Connections

Name: `searchConnections`

| name | type | type in python |
| ---- | ---- | ---- |
| name | string | str |
| data | string | json / dict |

# Connected Categorys

Name: `connectedCategorys`

| name | type | type in python |
| ---- | ---- | ---- |
| name | string | str |
| data | string | json / dict |