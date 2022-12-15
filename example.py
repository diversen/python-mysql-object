from mysql_object import MySQLObject, get_mysql_object
from mysql_object import SQLQuery
from tests.settings import settings

# Get a MySQLObject instance from a SQL table name
def get_db_table_object(table) -> MySQLObject:
    mysql_object = get_mysql_object(
            host=settings["mysql"]["host"],
            user=settings["mysql"]["user"],
            password=settings["mysql"]["password"],
            database=settings["mysql"]["database"],
            
            )
    mysql_object.set_table(table)
    return mysql_object

mysql_object = get_db_table_object("tests")


mysql_object.insert({"title": "test"})
print(mysql_object.rows_affected(), "rows affected")
print(mysql_object.insert_id(), "last insert id")

row = mysql_object.fetchone(where="title = %s", placeholder_values=("test",))
if row:
    print(row, "fetchone")

row = mysql_object.fetchone_simple(where={"title": "test"})
if row:
    print(row, "fetchone_simple")

mysql_object.insert({"title": "test 2"})
rows = mysql_object.fetchall(where="title = %s", placeholder_values=("test",))
print(rows, "fetchall",)

rows = mysql_object.fetchall_simple(where={"title": "test"})
print(rows, "fetchall_simple",)

# Update using a dict of values and a dict of where clause
mysql_object.update_simple(values={"title": "new test"}, where={"title": "test"})

# Update values if they are found in where, otherwise insert new values
mysql_object.replace(values={"title": "new test"}, where={"title": "test"})

# Make a custom SQL query
query = SQLQuery()
query.select("tests")
query.where("title = %s")
query.order_by([['title', 'DESC'], ['description', 'ASC']])
query.limit([0, 2])

# Get SQL query as string
query = query.get_query()
print("query", query)

mysql_object.fetchall_query(query, placeholder_values=("test",))

mysql_object.delete_simple(where={"title": "new test"})
mysql_object.delete_simple(where={"title": "test 2"})
