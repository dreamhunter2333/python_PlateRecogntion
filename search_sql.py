#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pymysql
import tkinter as tk
import tkinter.messagebox

from tkinter import END, LEFT, RIGHT, TOP, StringVar, Text, ttk

from lib.config import settings


class Search(ttk.Frame):
    def __init__(self, win):
        ttk.Frame.__init__(self, win)

        win.title("车牌数据库查询")

        self.host = StringVar()
        self.port = StringVar()
        self.user = StringVar()
        self.passwd = StringVar()
        self.db = StringVar()
        self.table = StringVar()
        self.keyword = StringVar()

        frame_result = ttk.Frame(self)
        frame_host = ttk.Frame(self)
        frame_user = ttk.Frame(self)
        frame_input = ttk.Frame(self)
        frame_passwd = ttk.Frame(self)
        frame_db = ttk.Frame(self)
        frame_table = ttk.Frame(self)
        frame_clean = ttk.Frame(self)
        frame_keyword = ttk.Frame(self)

        frame_result.pack(side=TOP, fill=tk.Y, expand=1)
        frame_host.pack(side=TOP, fill=tk.Y, expand=1)
        frame_input.pack(side=TOP, fill=tk.Y, expand=1)
        frame_user.pack(side=TOP, fill=tk.Y, expand=1)
        frame_passwd.pack(side=TOP, fill=tk.Y, expand=1)
        frame_db.pack(side=TOP, fill=tk.Y, expand=1)
        frame_table.pack(side=TOP, fill=tk.Y, expand=1)
        frame_keyword.pack(side=TOP, fill=tk.Y, expand=1)
        frame_clean.pack(side=TOP, fill=tk.Y, expand=1)

        self.result = Text(frame_result, width=100)
        self.result.pack()
        self.result.insert('1.0', "此处显示查询结果\n")

        self.host_label = ttk.Label(frame_host, text='数据库地址：', width=10)
        self.host_label.pack(side=LEFT)
        self.host_input = ttk.Entry(
            frame_host, textvariable=self.host, width=30)
        self.host_input.pack(side=RIGHT)

        self.port_lable = ttk.Label(frame_input, text='端口号', width=10)
        self.port_lable.pack(side=LEFT)
        self.port_input = ttk.Entry(
            frame_input, textvariable=self.port, width=30)
        self.port_input.pack(side=RIGHT)

        self.user_label = ttk.Label(frame_user, text='用户名：', width=10)
        self.user_label.pack(side=LEFT)
        self.user_input = ttk.Entry(
            frame_user, textvariable=self.user, width=30)
        self.user_input.pack(side=RIGHT)

        self.passwd_label = ttk.Label(frame_passwd, text='密码: ', width=10)
        self.passwd_label.pack(side=LEFT)
        self.passwd_input = ttk.Entry(
            frame_passwd, textvariable=self.passwd, width=30)
        self.passwd_input.pack(side=RIGHT)

        self.db_label = ttk.Label(frame_db, text='数据库名称: ', width=10)
        self.db_label.pack(side=LEFT)
        self.db_input = ttk.Entry(frame_db, textvariable=self.db, width=30)
        self.db_input.pack(side=RIGHT)

        self.table_label = ttk.Label(frame_table, text='数据表名称: ', width=10)
        self.table_label.pack(side=LEFT)
        self.table_input = ttk.Entry(
            frame_table, textvariable=self.table, width=30)
        self.table_input.pack(side=RIGHT)

        self.keyword_input = ttk.Entry(
            frame_keyword, textvariable=self.keyword, width=30)
        self.keyword_input.pack(side=LEFT)
        self.keyword_button = ttk.Button(
            frame_keyword, text='关键字查询', width=10, command=self.keyword_search)
        self.keyword_button.pack(side=RIGHT)

        self.clean_button = ttk.Button(
            frame_clean, text="清除输入信息", width=15, command=self.clean)
        self.clean_button.pack(side=LEFT)
        self.search_button = ttk.Button(
            frame_clean, text="开始查询", width=15, command=self.search)
        self.search_button.pack(side=LEFT)

        self.pack(fill=tk.BOTH, expand=tk.YES, padx="10", pady="10")

        self.center_window()

    def get_db(self):
        try:
            # 打开数据库连接
            return pymysql.connect(
                host=self.host_input.get() or settings.host,
                port=int(self.port_input.get() or settings.port),
                user=self.user_input.get() or settings.user,
                passwd=self.passwd_input.get() or settings.passwd,
                database=self.db_input.get() or settings.database
            )
        except Exception as e:
            print("数据库连接失败", e)
            return

    def search(self):
        self.result.delete(1.0, END)
        table = self.table_input.get() or "CARINFO"
        # 打开数据库连接
        db = self.get_db()
        if not db:
            self.result.insert('1.0', "数据库连接失败")
            return

        cursor = db.cursor()

        # SQL 查询语句
        sql = "SELECT * FROM %s" % (table)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                row2 = str(row) + "\n"
                self.result.insert('1.0', row2)
                self.result.insert('1.0', "-----------------------------"
                                   "------------------------------"
                                   "------------------------------"
                                   "--------\n")
                # print(row)
            # print(results)
        except Exception as e:
            print(e)
            self.result.insert('1.0', "查询失败" + e)

        db.close()

    def keyword_search(self):
        self.result.delete(1.0, END)
        table = self.table_input.get() or "CARINFO"
        keyword = self.keyword_input.get()

        if (keyword == ""):
            tkinter.messagebox.showinfo(title='车牌数据库系统', message='关键字不能为空')
            return

        keyword = "%" + keyword + "%"
        # 打开数据库连接
        db = self.get_db()
        if not db:
            self.result.insert('1.0', "数据库连接失败")
            return

        cursor = db.cursor()

        # SQL 查询语句
        sql = "SELECT * FROM %s WHERE TEXT1 like ('%s') or TEXT2 like ('%s') " \
              "or API like ('%s') or COLOR1 like ('%s') or COLOR2 like ('%s')" \
            % (table, keyword, keyword, keyword, keyword, keyword)
        # print(sql)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            for row in results:
                row2 = str(row) + "\n"
                self.result.insert('1.0', row2)
                self.result.insert('1.0', "-----------------------------"
                                   "------------------------------"
                                   "------------------------------"
                                   "--------\n")
                # print(row)
            # print(results)
        except Exception as e:
            print(e)
            self.result.insert('1.0', "查询失败" + e)
        # 关闭数据库连接
        db.close()

    def clean(self):
        self.host.set("")
        self.user.set("")
        self.passwd.set("")
        self.db.set("")
        self.table.set("")
        self.keyword.set("")
        self.result.delete(1.0, END)

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
    search_window = Search(search)
    # close,退出输出destroy
    search.protocol('WM_DELETE_WINDOW', close_window)
    # 进入消息循环
    search.mainloop()
