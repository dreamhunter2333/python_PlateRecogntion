#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'jinmu333'

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
import tkinter.messagebox
from PIL import Image, ImageTk
import os
import lib.img_sql as img_sql


class Login(ttk.Frame):
    thread_run = False
    img_sql.create_signsql()

    def __init__(self, win):
        ttk.Frame.__init__(self, win)
        frame0 = ttk.Frame(self)
        frame1 = ttk.Frame(self)
        frame2 = ttk.Frame(self)
        frame3 = ttk.Frame(self)
        win.title("登录到车牌识别系统")
        win.minsize(850, 600)
        self.center_window()

        self.pilImage = Image.open("./pic/login.png")
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.image233 = tk.Label(win, image=self.tkImage)
        self.image233.pack(side=TOP)

        frame0.pack(side=TOP, fill=tk.Y, expand=1)
        frame1.pack(side=TOP, fill=tk.Y, expand=1)
        frame2.pack(side=TOP, fill=tk.Y, expand=1)
        frame3.pack(side=TOP, fill=tk.Y, expand=1)

        self.t1 = "登录到车牌 识别 系统"
        self.text_change = ttk.Label(frame0, text=self.t1, font=('Times', '20'))
        self.text_change.pack(side=TOP)
        self.change_button = ttk.Button(frame0, text="切换系统", width=15, command=self.change)
        self.change_button.pack(side=TOP)

        self.label_account = ttk.Label(frame1, text='账号: ')
        self.label_account.pack(side=LEFT)
        self.input_account = ttk.Entry(frame1, width=30)
        self.input_account.pack(side=RIGHT)
        self.label_password = ttk.Label(frame2, text='密码: ')
        self.label_password.pack(side=LEFT)
        self.input_password = ttk.Entry(frame2, show='*', width=30)
        self.input_password.pack(side=RIGHT)
        self.input_password.bind('<Key-Return>', self.login)
        self.signup_button = ttk.Button(frame3, text="注册", width=15, command=self.signup_interface)
        self.signup_button.pack(side=LEFT)
        self.login_button = ttk.Button(frame3, text="登录", width=15, command=self.backstage_interface)
        self.login_button.pack(side=RIGHT)

        self.pack(fill=tk.BOTH, expand=tk.YES, padx="10", pady="10")

    def center_window(self):
        screenwidth = log.winfo_screenwidth()
        screenheight = log.winfo_screenheight()
        log.update()
        width = log.winfo_width()
        height = log.winfo_height()
        size = '+%d+%d' % ((screenwidth - width)/2, (screenheight - height)/2)
        log.geometry(size)

    def change(self):
        if self.t1 == "登录到车牌 识别 系统":
            self.t1 = "登录到车牌 对比 系统"
            log.title("登录到车牌对比系统")
            self.text_change.configure(text=self.t1)
        elif self.t1 == "登录到车牌 对比 系统":
            self.t1 = "登录到车牌 搜索 系统"
            log.title("登录到车牌搜索系统")
            self.text_change.configure(text=self.t1)
        elif self.t1 == "登录到车牌 搜索 系统":
            self.t1 = "登录到车牌 数据库搜索 系统"
            log.title("登录到车牌数据库搜索系统")
            self.text_change.configure(text=self.t1)
        elif self.t1 == "登录到车牌 数据库搜索 系统":
            self.t1 = "登录到车牌 认证 系统"
            log.title("登录到车牌认证系统")
            self.text_change.configure(text=self.t1)
        else:
            self.t1 = "登录到车牌 识别 系统"
            log.title("登录到车牌识别系统")
            self.text_change.configure(text=self.t1)

    def signup_interface(self):
        account = self.input_account.get()
        password = self.input_password.get()
        if (account == ""):
            tkinter.messagebox.showinfo(title='车牌识别管理系统', message='账号不能为空')
            return
        if (password == ""):
            tkinter.messagebox.showinfo(title='车牌识别管理系统', message='密码不能为空')
            return
        if img_sql.select_sql(account):
            tkinter.messagebox.showinfo(title='车牌识别管理系统', message='用户名已注册')
            return
        img_sql.sign_sql(account, password)
        tkinter.messagebox.showinfo(title='车牌识别管理系统', message='注册成功，请登录')

    def backstage_interface(self):
        account = self.input_account.get()
        password = self.input_password.get()
        if (account == ""):
            tkinter.messagebox.showinfo(title='车牌识别管理系统', message='账号不能为空')
            return
        if (password == ""):
            tkinter.messagebox.showinfo(title='车牌识别管理系统', message='密码不能为空')
            return
        if not img_sql.select_sql(account):
            tkinter.messagebox.showinfo(title='车牌识别管理系统', message='用户名未注册')
            return
        if (password == img_sql.select_sql(account)):
            tkinter.messagebox.showinfo(title='车牌识别管理系统', message='登录成功')
            # close_window()
            log.state('icon')
            if self.t1 == "登录到车牌 识别 系统":
                os.system("python3 ./main.py")
            elif self.t1 == "登录到车牌 对比 系统":
                os.system("python3 ./match.py")
            elif self.t1 == "登录到车牌 搜索 系统":
                os.system("python3 ./search.py")
            elif self.t1 == "登录到车牌 数据库搜索 系统":
                os.system("python3 ./search_sql.py")
            elif self.t1 == "登录到车牌 认证 系统":
                os.system("python3 ./identification.py")
            log.state('normal')
        else:
            tkinter.messagebox.showinfo(title='车牌识别管理系统', message='密码错误')

    def login(self, self2):
        self.backstage_interface()


def close_window():
    print("log destroy")
    if login.thread_run:
        login.thread_run = False
        login.thread.join(2.0)
    log.destroy()


if __name__ == '__main__':
    log = tk.Tk()

    login = Login(log)
    # close,退出输出destroy
    log.protocol('WM_DELETE_WINDOW', close_window)
    # 进入消息循环
    log.mainloop()
