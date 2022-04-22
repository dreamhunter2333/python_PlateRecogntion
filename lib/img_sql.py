#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'jinmu333'

import pymysql

from .config import settings


def get_db():
    try:
        # 打开数据库连接
        return pymysql.connect(
            host=settings.host,
            port=settings.port,
            user=settings.user,
            passwd=settings.passwd,
            database=settings.database
        )
    except Exception as e:
        print("数据库连接失败", e)
        return


def sql(TIME, COLOR1, TEXT1, COLOR2, TEXT2, API, SOURCE):
    # 打开数据库连接
    db = get_db()
    if not db:
        return
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO CARINFO(TIME, \
       COLOR1, TEXT1, COLOR2, TEXT2, API, SOURCE) \
       VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
        (TIME, COLOR1, TEXT1, COLOR2, TEXT2, API, SOURCE)

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print("数据库写入成功")
    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        print("数据库写入失败", e)

    # 关闭数据库连接
    db.close()


def create_sql():
    # 打开数据库连接
    db = get_db()
    if not db:
        return
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用预处理语句创建表
    sql = """CREATE TABLE IF NOT EXISTS CARINFO (
            TIME VARCHAR(100),
            COLOR1 VARCHAR(100),
            TEXT1 VARCHAR(100),
            COLOR2 VARCHAR(100),
            TEXT2 VARCHAR(100),
            API VARCHAR(100),
            SOURCE VARCHAR(500))"""

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print("数据库创建成功")
    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        print("数据库已存在", e)

    # 关闭数据库连接
    db.close()


def select_sql(NAME):
    # 打开数据库连接
    db = get_db()
    if not db:
        return

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 查询语句
    sql = "SELECT PASSWORD FROM USERS \
            WHERE NAME = ('%s')" % (NAME)

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            password = row[0]
            # 打印结果
            # print("password=%s" %(password))
            # print(password)
            return password
    except Exception as e:
        print(e)
        return 0

    # 关闭数据库连接
    db.close()


def sign_sql(NAME, PASSWORD):
    # 打开数据库连接
    db = get_db()
    if not db:
        return

    # 使用cursor()方法获取操作游标
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO USERS(NAME, PASSWORD) VALUES ('%s', '%s')" % (
        NAME, PASSWORD)

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print("注册数据库写入成功")
    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        print("注册数据库写入失败", e)

    # 关闭数据库连接
    db.close()


def create_signsql():
    # 打开数据库连接
    db = get_db()
    if not db:
        return
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用预处理语句创建表
    sql = """CREATE TABLE IF NOT EXISTS USERS (
            NAME VARCHAR(100),
            PASSWORD VARCHAR(100))"""

    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        print("注册数据库创建成功")
    except Exception as e:
        # 如果发生错误则回滚
        db.rollback()
        print("注册数据库已存在", e)

    # 关闭数据库连接
    db.close()
