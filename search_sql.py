#!/usr/bin/python3
# -*- coding: utf-8 -*-
__author__ = 'jinmu333'

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
import tkinter.messagebox
import pymysql


class Search(ttk.Frame):
    def __init__(self, win):
        ttk.Frame.__init__(self, win)
        frame00 = ttk.Frame(self)
        frame0 = ttk.Frame(self)
        frame1 = ttk.Frame(self)
        frame2 = ttk.Frame(self)
        frame3 = ttk.Frame(self)
        frame4 = ttk.Frame(self)
        frame5 = ttk.Frame(self)
        frame6 = ttk.Frame(self)
        win.title("车牌数据库查询")
        # win.minsize(920, 600)
        self.s1 = StringVar()
        self.s2 = StringVar()
        self.s3 = StringVar()
        self.s4 = StringVar()
        self.s5 = StringVar()
        self.s6 = StringVar()

        frame00.pack(side=TOP, fill=tk.Y, expand=1)
        frame0.pack(side=TOP, fill=tk.Y, expand=1)
        frame1.pack(side=TOP, fill=tk.Y, expand=1)
        frame2.pack(side=TOP, fill=tk.Y, expand=1)
        frame3.pack(side=TOP, fill=tk.Y, expand=1)
        frame4.pack(side=TOP, fill=tk.Y, expand=1)
        frame6.pack(side=TOP, fill=tk.Y, expand=1)
        frame5.pack(side=TOP, fill=tk.Y, expand=1)

        self.t = Text(frame00, width=100)
        self.t.pack()
        self.t.insert('1.0', "此处显示查询结果\n")

        self.label0 = ttk.Label(frame0, text='数据库地址：', width=10)
        self.label0.pack(side=LEFT)
        self.input0 = ttk.Entry(frame0, textvariable=self.s1, width=30)
        self.input0.pack(side=RIGHT)

        self.label = ttk.Label(frame1, text='用户名：', width=10)
        self.label.pack(side=LEFT)
        self.input1 = ttk.Entry(frame1, textvariable=self.s2, width=30)
        self.input1.pack(side=RIGHT)

        self.label2 = ttk.Label(frame2, text='密码: ', width=10)
        self.label2.pack(side=LEFT)
        self.input2 = ttk.Entry(frame2, textvariable=self.s3, width=30)
        self.input2.pack(side=RIGHT)

        self.label3 = ttk.Label(frame3, text='数据库名称: ', width=10)
        self.label3.pack(side=LEFT)
        self.input3 = ttk.Entry(frame3, textvariable=self.s4, width=30)
        self.input3.pack(side=RIGHT)

        self.label4 = ttk.Label(frame4, text='数据表名称: ', width=10)
        self.label4.pack(side=LEFT)
        self.input4 = ttk.Entry(frame4, textvariable=self.s5, width=30)
        self.input4.pack(side=RIGHT)

        self.input5 = ttk.Entry(frame6, textvariable=self.s6, width=30)
        self.input5.pack(side=LEFT)
        self.label5 = ttk.Button(frame6, text='关键字查询', width=10, command=self.sql2)
        self.label5.pack(side=RIGHT)

        self.clean_button = ttk.Button(frame5, text="清楚输入信息", width=15, command=self.clean)
        self.clean_button.pack(side=LEFT)
        self.url_face_button = ttk.Button(frame5, text="开始查询", width=15, command=self.sql)
        self.url_face_button.pack(side=LEFT)

        self.pack(fill=tk.BOTH, expand=tk.YES, padx="10", pady="10")

        self.center_window()

    def sql(self):
        self.t.delete(1.0, END)
        NAME1 = self.input0.get() or "localhost"
        USRE1 = self.input1.get() or "python"
        PASS1 = self.input2.get() or "Python12345@"
        SQLNAME1 = self.input3.get() or "chepai"
        TABLENAME1 = self.input4.get() or "CARINFO"
        self.select_sql(NAME1, USRE1, PASS1, SQLNAME1, TABLENAME1)

    def sql2(self):
        self.t.delete(1.0, END)
        NAME1 = self.input0.get() or "localhost"
        USRE1 = self.input1.get() or "python"
        PASS1 = self.input2.get() or "Python12345@"
        SQLNAME1 = self.input3.get() or "chepai"
        TABLENAME1 = self.input4.get() or "CARINFO"
        CARPLA1 = self.input5.get()
        if (CARPLA1==""):
            tkinter.messagebox.showinfo(title='车牌数据库系统', message='关键字不能为空')
            return
        CARPLA1 = "%" + CARPLA1 + "%"
        self.select_sql2(NAME1, USRE1, PASS1, SQLNAME1, TABLENAME1, CARPLA1)

    def clean(self):
        self.s1.set("")
        self.s2.set("")
        self.s3.set("")
        self.s4.set("")
        self.s5.set("")
        self.s6.set("")
        self.t.delete(1.0, END)

    def select_sql(self, NAME, USRE, PASS, SQLNAME, TABLENAME):
        # 打开数据库连接
        try:
            # 打开数据库连接
            db = pymysql.connect(NAME, USRE, PASS, SQLNAME)
        except:
            print("数据库连接失败")
            self.t.insert('1.0', "数据库连接失败")
            return

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 查询语句
        sql = "SELECT * FROM %s" % (TABLENAME)
        # print(sql)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                row2 = str(row) + "\n"
                self.t.insert('1.0', row2)
                self.t.insert('1.0', "-----------------------------"
                                     "------------------------------"
                                     "------------------------------"
                                     "--------\n")
                # print(row)
            # print(results)
        except:
            return 0

        # 关闭数据库连接
        db.close()

    def select_sql2(self, NAME, USRE, PASS, SQLNAME, TABLENAME, CARPLA):
        # 打开数据库连接
        try:
            # 打开数据库连接
            db = pymysql.connect(NAME, USRE, PASS, SQLNAME)
        except:
            print("数据库连接失败")
            self.t.insert('1.0', "数据库连接失败")
            return

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 查询语句
        sql = "SELECT * FROM %s WHERE TEXT1 like ('%s') or TEXT2 like ('%s') " \
              "or API like ('%s') or COLOR1 like ('%s') or COLOR2 like ('%s')" \
                % (TABLENAME, CARPLA, CARPLA, CARPLA, CARPLA, CARPLA)
        # print(sql)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                row2 = str(row) + "\n"
                self.t.insert('1.0', row2)
                self.t.insert('1.0', "-----------------------------"
                                     "------------------------------"
                                     "------------------------------"
                                     "--------\n")
                # print(row)
            # print(results)
        except:
            return 0

        # 关闭数据库连接
        db.close()

    def center_window(self):
        screenwidth = search.winfo_screenwidth()
        screenheight = search.winfo_screenheight()
        search.update()
        width = search.winfo_width()
        height = search.winfo_height()
        size = '+%d+%d' % ((screenwidth - width)/2, (screenheight - height)/2)
        search.geometry(size)


def close_window():
    print("search destroy")
    search.destroy()


if __name__ == '__main__':
    search = tk.Tk()

    search2 = Search(search)
    # close,退出输出destroy
    search.protocol('WM_DELETE_WINDOW', close_window)
    # 进入消息循环
    search.mainloop()



