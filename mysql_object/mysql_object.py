from mysql.connector import connect, cursor, Error
from mysql_object.sql_query import SQLQuery

class MySQLObject:

    def __init__(self, host, user, password, database):

        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = self.get_connection()
        self.cursor = None

    def get_connection(self) -> connect:

        return connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def close(self) -> None:
        self.connection.close()

    def set_table(self, table) -> None:
        self.table = table

    def get_table(self) -> str:
        if not self.table:
            raise Exception("No table set. Use set_table() first.")

        return self.table

    def execute(self, query, values=None) -> cursor:
        connection = self.connection
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query, values)
        self.cursor = cursor
        return cursor

    def insert_id(self) -> int:
        return self.cursor.lastrowid

    def rows_affected(self) -> int:
        return self.cursor.rowcount

    def fetchone(self, columns='*', where: str=None, order_by=None, limit=None, values: tuple=None) -> dict:
        query = SQLQuery()
        
        query.select(self.get_table(), columns)
        query.where(where)
        query.order_by(order_by)
        query.limit(limit)
        sql = query.get_query()

        cursor = self.execute(sql, values)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetchall(self, columns='*', where: str=None, order_by=None, limit=None, values: tuple=None) -> list:
        """ returns a list of dicts"""
        query = SQLQuery()
        
        query.select(self.get_table(), columns)
        query.where(where)    
        query.order_by(order_by)
        query.limit(limit)    
        sql = query.get_query()

        cursor = self.execute(sql, values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def fetchall_query(self, query, values=None) -> list:
        """ using just a query and values returns a list of dicts"""
        cursor = self.execute(query, values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def fetchone_query(self, query, values=None) -> dict:
        """ using just a query and values returns a single dict"""
        cursor = self.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        return result

    def insert(self, insert_values: dict) -> None:

        table = self.get_table()
        keys, insert_values = SQLQuery.get_columns_and_values(insert_values)
        insert_sql = SQLQuery().insert(table, keys).get_query()

        self.execute(insert_sql, insert_values)
        self.connection.commit()

    def update(self, update_values: dict, where: str, where_values: tuple = None) -> None:
        table = self.get_table()
        columns, update_values = SQLQuery.get_columns_and_values(update_values)

        update_sql = SQLQuery().update(table, columns).where(where).get_query()
        update_values = update_values + where_values

        self.execute(update_sql, update_values)
        self.connection.commit()

    def delete(self, where, where_values) -> None:
        table = self.get_table()
        delete_sql = SQLQuery().delete(table).where(where).get_query()
        self.execute(delete_sql, where_values)
        self.connection.commit()


def get_mysql_object(*kargs, **kwargs) -> MySQLObject:
    """Returns a MySQLObject instance"""

    try:
        return get_mysql_object.object
    except AttributeError:
        get_mysql_object.object = MySQLObject(*kargs, **kwargs)

    return get_mysql_object.object
