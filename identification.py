#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
import tkinter.messagebox
import pymysql
from PIL import Image, ImageTk, ImageGrab
from hyperlpr import *
import cv2
import threading
from threading import Thread
import lib.img_function as predict
from lib.img_api import api_pic
import tkinter.messagebox


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return1 = None
        self._return2 = None
        self._return3 = None

    def run(self):
        if self._target is not None:
            self._return1, self._return2, self._return3 = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return1, self._return2, self._return3


class Search(ttk.Frame):
    def __init__(self, win):
        ttk.Frame.__init__(self, win)
        frame00 = ttk.Frame(self)
        frame0 = ttk.Frame(self)
        frame1 = ttk.Frame(self)
        frame2 = ttk.Frame(self)
        frame4 = ttk.Frame(self)
        frame5 = ttk.Frame(self)
        win.title("车牌认证系统")
        win.minsize(650, 570)
        self.s1 = StringVar()

        frame00.pack(side=TOP, fill=tk.Y, expand=1)
        frame0.pack(side=TOP, fill=tk.Y, expand=1)
        frame4.pack(side=TOP, fill=tk.Y, expand=1)
        frame1.pack(side=TOP, fill=tk.Y, expand=1)
        frame2.pack(side=TOP, fill=tk.Y, expand=1)
        frame5.pack(side=TOP, fill=tk.Y, expand=1)

        self.pilImage = Image.open("pic/identification.png")
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.image_ctl = tk.Label(frame00, image=self.tkImage)
        self.image_ctl.pack(side=LEFT)

        self.text = ttk.Label(frame0, text='', font=('Times', '20'))
        self.text.pack()

        self.text2 = ttk.Label(frame4, text='', font=('Times', '20'))
        self.text2.pack()

        self.clean_button0 = ttk.Button(frame1, text="打开/关闭摄像头", width=15, command=self.video)
        self.clean_button0.pack(side=LEFT)
        self.url_face_button0 = ttk.Button(frame1, text="选择照片", width=15, command=self.pic)
        self.url_face_button0.pack(side=LEFT)

        self.input5 = ttk.Entry(frame2, textvariable=self.s1, width=23)
        self.input5.pack(side=LEFT)
        self.label5 = ttk.Button(frame2, text='添加认证', width=10, command=self.add)
        self.label5.pack(side=RIGHT)

        self.clean_button = ttk.Button(frame5, text="清除信息", width=15, command=self.clean)
        self.clean_button.pack(side=LEFT)
        self.url_face_button = ttk.Button(frame5, text="开始查询", width=15, command=self.sql)
        self.url_face_button.pack(side=LEFT)

        self.pack(fill=tk.BOTH, expand=tk.YES, padx="10", pady="10")

        self.center_window()

        self.pic_path = ""
        self.thread_run = False
        self.camera = None

        self.predictor = predict.CardPredictor()
        self.predictor.train_svm()

    def add(self):
        pass

    def video(self):
        if self.thread_run:
            if self.camera.isOpened():
                self.camera.release()
                print("关闭摄像头")
                self.camera = None
                self.thread_run = False
            return
        if self.camera is None:
            self.camera = cv2.VideoCapture(1)
            if not self.camera.isOpened():
                self.camera = None
                print("没有外置摄像头")
                self.camera = cv2.VideoCapture(0)
                if not self.camera.isOpened():
                    print("没有内置摄像头")
                    tkinter.messagebox.showinfo('警告', '摄像头打开失败！')
                    self.camera = None
                    return
                else:
                    print("打开内置摄像头")
            else:
                print("打开外置摄像头")
        self.pic_source = "摄像头"
        self.thread = threading.Thread(target=self.video_thread, args=(self,))
        self.thread.setDaemon(True)
        self.thread.start()
        self.thread_run = True

    def video_thread(delf,self):
        self.thread_run = True
        while self.thread_run:
            _, img_bgr = self.camera.read()
            img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(img)
            w, h = im.size
            pil_image_resized = self.resize(w, h, im)
            self.imgtk = ImageTk.PhotoImage(image=pil_image_resized)
            self.image_ctl.configure(image=self.imgtk)
        print("run end")

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
        self.pic_path = ""
        self.pic_path = askopenfilename(title="选择识别图片", filetypes=[("jpeg图片", "*.jpeg"), ("jpg图片", "*.jpg"), ("png图片", "*.png")])
        self.pilImage3 = Image.open(self.pic_path)
        self.text.configure(text="")
        self.text2.configure(text="")
        w, h = self.pilImage3.size
        pil_image_resized = self.resize(w, h, self.pilImage3)
        self.tkImage3 = ImageTk.PhotoImage(image=pil_image_resized)
        self.image_ctl.configure(image=self.tkImage3)

    def api_ctl(self, pic_path):
        colorstr, text1str = api_pic(pic_path)
        print(colorstr, text1str)
        return text1str

    def picre(self):
        r_c = None
        r_color = None
        text1str = None
        img_bgr = cv2.imread(self.pic_path)
        first_img, oldimg = self.predictor.img_first_pre(img_bgr)
        try:
            th1 = ThreadWithReturnValue(target=self.predictor.img_color_contours, args=(first_img, oldimg))
            th2 = ThreadWithReturnValue(target=self.predictor.img_only_color, args=(oldimg, oldimg, first_img))
            th1.start()
            th2.start()
            r_c, roi_c, color_c = th1.join()
            r_color, roi_color, color_color = th2.join()
        except:
            pass
        try:
            Plate = HyperLPR_PlateRecogntion(img_bgr)
            # print(Plate[0][0])
            r_c = Plate[0][0]
            r_color = Plate[0][0]
        except:
            pass
        if r_c:
            text1str = r_c
        if r_color:
            text1str = r_color
        if not (r_color or r_c):
            text1str = self.api_ctl(self.pic_path)
        print(text1str)
        return text1str

    def sql(self):
        if (self.pic_path == ""):
            tkinter.messagebox.showinfo(title='车牌数据库系统', message='请选择图片或打开摄像头')
            return

        NAME1 = "localhost"
        USRE1 = "python"
        PASS1 = "Python12345@"
        SQLNAME1 = "chepai"
        TABLENAME1 = "CARINFO"
        CARPLA1 = self.picre()
        if CARPLA1 == "":
            return
        # CARPLA1 = "赣"

        CARPLA1 = "%" + CARPLA1 + "%"
        self.select_sql(NAME1, USRE1, PASS1, SQLNAME1, TABLENAME1, CARPLA1)

    def clean(self):
        self.pic_path = ""
        self.text.configure(text="")
        self.text2.configure(text="")
        self.pilImage = Image.open("pic/identification.png")
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.image_ctl.configure(image=self.tkImage)

    def select_sql(self, NAME, USRE, PASS, SQLNAME, TABLENAME, CARPLA):
        textstr = ""
        textstr2 = ""
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
            textstr = str(CARPLA) + "您已认证" + str(p) + "次"
            textstr2 = "上次认证时间: " + str(results[p-1][0])
            print(textstr + "\n" + textstr2)
            self.text.configure(text=textstr)
            self.text2.configure(text=textstr2)
            # print(results)
        except:
            textstr = str(CARPLA) + "您未认证"
            self.text.configure(text=textstr)

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
