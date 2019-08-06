import sqlite3


class DataSource(object):
    def __init__(self, data_base):
        self.connection_name = data_base

    def sql_select(self, table_name: str, required_fields: list = None, selection_criteria: dict = None) -> list:
        """
        Realisation of SELECT SQLite3 with WHERE criteria 'and' or without WHERE
        :param table_name: name of table for selection from
        :param required_fields: list of fields to return from table in database
        :param selection_criteria: criteria for WHERE in SQL
        :return: list of values from database
        """
        if selection_criteria is None:
            selection_criteria = {}
        if required_fields is None:
            required_fields = []
        with sqlite3.connect(self.connection_name) as connection:
            if selection_criteria:
                selection_criteria = ' and '.join(list(map(lambda x: f"{x}={selection_criteria[x] if type(selection_criteria[x]) != str else self.make_quoted_string(selection_criteria[x])}", selection_criteria.keys())))
            else:
                selection_criteria = 'id'
            required_fields = ' '.join(required_fields) if required_fields else '*'
            sql = f"SELECT {required_fields} FROM {table_name} WHERE {selection_criteria};"
            print(sql)
            cursor = connection.cursor()
            result = list(cursor.execute(sql))
            cursor.fetchall()
            cursor.close()

        return result

    @staticmethod
    def make_quoted_string(string: str) -> str:
        """
        Use this method to apply string values to SQL
        :param string: string variable for input into SQL
        :return: quoted value
        """
        return "\'{}\'".format(string)
