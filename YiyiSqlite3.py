# -*- coding: UTF-8 -*-
import sqlite3

import os


class Sqlite3db:
    def __init__(self, sqlite_file):
        self.conn = sqlite3.connect(sqlite_file)
        self.conn.text_factory = str
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def executeUpdate(self, sql, ob):
        """
        数据库的插入、修改函数
        :param sql: 传入的SQL语句
        :param ob: 传入数据
        :return: 返回操作数据库状态
        """
        try:
            self.c.executemany(sql, ob)
            i = self.conn.total_changes
        except Exception as e:
            print('错误类型： ', e)
            return False
        finally:
            self.conn.commit()
        if i > 0:
            return True
        else:
            return False

# sqlite3db = Sqlite3db()
if __name__ == '__main__':
    sq = Sqlite3db(':memory:')
