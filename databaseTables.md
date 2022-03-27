# Datenbank Tables

Hier werden einmal alle benötigten datenbank tables gelistet mit namen und typen

Es werden allgemein verständliche typen genutzt, da datenbank vielleicht spezielle typen nicht unterstützen könnten.

Nebenbei wird geschrieben wie folgendes auch in python genutzt wird.

Im Laufe der Zeit wird die möglichkeit der Personalisierung aller Variablen in diesem System nachgerüstet, 
somit kann man dann eigene Table Namen und Column Namen vergeben, womit das system arbeitet.

### Collection

Name: `collection`

Database: `s2data.db`

| name        | type    | type in python |
|-------------|---------|----------------|
| id          | integer | int            |
| identifier  | integer | int            |
| name        | string  | str            |
| category    | text    | json / list    |
| extraSearch | string  | str            |
| count       | integer | int            |
| ignore      | string  | bool           |

### User

Name: `user`

Database: `user.db`

User ist eine separierte datenbank anbindung, da dieses effizienter ist

| name         | type    | extra settings | type in python |
|--------------|---------|----------------|----------------|
| id           | integer |                | int            |
| identifier   | string  |                | str            |
| likes        | text    |                | json           |
| dislikes     | text    |                | json           |
| interested   | text    |                | json           |
| uninterested | text    |                | json           |
| ignored      | string  |                | list           |


`ignored` ignoriert die Collections, keine verbindungen

_in entwicklung_


### Search Connections

Name: `searchConnections`

Database: `s2data.db`

| name | type   | type in python |
|------|--------|----------------|
| name | string | str            |
| data | text   | json / dict    |

# Connected Categorys

Name: `connectedCategorys`

Database: `s2data.db`

| name | type   | type in python |
|------|--------|----------------|
| name | string | str            |
| data | text   | json / dict    |