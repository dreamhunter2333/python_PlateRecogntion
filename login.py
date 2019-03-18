# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
import tkinter.messagebox
from PIL import Image, ImageTk
import os
import img_sql


class Login(ttk.Frame):
    thread_run = False
    img_sql.create_signsql()

    def __init__(self, win):
        ttk.Frame.__init__(self, win)
        frame1 = ttk.Frame(self)
        frame2 = ttk.Frame(self)
        frame3 = ttk.Frame(self)
        win.title("车牌识别")
        win.minsize(850, 600)
        self.center_window()

        self.pilImage = Image.open("./pic/login.png")
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.image233 = tk.Label(win, image=self.tkImage)
        self.image233.pack(side=TOP)

        frame1.pack(side=TOP, fill=tk.Y, expand=1)
        frame2.pack(side=TOP, fill=tk.Y, expand=1)
        frame3.pack(side=TOP, fill=tk.Y, expand=1)

        # 创建一个`label`名为`Account: `  
        self.label_account = ttk.Label(frame1, text='账号: ')
        self.label_account.pack(side=LEFT)
        # 创建一个账号输入框,并设置尺寸  
        self.input_account = ttk.Entry(frame1, width=30)
        self.input_account.pack(side=RIGHT)
        # 创建一个`label`名为`Password: `  
        self.label_password = ttk.Label(frame2, text='密码: ')
        self.label_password.pack(side=LEFT)
        # 创建一个密码输入框,并设置尺寸  
        self.input_password = ttk.Entry(frame2, show='*', width=30)
        self.input_password.pack(side=RIGHT)
        # 创建一个注册系统的按钮  
        self.signup_button = ttk.Button(frame3, text="注册", width=15, command=self.signup_interface)
        self.signup_button.pack(side=LEFT)
        # 创建一个注册系统的按钮
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
        if not img_sql.select_sql(account):
            tkinter.messagebox.showinfo(title='车牌识别管理系统', message='用户名未注册')
            return
        if (password == img_sql.select_sql(account)):
            tkinter.messagebox.showinfo(title='车牌识别管理系统', message='登录成功')
            close_window()
            os.system("python3 ./main.py")
        else:
            tkinter.messagebox.showinfo(title='车牌识别管理系统', message='密码错误')


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
