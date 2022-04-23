#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'jinmu333'

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
import tkinter.messagebox
from PIL import Image, ImageTk, ImageGrab
import requests
from hyperlpr import *
import cv2
from threading import Thread
import lib.img_function as predict
from lib.img_api import api_pic
import lib.screencut as screencut
from time import sleep


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


class Login(ttk.Frame):
    def __init__(self, win):
        ttk.Frame.__init__(self, win)
        frame0 = ttk.Frame(self)
        frame1 = ttk.Frame(self)
        frame2 = ttk.Frame(self)
        frame3 = ttk.Frame(self)
        frame4 = ttk.Frame(self)
        win.title("车牌对比识别")
        win.minsize(920, 600)
        self.center_window()
        self.s1 = StringVar()
        self.s2 = StringVar()

        self.pilImage = Image.open("pic/left.png")
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.image_ctl = tk.Label(frame0, image=self.tkImage)
        self.image_ctl.pack(side=LEFT)

        self.pilImage2 = Image.open("pic/right.png")
        self.tkImage2 = ImageTk.PhotoImage(image=self.pilImage2)
        self.image_ctl2 = tk.Label(frame0, image=self.tkImage2)
        self.image_ctl2.pack(side=RIGHT)

        frame0.pack(side=TOP, fill=tk.Y, expand=1)
        frame4.pack(side=TOP, fill=tk.Y, expand=1)
        frame1.pack(side=TOP, fill=tk.Y, expand=1)
        frame2.pack(side=TOP, fill=tk.Y, expand=1)
        frame3.pack(side=TOP, fill=tk.Y, expand=1)

        self.label = ttk.Label(frame1, text='图片1(左): ')
        self.label.pack(side=LEFT)
        self.input1 = ttk.Entry(frame1, textvariable=self.s1, width=30)
        self.input1.pack(side=LEFT)
        self.face_button1 = ttk.Button(frame1, text="选择文件", width=15, command=self.file1)
        self.face_button1.pack(side=RIGHT)
        self.cut_ctrl2 = ttk.Button(frame1, text="截图选取", width=15, command=self.cut_pic1)
        self.cut_ctrl2.pack(side=RIGHT)
        self.label2 = ttk.Label(frame2, text='图片2(右): ')
        self.label2.pack(side=LEFT)
        self.input2 = ttk.Entry(frame2, textvariable=self.s2, width=30)
        self.input2.pack(side=LEFT)
        self.face_button2 = ttk.Button(frame2, text="选择文件", width=15, command=self.file2)
        self.face_button2.pack(side=RIGHT)
        self.cut_ctrl3 = ttk.Button(frame2, text="截图选取", width=15, command=self.cut_pic2)
        self.cut_ctrl3.pack(side=RIGHT)
        self.clean_button = ttk.Button(frame3, text="清除显示信息", width=15, command=self.cut_clean)
        self.clean_button.pack(side=LEFT)
        self.url_face_button = ttk.Button(frame3, text="网络地址识别", width=15, command=self.url_p)
        self.url_face_button.pack(side=LEFT)
        self.file_pic_button = ttk.Button(frame3, text="本地文件识别", width=15, command=self.file_pic)
        self.file_pic_button.pack(side=RIGHT)

        self.match = ttk.Label(frame4, text='', font=('Times', '20'))
        self.match.pack()

        self.pack(fill=tk.BOTH, expand=tk.YES, padx="10", pady="10")

        self.predictor = predict.CardPredictor()
        self.predictor.train_svm()

    def cut_pic1(self):
        log.state('icon')
        sleep(0.2)
        filename = "tmp/cut1.gif"
        im =ImageGrab.grab()
        im.save(filename)
        im.close()
        w = screencut.MyCapture(log, filename)
        self.cut_ctrl2.wait_window(w.top)
        log.state('normal')
        os.remove(filename)
        self.pic_path = "tmp/cut.png"
        self.pic_cut = Image.open(self.pic_path)
        self.pic_cut.save("tmp/cut1.png")
        self.pic_path = "tmp/cut1.png"
        self.s1.set(self.pic_path)
        self.pilImage3 = Image.open(self.pic_path)
        w, h = self.pilImage3.size
        pil_image_resized = self.resize(w, h, self.pilImage3)
        self.tkImage3 = ImageTk.PhotoImage(image=pil_image_resized)
        self.image_ctl.configure(image=self.tkImage3)

    def cut_pic2(self):
        log.state('icon')
        sleep(0.2)
        filename = "tmp/cut2.gif"
        im =ImageGrab.grab()
        im.save(filename)
        im.close()
        w = screencut.MyCapture(log, filename)
        self.cut_ctrl3.wait_window(w.top)
        log.state('normal')
        os.remove(filename)
        self.pic_path2 = "tmp/cut.png"
        self.pic_cut = Image.open(self.pic_path2)
        self.pic_cut.save("tmp/cut2.png")
        self.pic_path2 = "tmp/cut2.png"
        self.s2.set(self.pic_path2)
        self.pilImage4 = Image.open(self.pic_path2)
        w, h = self.pilImage4.size
        pil_image_resized2 = self.resize(w, h, self.pilImage4)
        self.tkImage4 = ImageTk.PhotoImage(image=pil_image_resized2)
        self.image_ctl2.configure(image=self.tkImage4)

    def center_window(self):
        screenwidth = log.winfo_screenwidth()
        screenheight = log.winfo_screenheight()
        log.update()
        width = log.winfo_width()
        height = log.winfo_height()
        size = '+%d+%d' % ((screenwidth - width)/2, (screenheight - height)/2)
        log.geometry(size)

    def file1(self):
        self.pic_path = askopenfilename(title="选择识别图片", filetypes=[("jpeg图片", "*.jpeg"), ("jpg图片", "*.jpg"), ("png图片", "*.png")])
        self.s1.set(self.pic_path)
        self.pilImage3 = Image.open(self.pic_path)
        w, h = self.pilImage3.size
        pil_image_resized = self.resize(w, h, self.pilImage3)
        self.tkImage3 = ImageTk.PhotoImage(image=pil_image_resized)
        self.image_ctl.configure(image=self.tkImage3)

    def file2(self):
        self.pic_path2 = askopenfilename(title="选择识别图片", filetypes=[("jpeg图片", "*.jpeg"), ("jpg图片", "*.jpg"), ("png图片", "*.png")])
        self.s2.set(self.pic_path2)
        self.pilImage4 = Image.open(self.pic_path2)
        w, h = self.pilImage4.size
        pil_image_resized2 = self.resize(w, h, self.pilImage4)
        self.tkImage4 = ImageTk.PhotoImage(image=pil_image_resized2)
        self.image_ctl2.configure(image=self.tkImage4)

    def url_p(self):
        url1 = self.input1.get()
        url2 = self.input2.get()
        self.url_dpic1(url1)
        self.url_dpic2(url2)
        self.match_pic()

    def file_pic(self):
        if self.pic_path == "":
            tkinter.messagebox.showinfo(title='车牌对比识别系统', message='图片1不能为空')
            return
        else:
            imagepath1 = os.path.exists(self.pic_path)
            if imagepath1 == None:
                tkinter.messagebox.showinfo(title='车牌对比识别系统', message='图片1路径错误')
        if self.pic_path2 == "":
            tkinter.messagebox.showinfo(title='车牌对比识别系统', message='图片2不能为空')
            return
        else:
            imagepath2 = os.path.exists(self.pic_path2)
            if imagepath2 == None:
                tkinter.messagebox.showinfo(title='车牌对比识别系统', message='图片2路径错误')
        self.match_pic()

    def match_pic(self):
        matchstr1 = self.match_path(self.pic_path)
        matchstr2 = self.match_path(self.pic_path2)
        '''Plate1 = HyperLPR_PlateRecogntion(image1)
        # print(Plate1[0][0])
        matchstr1 = Plate1[0][0]
        Plate2 = HyperLPR_PlateRecogntion(image2)
        # print(Plate2[0][0])
        matchstr2 = Plate2[0][0]'''
        if matchstr1==matchstr2:
            matchstr3 = "        车牌相符        "
        else:
            matchstr3 = "        车牌不符        "
        matchstr = matchstr1 + matchstr3 + matchstr2

        self.match.configure(text=str(matchstr))
        self.s1.set("")
        self.s2.set("")
        self.pic_path = ""
        self.pic_path2 = ""

    def match_path(self, pic_path):
        r_c = None
        r_color = None
        textstr = None
        img_bgr = cv2.imread(pic_path)
        first_img, oldimg = self.predictor.img_first_pre(img_bgr)
        th1 = ThreadWithReturnValue(target=self.predictor.img_color_contours, args=(first_img, oldimg))
        th2 = ThreadWithReturnValue(target=self.predictor.img_only_color, args=(oldimg, oldimg, first_img))
        th1.start()
        th2.start()
        r_c, roi_c, color_c = th1.join()
        r_color, roi_color, color_color = th2.join()
        try:
            Plate = HyperLPR_PlateRecogntion(img_bgr)
            print(Plate[0][0])
            r_c = Plate[0][0]
            r_color = Plate[0][0]
        except:
            pass
        if r_c:
            textstr = r_c
        if r_color:
            textstr = r_color
        if not (r_color or r_c):
            textstr = self.api_ctl(pic_path)
        return str(textstr)

    def api_ctl(self, pic_path):
        colorstr, textstr = api_pic(pic_path)
        print(colorstr, textstr)
        return textstr

    def url_dpic1(self, IMAGE_URL):
        if (IMAGE_URL == ""):
            tkinter.messagebox.showinfo('提示', '请输入网址1！')
            return
        r = requests.get(IMAGE_URL)
        with open("tmp/url1.png", 'wb') as f:
            f.write(r.content)
        self.pic_path = "tmp/url1.png"

    def url_dpic2(self, IMAGE_URL):
        if (IMAGE_URL == ""):
            tkinter.messagebox.showinfo('提示', '请输入网址2！')
            return
        r = requests.get(IMAGE_URL)
        with open("tmp/url2.png", 'wb') as f:
            f.write(r.content)
        self.pic_path2 = "tmp/url2.png"

    def resize(self, w, h, pil_image):
        w_box = 400
        h_box = 400
        f1 = 1.0*w_box/w
        f2 = 1.0*h_box/h
        factor = min([f1, f2])
        width = int(w*factor)
        height = int(h*factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def cut_clean(self):
        self.pilImage3 = Image.open("pic/left.png")
        self.tkImage3 = ImageTk.PhotoImage(image=self.pilImage3)
        self.image_ctl.configure(image=self.tkImage3)
        self.pilImage4 = Image.open("pic/right.png")
        self.tkImage4 = ImageTk.PhotoImage(image=self.pilImage4)
        self.image_ctl2.configure(image=self.tkImage4)
        self.s1.set("")
        self.s2.set("")
        self.pic_path = ""
        self.pic_path2 = ""
        self.match.configure(text="")


def close_window():
    print("log destroy")
    log.destroy()


if __name__ == '__main__':
    log = tk.Tk()

    login = Login(log)
    # close,退出输出destroy
    log.protocol('WM_DELETE_WINDOW', close_window)
    # 进入消息循环
    log.mainloop()
