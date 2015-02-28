import os
import uuid
import sqlite3
import unittest
from contextlib import closing
import rawsql

def relative(filename):
    return os.path.join(os.path.dirname(__file__), filename)

class TestRawsql(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        with self.db:
            self.db.execute('CREATE TABLE items (id INT, uuid TEXT)')
            self.items = {i + 1: str(uuid.uuid4()) for i in range(10)}
            self.db.executemany('INSERT INTO items (id, uuid) VALUES (?, ?)', self.items.items())

    def tearDown(self):
        self.db.close()

    def test_single_query(self):
        fetch_by_id = rawsql.query(relative('sql/fetch_by_id.sql'))
        for id, uuid in self.items.items():
            db_id, db_uuid = next(fetch_by_id(self.db, id))
            self.assertEqual(db_id, id)
            self.assertEqual(db_uuid, uuid)

    def test_default_connection(self):
        fetch_by_id = rawsql.query(relative('sql/fetch_by_id.sql'), self.db)
        for id, uuid in self.items.items():
            db_id, db_uuid = next(fetch_by_id(id))
            self.assertEqual(db_id, id)
            self.assertEqual(db_uuid, uuid)

    def test_docstring(self):
        fetch_by_id = rawsql.query(relative('sql/fetch_by_id.sql'))
        self.assertTrue(fetch_by_id.__doc__.startswith("retrieves a single record by id."))

    def test_name(self):
        fetch_by_id = rawsql.query(relative('sql/fetch_by_id.sql'))
        self.assertEqual(fetch_by_id.__name__, "fetch_by_id")

    def test_sql(self):
        fetch_by_id = rawsql.query(relative('sql/fetch_by_id.sql'))
        self.assertTrue(sqlite3.complete_statement(fetch_by_id.sql))

    def test_specified_cursor(self):
        fetch_by_id = rawsql.query(relative('sql/fetch_by_id.sql'), self.db)
        c = self.db.cursor()
        returned_c = fetch_by_id(1, cursor=c)
        self.assertEqual(c, returned_c)

    def test_multiple(self):
        queries = rawsql.queries(relative('sql/persons.sql'))
        expected = [
            'create_person_table',
            'insert_person',
            'find_older_than',
            'find_by_age',
            'update_age',
            'delete_person',
            'drop_person_table'
        ]
        self.assertEqual(len(queries.keys()), len(expected))
        self.assertEqual(queries['drop_person_table'].sql, 'DROP TABLE person;')
        self.assertTrue(sqlite3.complete_statement(queries['update_age'].sql))
        self.assertTrue(queries['drop_person_table'].__doc__.startswith('completely destroys the person table!'))

    def test_no_name(self):
        titles_for_year = rawsql.query(relative('sql/titles_for_year.sql'))
        self.assertTrue(sqlite3.complete_statement(titles_for_year.sql))

if __name__ == '__main__':
    unittest.main()
