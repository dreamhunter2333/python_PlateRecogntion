# -*- coding: utf-8 -*-
__author__ = '樱花落舞'
import pymysql

db = pymysql.connect(host = '',  # 远程主机的ip地址，
                     user = '',   # MySQL用户名
                     db = '',   # database名
                     passwd = '',   # 数据库密码
                     port = 3306,  #数据库监听端口，默认3306
                     charset = "utf8")  #指定utf8编码的连接

cur= db.cursor()
sql="select * from sex"
try:
    cur.execute(sql)
    re=cur.fetchall()
    for it in re:
        name = it[0]
        num  = it[1]
        print(name,num)
except Exception as e:
    raise  e
finally:
    db.close()

