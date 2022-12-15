class SQLQuery:

    """ 
    Class to make it easier to create SQL queries.
    """

    def __init__(self, table: str = None):
        self.sql = ""
        self.table = table

        # List of values to use with placeholders, extracted from a dict
        self.placeholder_values = None

    def columns_as_str(self, columns):
        if type(columns) == list:
            columns = ["`%s`" % column for column in columns]
            columns = ", ".join(columns)

        return columns

    def select(self, table: str, columns='*'):

        columns = self.columns_as_str(columns)
        self.sql = "SELECT %s FROM `%s`" % (columns, table)
        return self

    def where(self, where: str = None):
        if not where:
            return self

        self.sql += " WHERE %s" % where
        return self

    def where_simple(self, where: dict = None):
        """ where: dict of columns and values """
        if not where:
            return self

        columns, values = self.get_columns_and_values(where)
        self.placeholder_values = values

        where = []
        for column in columns:
            where.append("%s = %%s" % column)

        where = " AND ".join(where)
        self.sql += " WHERE %s" % where
        return self

    def order_by(self, column_directions: list = None):
        """ columns: list of columns where a column look like e.g: ['column', 'ASC'] """
        if not column_directions:
            return self

        if type(column_directions[0]) == str:
            column_directions = [column_directions]

        order_by = []
        for column_direction in column_directions:
            order_by.append("%s %s" %
                            (column_direction[0], column_direction[1],))
        order_by = ", ".join(order_by)
        self.sql += " ORDER BY %s" % order_by
        return self

    def limit(self, limit: list = None):
        if not limit:
            return self

        self.sql += " LIMIT %s, %s" % (limit[0], limit[1])
        return self

    def insert(self, table: str, columns: list):

        columns = self.columns_as_str(columns)
        self.sql = "INSERT INTO %s (%s) VALUES " % (table, columns)

        placeholders = []
        for _ in columns.split(", "):
            placeholders.append("%s")

        placeholders = ", ".join(placeholders)
        self.sql += "(%s)" % placeholders

        return self

    def update(self, table: str, columns: list):

        self.sql = "UPDATE %s SET " % table
        set_columns = []

        columns = self.columns_as_str(columns)
        for column in columns.split(", "):
            set_columns.append("%s = %%s" % column)

        set_columns = ", ".join(set_columns)

        self.sql += set_columns
        return self

    def update_simple(self, table: str, values: dict, where: dict = None):

        self.update(table, list(values.keys()))
        self.where_simple(where)
        self.placeholder_values = tuple(values.values()) + self.get_placeholder_values()

        return self
        

    def delete(self, table, where=None):

        self.sql = "DELETE FROM %s" % table
        self.where(where)

        return self

    def get_query(self):
        sql = self.sql
        self.sql = ""
        return sql

    def get_placeholder_values(self):
        values = self.placeholder_values
        self.placeholder_values = None
        return values

    # make static method
    @staticmethod
    def get_columns_and_values(dict, keys_filter=None):
        """ 
        Returns keys as a list and values as a tuple from a dictionary
        This is easy to use with sql queries
        """

        # only include keys that are in keys_filter
        if keys_filter:
            for key in list(dict.keys()):
                if key not in keys_filter:
                    dict.pop(key, None)

        keys = list(dict.keys())

        if keys_filter:
            keys.sort(key=keys_filter.index)

        values = tuple(dict.values())

        if keys_filter:
            values = tuple(dict[key] for key in keys)

        return keys, values
