#!/usr/bin/python3

import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "qqqqqqqq1", "chepai")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS CARINFO")

# 使用预处理语句创建表
sql = """CREATE TABLE CARINFO (
        TIME VARCHAR(100),
        COLOR1 VARCHAR(100), 
        TEXT1 VARCHAR(100), 
        COLOR2 VARCHAR(100), 
        TEXT2 VARCHAR(100))"""

cursor.execute(sql)

# 关闭数据库连接
db.close()
