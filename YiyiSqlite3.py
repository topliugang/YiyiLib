# -*- coding: UTF-8 -*-
import sqlite3

import os


# # This is the qmark style:
# cur.execute("insert into people values (?, ?)", (who, age))
#
# # And this is the named style:
# cur.execute("select * from people where name_last=:who and age=:age", {"who": who, "age": age})

class Sqlite3db:
    def __init__(self, sqlite_file):
        self.sqlite_file = sqlite_file
        self.conn = sqlite3.connect(sqlite_file)
        self.conn.text_factory = str
        # 让查询结果可以用字段名来查询 row['book_id']=row[0]
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    # select操作，返回全部数据
    def select(self, sql, parms=None):
        if parms:
            self.c.execute(sql, parms)
        else:
            self.c.execute(sql)
        return self.c.fetchall()

    # insert, update, delet操作
    def execute(self, sql, parms=None):
        if parms:
            self.c.execute(sql, parms)
        else:
            self.c.execute(sql)
        self.conn.commit()

    # 建表sql，执行多条sql
    def create_table(self, sql):
        self.c.executescript(sql)
        # print "### SQL:executescript:%s" % sql
        self.conn.commit()

sqlite3db = Sqlite3db('./data/db/fuck.db')

# 使用 from YiyiSqlite3 import sqlite3db
