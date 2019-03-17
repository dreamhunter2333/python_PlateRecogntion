#!/usr/bin/python3

import pymysql


def sql(TIME, COLOR1, TEXT1, COLOR2, TEXT2):
    # 打开数据库连接
    db = pymysql.connect("localhost", "python", "Python12345@", "chepai")

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO CARINFO(TIME, \
       COLOR1, TEXT1, COLOR2, TEXT2) \
       VALUES ('%s', '%s', '%s', '%s', '%s')" % \
        (TIME, COLOR1, TEXT1, COLOR2, TEXT2)

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print("数据库写入成功")
    except:
        # 如果发生错误则回滚
        db.rollback()
        print("数据库写入失败")

    # 关闭数据库连接
    db.close()


def create_sql():
    # 打开数据库连接
    db = pymysql.connect("localhost", "python", "Python12345@", "chepai")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用预处理语句创建表
    sql = """CREATE TABLE CARINFO (
            TIME VARCHAR(100),
            COLOR1 VARCHAR(100), 
            TEXT1 VARCHAR(100), 
            COLOR2 VARCHAR(100), 
            TEXT2 VARCHAR(100))"""

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print("数据库创建成功")
    except:
        # 如果发生错误则回滚
        db.rollback()
        print("数据库已存在")

    # 关闭数据库连接
    db.close()
