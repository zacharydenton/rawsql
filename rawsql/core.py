import os
from . import parser

def query(filename, connection=None):
    with open(filename) as f:
        return _query_fn(filename, connection, next(parser.parse_queries(f)))

def queries(filename, connection=None):
    with open(filename) as f:
        queries = (_query_fn(filename, connection, q) for q in parser.parse_queries(f))
        return {q.__name__: q for q in queries}

def _execute_sql(cursor, sql, parameters=()):
    cursor.execute(sql, parameters)
    return cursor

def _query_fn(filename, connection, q):
    doc = q['doc']
    sql = q['sql']
    name = q['name']

    if connection is None:
        def execute_sql(*args, **kwargs):
            connection, args = args[0], args[1:]
            cursor = kwargs.pop('cursor', None)
            return _execute_sql(cursor or connection.cursor(), sql, args or kwargs)
    else:
        def execute_sql(*args, **kwargs):
            cursor = kwargs.pop('cursor', None)
            return _execute_sql(cursor or connection.cursor(), sql, args or kwargs)

    if doc:
        execute_sql.__doc__ = doc + '\n\n' + sql
    else:
        execute_sql.__doc__ = sql

    execute_sql.__name__ = name or _filename_to_name(filename)
    execute_sql.sql = sql

    return execute_sql

def _filename_to_name(filename):
    return os.path.splitext(os.path.basename(filename))[0]
