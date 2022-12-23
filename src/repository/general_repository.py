import mysql.connector


class Repository:
    def __init__(self):
        self._database = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='krubimubi',
            database='database'
        )
        self._cursor = self._database.cursor()
