class SQLQuery:

    """ 
    Class to make it easier to create SQL queries.
    """

    def __init__(self, table = None):
        self.sql = ""

    def columns_as_str(self, columns):
        if type(columns) == list:
            columns = ["`%s`" % column for column in columns]
            columns = ", ".join(columns)

        return columns

    def select(self, table, columns='*', where=None):

        columns = self.columns_as_str(columns)
        self.sql = "SELECT %s FROM %s" % (columns, table)
        return self

    def where(self, where=None):
        if not where:
            return self
        
        self.sql += " WHERE %s" % where
        return self

    def order_by(self, column_directions:list=None):
        """ columns: list of columns where a column look like e.g: ['column', 'ASC'] """
        if not column_directions:
            return self
        
        order_by = []
        for column_direction in column_directions:
            order_by.append("%s %s" % (column_direction[0], column_direction[1],))
        order_by = ", ".join(order_by)
        self.sql += " ORDER BY %s" % order_by
        return self

    def limit(self, limit=None):
        if not limit:
            return self
        
        self.sql += " LIMIT %s, %s" % (limit[0], limit[1])
        return self

    def insert(self, table, columns):

        columns = self.columns_as_str(columns)
        self.sql = "INSERT INTO %s (%s) VALUES " % (table, columns)

        placeholders = []
        for _ in columns.split(", "):
            placeholders.append("%s")
        placeholders = ", ".join(placeholders)
        self.sql += "(%s)" % placeholders

        return self

    def update(self, table, columns):

        self.sql = "UPDATE %s SET " % table
        set_columns = []

        columns = self.columns_as_str(columns)
        for column in columns.split(", "):
            # e.g. `column` = %s
            set_columns.append("%s = %%s" % column)

        set_columns = ", ".join(set_columns)

        self.sql += set_columns


        return self

    def delete(self, table, where=None):

        self.sql = "DELETE FROM %s" % table
        self.where(where)

        return self

    def get_query(self):
        sql = self.sql
        self.sql = ""
        return sql

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
