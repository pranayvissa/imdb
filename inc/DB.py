#!/usr/bin/python

import time
import MySQLdb

from Log import printExeptionDetails

class DB():

    def __init__(self):

        self._db = MySQLdb.connect(host = 'localhost',
                                   user = 'root',
                                   passwd = 'root',
                                   db = 'IMDB')

    def __del__(self):
        if self._db:
            self._db.close()


    def execute_query(self, query):
        retry_count = 3
        retry_wait_time = 5
        committed = False

        while committed == False and retry_count > 0:
            try:
                self._cursor = self._db.cursor(MySQLdb.cursors.DictCursor)
                self._cursor.execute(query)
                self._db.commit()
                committed = True
            except:
                printExeptionDetails()
                time.sleep(retry_wait_time)
                retry_count -= 1;

        if retry_count == 0:
            return False

        return True


    def insert_row(self, table, record):

        headers = record.keys()
        values = record.values()

        for i in range(len(values)):
            if type(values[i]) is str:
                values[i] = MySQLdb.escape_string(values[i])

        col_str = '(`' + '`, `'.join(headers) + '`)'
        row_str = "(\"" + "\", \"".join(values) + "\")"

        query = "INSERT IGNORE INTO `%s` %s VALUES %s" % (table,
                                                    col_str,
                                                    row_str)

        cursor = self._db.cursor()
        try:
            self.execute_query(query)
            self._db.commit()
            return cursor.lastrowid
        except MySQLdb.IntegrityError:
            return -1


    def get_id(self, table, condition):

        query = "SELECT `id` from `%s` WHERE %s" % (table, condition)
        cursor = self._db.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query)
            data = cursor.fetchone()
            return int(data['id'])      # returned as tuple
        except MySQLdb.IntegrityError:
            return -1


    def check_row_exist(self, table, condition):

        query = "SELECT `id` from `%s` WHERE %s" % (table, condition)
        cursor = self._db.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute(query)
            data = cursor.fetchone()
            if 'id' in data:
                return True
            else:
                return False
        except MySQLdb.IntegrityError:
            return False

