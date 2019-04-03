#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
import tkinter.messagebox
import pymysql
from PIL import Image, ImageTk, ImageGrab


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
        win.title("车牌认证系统")
        win.minsize(650, 570)
        self.s1 = StringVar()

        frame00.pack(side=TOP, fill=tk.Y, expand=1)
        frame0.pack(side=TOP, fill=tk.Y, expand=1)
        frame4.pack(side=TOP, fill=tk.Y, expand=1)
        frame1.pack(side=TOP, fill=tk.Y, expand=1)
        frame2.pack(side=TOP, fill=tk.Y, expand=1)
        frame3.pack(side=TOP, fill=tk.Y, expand=1)
        frame6.pack(side=TOP, fill=tk.Y, expand=1)
        frame5.pack(side=TOP, fill=tk.Y, expand=1)

        self.pilImage = Image.open("pic/identification.png")
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.image_ctl = tk.Label(frame00, image=self.tkImage)
        self.image_ctl.pack(side=LEFT)

        self.text = ttk.Label(frame0, text='', font=('Times', '20'))
        self.text.pack()

        self.text2 = ttk.Label(frame4, text='', font=('Times', '20'))
        self.text2.pack()

        self.clean_button0 = ttk.Button(frame1, text="打开摄像头", width=15, command=self.clean)
        self.clean_button0.pack(side=LEFT)
        self.url_face_button0 = ttk.Button(frame1, text="选择照片", width=15, command=self.pic)
        self.url_face_button0.pack(side=LEFT)

        self.input5 = ttk.Entry(frame2, textvariable=self.s1, width=23)
        self.input5.pack(side=LEFT)
        self.label5 = ttk.Button(frame2, text='添加认证', width=10, command=self.add)
        self.label5.pack(side=RIGHT)

        self.clean_button = ttk.Button(frame5, text="清楚信息", width=15, command=self.clean)
        self.clean_button.pack(side=LEFT)
        self.url_face_button = ttk.Button(frame5, text="开始查询", width=15, command=self.sql)
        self.url_face_button.pack(side=LEFT)

        self.pack(fill=tk.BOTH, expand=tk.YES, padx="10", pady="10")

        self.center_window()

    def add(self):
        pass

    def resize(self, w, h, pil_image):
        w_box = 600
        h_box = 400
        f1 = 1.0*w_box/w
        f2 = 1.0*h_box/h
        factor = min([f1, f2])
        width = int(w*factor)
        height = int(h*factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def pic(self):
        self.pic_path = askopenfilename(title="选择识别图片", filetypes=[("jpeg图片", "*.jpeg"), ("jpg图片", "*.jpg"), ("png图片", "*.png")])
        self.pilImage3 = Image.open(self.pic_path)
        w, h = self.pilImage3.size
        pil_image_resized = self.resize(w, h, self.pilImage3)
        self.tkImage3 = ImageTk.PhotoImage(image=pil_image_resized)
        self.image_ctl.configure(image=self.tkImage3)

    def sql(self):
        NAME1 = "localhost"
        USRE1 = "python"
        PASS1 = "Python12345@"
        SQLNAME1 = "chepai"
        TABLENAME1 = "CARINFO"
        # CARPLA1 = self.input5.get()
        CARPLA1 = "赣"
        if (CARPLA1==""):
            tkinter.messagebox.showinfo(title='车牌数据库系统', message='关键字不能为空')
            return
        CARPLA1 = "%" + CARPLA1 + "%"
        self.select_sql(NAME1, USRE1, PASS1, SQLNAME1, TABLENAME1, CARPLA1)

    def clean(self):
        self.text.configure(text="")
        self.text2.configure(text="")
        self.pilImage = Image.open("pic/identification.png")
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.image_ctl.configure(image=self.tkImage)

    def select_sql(self, NAME, USRE, PASS, SQLNAME, TABLENAME, CARPLA):
        # 打开数据库连接
        try:
            # 打开数据库连接
            db = pymysql.connect(NAME, USRE, PASS, SQLNAME)
        except:
            print("数据库连接失败")
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
            p = 0
            for row in results:
                p += 1
                # print(row)
            # print(results[p-2][0])
            textstr = "您已认证" + str(p) + "次"
            textstr2 = "上次认证时间: " + str(results[p-2][0])
            self.text.configure(text=textstr)
            self.text2.configure(text=textstr2)
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
