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

    def execute(self, query, placeholder_values=None) -> cursor:
        connection = self.connection
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(query, placeholder_values)
        self.cursor = cursor
        return cursor

    def insert_id(self) -> int:
        return self.cursor.lastrowid

    def rows_affected(self) -> int:
        return self.cursor.rowcount

    def fetchone(self, columns='*', where=None, order_by=None, limit=None, placeholder_values: tuple=None) -> dict:
        query = SQLQuery()
        
        query.select(self.get_table(), columns)
        query.where(where)
        query.order_by(order_by)
        query.limit(limit)
        sql = query.get_query()

        cursor = self.execute(sql, placeholder_values)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetchall(self, columns='*', where=None, order_by=None, limit=None, placeholder_values: tuple=None) -> list:
        """ returns a list of dicts"""
        query = SQLQuery()
        
        query.select(self.get_table(), columns)
        query.where(where)    
        query.order_by(order_by)
        query.limit(limit)    
        sql = query.get_query()

        cursor = self.execute(sql, placeholder_values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def fetchall_query(self, query:str, placeholder_values=None) -> list:
        """ using just a query and values returns a list of dicts"""

        cursor = self.execute(query, placeholder_values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def fetchone_query(self, query:str, placeholder_values=None) -> dict:
        """ using just a query and values returns a single dict"""
        cursor = self.execute(query, placeholder_values)
        result = cursor.fetchone()
        cursor.close()
        return result

    def insert(self, cols_and_vals: dict) -> None:

        table = self.get_table()
        columns, values = SQLQuery.get_columns_and_values(cols_and_vals)
        insert_sql = SQLQuery().insert(table, columns).get_query()

        self.execute(insert_sql, values)
        self.connection.commit()

    def update(self, cols_and_values: dict, where: str, placeholder_values:tuple = None) -> None:
        table = self.get_table()
        columns, cols_and_values = SQLQuery.get_columns_and_values(cols_and_values)

        update_sql = SQLQuery().update(table, columns).where(where).get_query()
        cols_and_values = cols_and_values + placeholder_values

        self.execute(update_sql, cols_and_values)
        self.connection.commit()

    def delete(self, where:str, placeholder_values:tuple) -> None:
        table = self.get_table()
        delete_sql = SQLQuery().delete(table).where(where).get_query()
        self.execute(delete_sql, placeholder_values)
        self.connection.commit()


def get_mysql_object(*kargs, **kwargs) -> MySQLObject:
    """Returns a MySQLObject instance"""

    try:
        return get_mysql_object.object
    except AttributeError:
        get_mysql_object.object = MySQLObject(*kargs, **kwargs)

    return get_mysql_object.object
