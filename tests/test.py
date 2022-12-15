import unittest
from tests.settings import settings
from mysql_object import SQLQuery
from mysql_object import MySQLObject, get_mysql_object
import sys
sys.path.append(".")


def get_object(table) -> MySQLObject:
    mysql_object = get_mysql_object(
        host=settings["mysql"]["host"],
        user=settings["mysql"]["user"],
        password=settings["mysql"]["password"],
        database=settings["mysql"]["database"],

    )
    mysql_object.set_table(table)
    return mysql_object


class TestMySQLObject(unittest.TestCase):

    def test_get_mysql_object(self):

        # get object one
        mysql_object = get_object("tests")
        self.assertIsInstance(mysql_object, MySQLObject)

        # get the same object again
        same_mysql_object = get_object("tests")
        self.assertEqual(mysql_object, same_mysql_object)

    def test_select_one(self):
        mysql_object = get_object('tests')
        mysql_object.insert({"title": "test"})
        result = mysql_object.fetchone(
            where="title = %s", placeholder_values=("test",))
        self.assertEqual(result["title"], "test")

    def test_select_one_simple(self):
        mysql_object = get_object('tests')
        mysql_object.insert({"title": "test"})
        result = mysql_object.fetchone_simple(where={"title": "test"})
        self.assertEqual(result["title"], "test")

    def test_insert(self):
        mysql_object = get_object('tests')

        mysql_object.delete(where="title = %s", placeholder_values=("test",))
        mysql_object.insert({"title": "test"})
        result = mysql_object.fetchone(
            where="title = %s", placeholder_values=("test",))

        self.assertEqual(result["title"], "test")

    def test_delete(self):

        mysql_object = get_object("tests")
        mysql_object.insert({"title": "test"})
        mysql_object.delete(where="title = %s", placeholder_values=("test",))
        result = mysql_object.fetchone(
            where="title = %s", placeholder_values=("test",))
        self.assertIsNone(result)

    def test_delete_simple(self):

        mysql_object = get_object("tests")
        mysql_object.insert({"title": "test"})
        mysql_object.delete_simple(where={"title": "test"})
        result = mysql_object.fetchone(
            where="title = %s", placeholder_values=("test",))
        self.assertIsNone(result)

    def test_update(self):

        mysql_object = get_object("tests")
        mysql_object.insert(values={"title": "test"})
        mysql_object.update(
            values={"title": "new test"}, where="title = %s", placeholder_values=("test",))

        result = mysql_object.fetchone(
            where="title = %s", placeholder_values=("new test",))
        self.assertEqual(result["title"], "new test")

        mysql_object.delete(where="title = %s", placeholder_values=("test",))

    def test_update_simple(self):

        mysql_object = get_object("tests")
        mysql_object.insert(values={"title": "test"})
        mysql_object.update_simple(
            values={"title": "new test"}, where={"title": "test"})

        result = mysql_object.fetchone(
            where="title = %s", placeholder_values=("new test",))
        self.assertEqual(result["title"], "new test")

        mysql_object.delete(where="title = %s", placeholder_values=("test",))

    def test_insert_id(self):
        mysql_object = get_object("tests")
        mysql_object.insert(values={"title": "test"})
        insert_id = mysql_object.insert_id()
        self.assertTrue(insert_id > 0)

        mysql_object.delete(where="title = %s", placeholder_values=("test",))

    def test_rows_affected(self):
        mysql_object = get_object("tests")
        mysql_object.insert(values={"title": "test"})
        mysql_object.delete(where="title = %s", placeholder_values=("test",))
        result = mysql_object.rows_affected()
        self.assertTrue(result == 1)

    def test_select_one_select_all_simple(self):
        mysql_object = get_object("tests")
        mysql_object.delete(where="title = %s OR title= %s",
                            placeholder_values=("test", "test2",))
        mysql_object.insert(values={"title": "test"})
        mysql_object.insert(values={"title": "test"})

        row = mysql_object.fetchone_simple(where={"title": "test"})
        self.assertEqual(row["title"], "test")

        rows = mysql_object.fetchall_simple(where={"title": "test"})

        self.assertTrue(len(rows) == 2)

    def test_select_one_select_all(self):
        mysql_object = get_object("tests")
        mysql_object.delete(where="title = %s OR title= %s",
                            placeholder_values=("test", "test2",))
        mysql_object.insert(values={"title": "test"})
        mysql_object.insert(values={"title": "test2"})

        row = mysql_object.fetchone(
            where="title = %s", placeholder_values=("test",))
        self.assertEqual(row["title"], "test")

        rows = mysql_object.fetchall(
            where="title = %s OR title = %s", placeholder_values=("test", "test2",))

        self.assertTrue(len(rows) == 2)

    def test_sql_query(self):

        query = SQLQuery().select("tests").where(
            "title = %s OR title = %s").get_query()
        self.assertEqual(
            query, "SELECT * FROM `tests` WHERE title = %s OR title = %s")

        query = SQLQuery()
        query.select("tests")
        query.where("title = %s OR title = %s")
        query.order_by([['test', 'DESC'], ['title', 'ASC']])
        query.limit([30, 10])

        sql = query.get_query()
        self.assertEqual(
            sql, "SELECT * FROM `tests` WHERE title = %s OR title = %s ORDER BY test DESC, title ASC LIMIT 30, 10")

        query = SQLQuery()
        sql = query.select("tests").where("title = %s OR title = %s").order_by(
            ['title', 'ASC']).limit([30, 10]).get_query()

        self.assertEqual(
            sql, "SELECT * FROM `tests` WHERE title = %s OR title = %s ORDER BY title ASC LIMIT 30, 10")


if __name__ == '__main__':
    unittest.main()
