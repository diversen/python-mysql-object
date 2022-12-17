from mysql.connector import Error
from mysql_object import MySQLObject, get_mysql_object
from mysql_object import SQLQuery
from tests.settings import settings

mysql_settings = settings["mysql"]

# Get a single MySQLObject instance from a SQL table name
def get_db_table_object(table) -> MySQLObject:

    # Settings are the same as the ones used in mysql.connector.connect()
    mysql_object = get_mysql_object(**mysql_settings)

    # Set the table name
    mysql_object.set_table(table)
    return mysql_object


# You could also just extend the MySQLObject class and set the table name in the constructor
# Or not set the table name and just set it directly in the methods
# This will give a new instance every time
class MySQLObjectTest(MySQLObject):
    def __init__(self):
        super().__init__(**mysql_settings)

    def insert(self, values):
        query = self.set_table("tests")
        query.insert(values)

# We use the single instance in the following example
# Get a object with the table name set to "tests"
mysql_object = get_db_table_object("tests")

# Insert using a dict of values
mysql_object.insert({"title": "test"})
print(mysql_object.rows_affected(), "rows affected")
print(mysql_object.insert_id(), "last insert id")

# Fetch one using where string and placeholder values
row = mysql_object.fetchone(where="title = %s", placeholder_values=("test",))
# -> dict with column names as keys and values as values
if row:
    print(row, "fetchone_simple")
    

# Or fetch one using a dict of where clauses
row = mysql_object.fetchone_simple(where={"title": "test"})

# You may also add order by and limit
row = mysql_object.fetchone_simple(where={"title": "test"}, order_by=[['title', 'DESC'], ['description', 'ASC']], limit=[0, 1])

# Insert another row
mysql_object.insert({"title": "test 2"})

# Fetchall using where string and placeholder values
rows = mysql_object.fetchall(where="title = %s", placeholder_values=("test",))
# -> List of dicts with column names as keys and values as values
for row in rows:
    print(row, "fetchall")

# Fetchall using a dict of where clauses
rows = mysql_object.fetchall_simple(where={"title": "test"})

# Fetch all using a dict of where clause and a list of order by clause and a list of limit clause
mysql_object.fetchall_simple(where={"title": "test"}, order_by=[['title', 'DESC'], ['description', 'ASC']], limit=[0, 2])

# Update using a dict of values and a dict of where clauses
mysql_object.update_simple(values={"title": "new test"}, where={"title": "test"})

# Update with values if they are found in where, otherwise insert new values
mysql_object.replace(values={"title": "new test"}, where={"title": "test"})

# Make a custom SQL query
query = SQLQuery()
query.select("tests")
query.where("title = %s")
query.order_by([['title', 'DESC'], ['description', 'ASC']])
query.limit([0, 2])
sql = query.get_query()
print("query", sql)
# -> SELECT * FROM `tests` WHERE title = %s ORDER BY `title` DESC, `description` ASC LIMIT 0, 2 

# Fetch all from a custom query
mysql_object.fetchall_query(sql, placeholder_values=("test",))

# Fetch one from a custom query
mysql_object.fetchone_query(sql, placeholder_values=("test",))

# Delete using a dict of where clause
mysql_object.delete_simple(where={"title": "new test"})
mysql_object.delete_simple(where={"title": "test 2"})

# Execute in a single transaction
def test_function():
    mysql_object.insert(values={"title": "transaction test"})
    mysql_object.insert(values={"unknown_column_causing_exception": "transaction test"})

try:
    mysql_object.in_transaction_execute(test_function)
except Error as e:
    # Unknown column 'unknown_column_causing_exception' in 'field list'
    pass

# Get num rows
num_rows = mysql_object.get_num_rows(where={"title": "transaction test"}, column="*")

# The first inserts was successful, but the second one failed
# Anything in the test_function() will be rolled back
print(num_rows) # -> 0

def test_function_working():
    mysql_object.insert(values={"title": "transaction test"})
    mysql_object.insert(values={"title": "transaction test"})

try:
    mysql_object.in_transaction_execute(test_function_working)
except Error as e:
    # No error
    pass

num_rows = mysql_object.get_num_rows(where={"title": "transaction test"}, column="*")

# Both inserts were commited
print(num_rows) # -> 2

# Delete the test rows
mysql_object.delete_simple(where={"title": "transaction test"})

# Close the connection
mysql_object.close()