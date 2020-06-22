"""
author: Nishaoshan
email:790016602@qq.com
time:2020-6-22
env:python3.6
socket,pymysql,M负责数据库处理
"""
import pymysql


class Database:
    def __init__(self):
        self.db = pymysql.connect(
            host="localhost",
            port=3306,
            user="root",
            password="123456",
            database="dict",
            charset="utf8"
        )

    def cursor(self):
        self.cur = self.db.cursor()

    def close(self):
        self.db.close()

    def r(self, name, passwd):
        sql = "select name from user where name=%s;"
        self.cur.execute(sql, [name])
        if self.cur.fetchone():
            return True
        else:
            sql = "insert into user (name,passwd) values (%s,%s);"
            self.cur.execute(sql, [name, passwd])
            self.db.commit()

    def l(self, name, passwd):
        sql = "select name from user where binary name=%s;"
        self.cur.execute(sql, [name])
        if self.cur.fetchone():
            sql = "select * from user where binary name=%s and passwd=%s;"
            self.cur.execute(sql, [name, passwd])
            if self.cur.fetchone():
                return True
            else:
                return "密码不正确"
        else:
            return "用户名不正确"

    def insert_h(self, name, word):
        sql = "select id from user where name=%s;"
        self.cur.execute(sql, [name])
        user_id = self.cur.fetchone()[0]
        sql = "insert into hist (word,user_id) values(%s,%s)"
        self.cur.execute(sql, [word, user_id])
        self.db.commit()

    def query(self, word):
        sql = "select mean from words where word=%s;"
        self.cur.execute(sql, [word])
        res = self.cur.fetchone()
        if res:
            return res[0]
        else:
            return

    def hist(self, name):
        sql = "select name,word,time from user left join hist on user.id=hist.user_id where name=%s order by time desc limit 10; "
        self.cur.execute(sql, [name])
        return self.cur.fetchall()


if __name__ == '__main__':
    Database()
