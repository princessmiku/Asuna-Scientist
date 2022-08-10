# Datenbank Tables

Hier werden einmal alle benötigten datenbank tables gelistet mit namen und typen

Es werden allgemein verständliche typen genutzt, da datenbank vielleicht spezielle typen nicht unterstützen könnten.

Nebenbei wird geschrieben wie folgendes auch in python genutzt wird.

Im Laufe der Zeit wird die möglichkeit der Personalisierung aller Variablen in diesem System nachgerüstet, 
somit kann man dann eigene Table Namen und Column Namen vergeben, womit das system arbeitet.

Beispiel datenbanken in form von sqlite befinden sich in ``exampels/databases/``

### Collection

Name: `collection`

Database: `s2data.db`

| name         | type        | extra settings                 | type in python |
|--------------|-------------|--------------------------------|----------------|
| id           | integer     | unique, primary, autoincrement | int            |
| identifier   | string(255) | default = 0                    | str            |
| name         | string(255) |                                | str            |
| category     | text / json | default = []                   | list           |
| extra_search | text        |                                | str            |
| count        | integer     | default = 0                    | int            |
| ignore       | int / bool  | default = 0 / False            | bool           |

### User

Name: `user`

Database: `user.db`

User ist eine separierte datenbank anbindung, da dieses effizienter ist

| name         | type        | extra settings      | type in python |
|--------------|-------------|---------------------|----------------|
| id           | integer     | primary key, unique | int            |
| identifier   | string(255) |                     | str            |
| likes        | text / json | default={}          | dict           |
| dislikes     | text / json | default={}          | dict           |
| interested   | text / json | default={}          | dict           |
| uninterested | text / json | default={}          | dict           |
| ignored      | text / json | default=[]          | list           |


`ignored` ignoriert die Collections, keine verbindungen

_in entwicklung_


### Search Connections

Name: `search_connections`

Database: `s2data.db`

| name | type        | extra settings      | type in python |
|------|-------------|---------------------|----------------|
| name | string(127) | primary key, unique | str            |
| data | text / json | default = {}        | dict           |

# Connected Categorys

Name: `connected_categorys`

Database: `s2data.db`

| name | type        | extra settings      | type in python |
|------|-------------|---------------------|----------------|
| name | string      | primary key, unique | str            |
| data | text / json | default = {}        | dict           |
