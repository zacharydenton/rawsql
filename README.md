# rawsql: A library for *using* SQL. [![Build Status](https://travis-ci.org/zacharydenton/rawsql.svg)](https://travis-ci.org/zacharydenton/rawsql)

rawsql is a Python library that makes it easy to use plain SQL in your projects. You can use it with any [DB-API](https://www.python.org/dev/peps/pep-0249/) compliant database adapter, like `MySQLdb` and `psycopg2`.

## Installation

```shell
$ pip install git+git://github.com/zacharydenton/rawsql
```

## Usage

First you need to put your query in a file:

```sql
-- retrieves a list of unique movie titles for a given year.
select distinct title from movies where year = ?
```

Then you can use the query in Python:

```python
import sqlite3
import rawsql

db = sqlite3.connect(':memory:') # Or any other DB-API connection.
titles_for_year = rawsql.query('sql/titles_for_year.sql', db)

for row in titles_for_year(2010): # Returns a DB-API cursor.
    print(row[0])
```

rawsql makes the comments and the query itself available in the function docstring:

```pycon
>>> help(titles_for_year)
Help on function titles_for_year in module rawsql.core:

titles_for_year(*args, **kwargs)
    retrieves a list of unique movie titles for a given year.

    select distinct title from movies where year = ?;
```

If you wish, you can also include multiple queries in a single file:

```sql
-- name: create_person_table
CREATE TABLE person (
    person_id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(20) UNIQUE NOT NULL,
    age INTEGER NOT NULL
)

-- name: insert_person
INSERT INTO person (
    name,
    age
) VALUES (
    %(name)s,
    %(age)s
)

-- name: find_older_than
SELECT *
FROM person
WHERE age > %s

-- name: find_by_age
SELECT *
FROM person
WHERE age IN (%s)

-- name: update_age
UPDATE person
SET age = %(age)s
WHERE name = %(name)s

-- name: delete_person
DELETE FROM person
WHERE name = %s

-- name: drop_person_table
-- completely destroys the person table!
DROP TABLE person
```

In this case, the queries are made available as a dictionary.

```pycon
>>> queries = rawsql.queries('sql/persons.sql', db)
>>> queries.keys()
['find_older_than', 'insert_person', 'find_by_age', 'drop_person_table', 'delete_person', 'create_person_table', 'update_age']
>>> help(queries['insert_person'])
Help on function insert_person in module rawsql.core:

insert_person(*args, **kwargs)
    INSERT INTO person (
        name,
        age
    ) VALUES (
        %(name)s,
        %(age)s
    );
```

If your query names are valid Python identifiers, you may wish to convert the dictionary to a `namedtuple` for more convenient access.

```pycon
>>> import collections
>>> queries = collections.namedtuple('Queries', queries.keys())(**queries)
>>> help(queries.drop_person_table)
Help on function drop_person_table in module rawsql.core:

drop_person_table(*args, **kwargs)
    completely destroys the person table!

    DROP TABLE person;
```

## Thanks

This project is inspired by [krisajenkins/yesql](https://github.com/krisajenkins/yesql). Check it out if you need something like this for Clojure!

## TODO

- [ ] Return functions with signatures based on the SQL parameters, not just (\*args, \*\*kwargs).
