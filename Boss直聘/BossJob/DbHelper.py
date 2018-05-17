# -*- coding:utf-8 _*-  
""" 
@author:Jianxiong Rao 
@file: DbHelper.py 
@time: 2018/05/17 
"""
import MySQLdb
from scrapy.utils.project import get_project_settings  # 导入settings配置


class DbHelper():
    def __init__(self):
        self.settings = get_project_settings()
        self.host = self.settings['MYSQL_HOST']
        self.port = self.settings['MYSQL_PORT']
        self.user = self.settings["MYSQL_USER"]
        self.passwd = self.settings['MYSQL_PASSWORD']
        self.db = self.settings['MYSQL_DBNAME']

    # 连接到mysql,注意不是连接到具体的数据库，中间件也有此操作
    def connectMysql(self):
        conn = MySQLdb.connect(host=self.host,
                               post=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               charset='utf8')  # 指定为utf8 OK
        return conn

    # 连接到数据库
    def connectDatabase(self):
        conn = MySQLdb.connect(host=self.host,
                               post=self.port,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.db,
                               charset='utf8')  # 指定为utf8 OK
        return conn

    # 创建数据库
    def createDatabase(self):
        conn = self.connectMysql()
        sql = "create database if not exists " + self.db
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    # 创建表
    def createTable(self, sql):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()

    # 插入数据
    def insert(self, sql, *params):  # *代表个数不确定，传递元组过来即可
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()  # 注意要commit
        cur.close()
        conn.close()

    # 更新数据
    def update(self, sql, *params):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()  # 注意要commit
        cur.close()
        conn.close()

    # 删除数据
    def delete(self, sql, *params):
        conn = self.connectDatabase()

        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()


# 测试
class TestDBHelper():
    def __init__(self):
        self.dbHelper = DbHelper()

    # 创建数据库
    def testCreateDatabase(self):
        self.dbHelper.createDatabase()

    # 创建表
    def testCreateTable(self):
        sql = '''create table BossJob(id int primary key auto_increment,
        company_name varchar(50),job varchar(100),salary varchar(30),experience varchar(10),situation varchar(10),
        publish_time varchar(20),publish_person varchar(20),
        company_link varchar(100)'''
        self.dbHelper.createTable(sql)


if __name__ == "_main__":
    try:
        helper = TestDBHelper()
        helper.testCreateDatabase()
        helper.testCreateTable()
    except Exception as e:
        print(str(e))
