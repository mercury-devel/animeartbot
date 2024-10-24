import sqlite3

class Sqlite:
    def __init__(self):
        self.conn = sqlite3.connect('userdata.db')

    def select(self, cmd):
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        data_list = cursor.fetchall()
        return data_list

    def insert_delete(self, cmd):
        cursor = self.conn.cursor()
        cursor.execute(cmd)
        self.conn.commit()
