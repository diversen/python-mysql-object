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

# Insert
mysql_object.insert({"title": "test"})

# Affected rows
print(mysql_object.rows_affected(), "rows affected")

# Insert ID
print(mysql_object.insert_id(), "last insert id")

# fetchone
row = mysql_object.fetchone(where="title = %s", placeholder_values=("test",))
if row:
    print(row, "fetchone")

mysql_object.insert({"title": "test 2"})

# fetchall
rows = mysql_object.fetchall(where="title = %s", placeholder_values=("test",))
print(rows, "fetchall",)

# update
mysql_object.update(cols_and_values={"title": "new test"}, where="title = %s", placeholder_values=("test",))
print(mysql_object.rows_affected(), "rows affected")

# fetchall
rows = mysql_object.fetchall(where="title = %s OR title = %s", placeholder_values=("new test", "test 2",))
print("fetchall", rows)

# Make a custom SQL query
query = SQLQuery()
query.select("tests")
query.where("title = %s")
query.order_by([['title', 'DESC'], ['description', 'ASC']])
query.limit([0, 2])

# Get SQL query as string
query = query.get_query()
print("query", query)

# Get all rows using the query
rows = mysql_object.fetchall_query(query, placeholder_values=("new test",))
print("fetchall_query", rows)

# Get one row usng the query
row = mysql_object.fetchone_query(query, placeholder_values=("new test",))
print("fetchone_query", row)

# delete both rows
mysql_object.delete(where="title = %s OR title = %s", placeholder_values=("new test", "test 2",))


