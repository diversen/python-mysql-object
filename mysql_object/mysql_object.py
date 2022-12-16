from mysql.connector import connect, cursor, Error
from mysql_object.sql_query import SQLQuery


class MySQLObject:

    def __init__(self, *kargs, **kwargs):
        self.connection = self.get_connection(*kargs, **kwargs)
        self.cursor = None
        self.auto_commit = True

    def get_connection(self, *kargs, **kwargs) -> connect:
        return connect(*kargs, **kwargs)

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

    def execute_commit(self, query, placeholder_values=None) -> cursor:
        cursor = self.execute(query, placeholder_values)

        if self.auto_commit == True:
            self.connection.commit()

        return cursor

    def insert_id(self) -> int:
        return self.cursor.lastrowid

    def rows_affected(self) -> int:
        return self.cursor.rowcount

    def in_transaction_execute(self, func):
        """ 
        Used for transactions. Return the result of the function passed in if success.
         """
        try:
            # Disable auto commit internally.
            self.auto_commit = False
            res = func()
            self.connection.commit()
            self.auto_commit = True
            return res
        except Error as e:
            self.connection.rollback()
            self.auto_commit = True 
            raise e

    def get_num_rows(self, where=None, column="*") -> int:
        query = SQLQuery()
        query.select(self.get_table(), f"COUNT({column}) as num_rows")
        query.where_simple(where)
        sql = query.get_query()

        cursor = self.execute(sql, query.placeholder_values)
        result = cursor.fetchone()
        cursor.close()
        return result["num_rows"]

    def fetchone(self, columns='*', where=None, order_by=None, limit=None, placeholder_values: tuple = None) -> dict:
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

    def fetchone_simple(self, columns='*', where=None, order_by=None, limit=None) -> dict:
        """ fetchone_simple uses a 'where' argument containing a dict of columns and values
        and returns a single dict
        """
        query = SQLQuery()

        query.select(self.get_table(), columns)
        query.where_simple(where)
        query.order_by(order_by)
        query.limit(limit)
        sql = query.get_query()

        cursor = self.execute(sql, query.placeholder_values)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetchall(self, columns='*', where=None, order_by=None, limit=None, placeholder_values: tuple = None) -> list:
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

    def fetchall_simple(self, columns='*', where=None, order_by=None, limit=None) -> list:
        """ fetchall_simple uses a 'where' argument containing a dict of columns and values
        and returns a list of dicts
        """
        query = SQLQuery()

        query.select(self.get_table(), columns)
        query.where_simple(where)
        query.order_by(order_by)
        query.limit(limit)
        sql = query.get_query()

        cursor = self.execute(sql, query.get_placeholder_values())
        result = cursor.fetchall()
        cursor.close()
        return result

    def fetchall_query(self, query: str, placeholder_values=None) -> list:
        """ using just a query and values returns a list of dicts"""

        cursor = self.execute(query, placeholder_values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def fetchone_query(self, query: str, placeholder_values=None) -> dict:
        """ using just a query and values returns a single dict"""
        cursor = self.execute(query, placeholder_values)
        result = cursor.fetchone()
        cursor.close()
        return result

    def insert(self, values: dict) -> None:

        table = self.get_table()

        query = SQLQuery()
        insert_sql = query.insert(table, values).get_query()
        values = query.get_placeholder_values()

        self.execute_commit(insert_sql, values)


    def update(self, values: dict, where: str, placeholder_values: tuple = None) -> None:
        table = self.get_table()

        query = SQLQuery()
        update_sql = query.update(table, values).where(where).get_query()
        values = query.get_placeholder_values() + placeholder_values

        self.execute_commit(update_sql, values)

    def update_simple(self, values: dict, where: dict) -> None:
        """ 
        update_simple uses a 'where' argument containing a dict of columns and values
        """
        
        table = self.get_table()

        query = SQLQuery()
        query.update_simple(table, values=values, where=where)
        update_sql = query.get_query()
        placeholder_values = query.get_placeholder_values()

        self.execute_commit(update_sql, placeholder_values)

    def replace(self, values: dict, where: dict) -> None:

        row = self.fetchone_simple(where=where)
        if row:
            self.update_simple(values, where)
        else:
            self.insert(values)

    def delete(self, where: str, placeholder_values: tuple) -> None:
        table = self.get_table()
        delete_sql = SQLQuery().delete(table).where(where).get_query()
        self.execute_commit(delete_sql, placeholder_values)

    def delete_simple(self, where: dict) -> None:
        table = self.get_table()
        query = SQLQuery()
        delete_sql = query.delete(table).where_simple(where).get_query()
        placeholder_values = query.get_placeholder_values()

        self.execute_commit(delete_sql, placeholder_values)


def get_mysql_object(*kargs, **kwargs) -> MySQLObject:
    """Returns a MySQLObject instance"""

    try:
        return get_mysql_object.object
    except AttributeError:
        get_mysql_object.object = MySQLObject(*kargs, **kwargs)

    return get_mysql_object.object
