#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'jinmu333'

import threading
import time
import tkinter as tk
import cv2
import lib.img_function as predict
import lib.img_math as img_math
import lib.img_excel as img_excel
import lib.img_sql as img_sql
from lib.img_api import api_pic
import lib.screencut as screencut
from threading import Thread
from tkinter import ttk
from tkinter.filedialog import *
from PIL import Image, ImageTk, ImageGrab
import tkinter.messagebox
import requests
from time import sleep
from hyperlpr import *


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return1 = None
        self._return2 = None
        self._return3 = None

    def run(self):
        if self._target is not None:
            try:
                self._return1, self._return2, self._return3 = self._target(*self._args, **self._kwargs)
            except:
                pass

    def join(self):
        Thread.join(self)
        return self._return1, self._return2, self._return3


class Surface(ttk.Frame):
    pic_path = ""
    viewhigh = 600
    viewwide = 600
    update_time = 0
    thread = None
    thread_run = False
    camera = None
    pic_source = ""
    color_transform = {"green": ("绿牌", "#55FF55"), "yello": ("黄牌", "#FFFF00"), "blue": ("蓝牌", "#6666FF")}

    def __init__(self, win):
        ttk.Frame.__init__(self, win)
        frame_left = ttk.Frame(self)
        frame_right1 = ttk.Frame(self)
        frame_right2 = ttk.Frame(self)
        top = ttk.Frame(self)
        win.title("车牌识别")
        win.minsize(850, 700)
        # win.wm_attributes('-topmost', 1)
        self.center_window()
        self.pic_path3 = ""
        self.cameraflag = 0

        top.pack(side=TOP, expand=1, fill=tk.Y)
        reset_ctl = ttk.Button(top, text="重置窗口", width=10, command=self.reset)
        reset_ctl.pack(side=LEFT)
        L1 = ttk.Label(top, text='网络地址:')
        L1.pack(side=LEFT)
        self.p1 = StringVar()
        self.user_text = ttk.Entry(top, textvariable=self.p1, width=45)
        self.user_text.pack(side = LEFT)
        self.user_text.bind('<Key-Return>', self.url_pic2)
        url_ctl = ttk.Button(top, text="识别网络图片", width=20, command=self.url_pic)
        url_ctl.pack(side=RIGHT)

        self.pack(fill=tk.BOTH, expand=tk.YES, padx="10", pady="10")
        frame_left.pack(side=LEFT, expand=1)
        frame_right1.pack(side=TOP, expand=1, fill=tk.Y)
        frame_right2.pack(side=RIGHT, expand=0)
        #ttk.Label(frame_left, text='地址：').pack(anchor="nw")

        self.image_ctl = ttk.Label(frame_left)
        self.image_ctl.pack(anchor="nw")

        ttk.Label(frame_right1, text='形状定位车牌位置：').grid(column=0, row=0, sticky=tk.W)
        from_pic_ctl = ttk.Button(frame_right2, text="来自图片", width=20, command=self.from_pic)
        from_pic_ctl2 = ttk.Button(frame_right2, text="路径批量识别", width=20, command=self.from_pic2)
        from_vedio_ctl = ttk.Button(frame_right2, text="打开/关闭摄像头", width=20, command=self.from_vedio)
        from_video_ctl = ttk.Button(frame_right2, text="拍照并识别", width=20, command=self.video_pic)
        from_img_pre = ttk.Button(frame_right2, text="查看预处理图像", width=20, command=self.show_img_pre)
        clean_ctrl = ttk.Button(frame_right2, text="清除识别数据", width=20, command=self.clean)
        exit_ctrl = ttk.Button(frame_right2, text="api再次识别", width=20, command=self.api_ctl)
        self.cut_ctrl = ttk.Button(frame_right2, text="截图识别", width=20, command=self.cut_pic)
        camera_ctrl = ttk.Button(frame_right2, text="开关摄像头实时识别(测试)", width=20, command=self.camera_flag)

        self.roi_ctl = ttk.Label(frame_right1)
        self.roi_ctl.grid(column=0, row=1, sticky=tk.W)
        ttk.Label(frame_right1, text='形状定位识别结果：').grid(column=0, row=2, sticky=tk.W)
        self.r_ctl = ttk.Label(frame_right1, text="", font=('Times', '20'))
        self.r_ctl.grid(column=0, row=3, sticky=tk.W)
        self.color_ctl = ttk.Label(frame_right1, text="", width="20")
        self.color_ctl.grid(column=0, row=4, sticky=tk.W)
        self.cut_ctrl.pack(anchor="se", pady="5")
        camera_ctrl.pack(anchor="se", pady="5")
        from_vedio_ctl.pack(anchor="se", pady="5")
        from_video_ctl.pack(anchor="se", pady="5")
        from_pic_ctl2.pack(anchor="se", pady="5")
        from_pic_ctl.pack(anchor="se", pady="5")
        from_img_pre.pack(anchor="se", pady="5")
        clean_ctrl.pack(anchor="se", pady="5")
        exit_ctrl.pack(anchor="se", pady="5")

        ttk.Label(frame_right1, text='-------------------------------').grid(column=0, row=5, sticky=tk.W)
        ttk.Label(frame_right1, text='颜色定位车牌位置：').grid(column=0, row=6, sticky=tk.W)
        self.roi_ct2 = ttk.Label(frame_right1)
        self.roi_ct2.grid(column=0, row=7, sticky=tk.W)
        ttk.Label(frame_right1, text='颜色定位识别结果：').grid(column=0, row=8, sticky=tk.W)
        self.r_ct2 = ttk.Label(frame_right1, text="", font=('Times', '20'))
        self.r_ct2.grid(column=0, row=9, sticky=tk.W)
        self.color_ct2 = ttk.Label(frame_right1, text="", width="20")
        self.color_ct2.grid(column=0, row=10, sticky=tk.W)
        ttk.Label(frame_right1, text='-------------------------------').grid(column=0, row=11, sticky=tk.W)

        self.clean()
        self.apistr = None
        img_excel.create_excel()
        img_sql.create_sql()

        self.predictor = predict.CardPredictor()
        self.predictor.train_svm()

    def cut_pic(self):
        #最小化主窗口
        win.state('icon')
        sleep(0.2)
        filename = "tmp/cut.gif"
        im =ImageGrab.grab()
        im.save(filename)
        im.close()
        #显示全屏幕截图
        w = screencut.MyCapture(win, filename)
        self.cut_ctrl.wait_window(w.top)

        #截图结束，恢复主窗口，并删除临时的全屏幕截图文件
        win.state('normal')
        os.remove(filename)
        self.cameraflag = 0
        self.pic_path = "tmp/cut.png"
        self.clean()
        self.pic_source = "来自截图"
        self.pic(self.pic_path)

    def reset(self):
        self.reset2()
        self.reset2()

    def reset2(self):
        win.geometry("850x700")
        self.clean()
        self.thread_run7 = False
        self.count = 0
        self.center_window()

    def center_window(self):
        screenwidth = win.winfo_screenwidth()
        screenheight = win.winfo_screenheight()
        win.update()
        width = win.winfo_width()
        height = win.winfo_height()
        size = '+%d+%d' % ((screenwidth - width)/2, (screenheight - height)/2)
        #print(size)
        win.geometry(size)

    def get_imgtk(self, img_bgr):
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(img)
        w, h = im.size
        pil_image_resized = self.resize2(w, h, im)
        imgtk = ImageTk.PhotoImage(image=pil_image_resized)
        return imgtk

    def resize(self, w, h, pil_image):
        w_box = 200
        h_box = 50
        f1 = 1.0*w_box/w
        f2 = 1.0*h_box/h
        factor = min([f1, f2])
        width = int(w*factor)
        height = int(h*factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def resize2(self, w, h, pil_image):
        width = win.winfo_width()
        height = win.winfo_height()
        w_box = width - 250
        h_box = height - 100
        f1 = 1.0*w_box/w
        f2 = 1.0*h_box/h
        factor = min([f1, f2])
        width = int(w*factor)
        height = int(h*factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def show_roi1(self, r, roi, color):
        if r:
            try:
                roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                roi = Image.fromarray(roi)
                w, h = roi.size
                pil_image_resized = self.resize(w, h, roi)
                self.tkImage1 = ImageTk.PhotoImage(image=pil_image_resized)
                # self.imgtk_roi1 = ImageTk.PhotoImage(image=roi)
                self.roi_ctl.configure(image=self.tkImage1, state='enable')
            except:
                pass
            self.r_ctl.configure(text=str(r))
            self.update_time = time.time()
            try:
                c = self.color_transform[color]
                self.color_ctl.configure(text=c[0], state='enable')
            except:
                self.color_ctl.configure(state='disabled')
        elif self.update_time + 8 < time.time():
            self.roi_ctl.configure(state='disabled')
            self.r_ctl.configure(text="")
            self.color_ctl.configure(state='disabled')

    def show_roi2(self, r, roi, color):
        if r:
            try:
                roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
                roi = Image.fromarray(roi)
                w, h = roi.size
                pil_image_resized = self.resize(w, h, roi)
                self.tkImage2 = ImageTk.PhotoImage(image=pil_image_resized)
                #self.imgtk_roi2 = ImageTk.PhotoImage(image=roi)
                self.roi_ct2.configure(image=self.tkImage2, state='enable')
            except:
                pass
            self.r_ct2.configure(text=str(r))
            self.update_time = time.time()
            try:
                c = self.color_transform[color]
                self.color_ct2.configure(text=c[0], state='enable')
            except:
                self.color_ct2.configure(state='disabled')
        elif self.update_time + 8 < time.time():

            self.roi_ct2.configure(state='disabled')
            self.r_ct2.configure(text="")
            self.color_ct2.configure(state='disabled')

    def camera_flag(self):
        if not self.thread_run:
            tkinter.messagebox.showinfo('提示', '请点击    [打开摄像头]    按钮！')
            return
        if not self.cameraflag:
            self.cameraflag = 1
            self.thread2 = threading.Thread(target=self.video_pic2)
            self.thread2.setDaemon(True)
            self.thread2.start()
            self.thread_run2 = True
        else:
            self.cameraflag = 0
            self.thread_run2 = False
            print("关闭摄像头实时识别 self.cameraflag", self.cameraflag)

    def from_vedio(self):
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
        self.cameraflag = 0
        self.thread = threading.Thread(target=self.vedio_thread)
        self.thread.setDaemon(True)
        self.thread.start()
        self.thread_run = True

    def pic(self, pic_path):
        self.apistr = None
        img_bgr = img_math.img_read(pic_path)
        first_img, oldimg = self.predictor.img_first_pre(img_bgr)
        if not self.cameraflag:
            self.imgtk = self.get_imgtk(img_bgr)
            self.image_ctl.configure(image=self.imgtk)
        th1 = ThreadWithReturnValue(target=self.predictor.img_color_contours, args=(first_img, oldimg))
        th2 = ThreadWithReturnValue(target=self.predictor.img_only_color, args=(oldimg, oldimg, first_img))
        th1.start()
        th2.start()
        r_c, roi_c, color_c = th1.join()
        r_color, roi_color, color_color = th2.join()
        try:
            Plate = HyperLPR_PlateRecogntion(img_bgr)
            # print(Plate[0][0])
            r_c = Plate[0][0]
            r_color = Plate[0][0]
        except:
            pass
        if not color_color:
            color_color = color_c
        if not color_c:
            color_c = color_color
        self.show_roi2(r_color, roi_color, color_color)
        self.show_roi1(r_c, roi_c, color_c)
        # self.center_window()
        localtime = time.asctime(time.localtime(time.time()))
        if not self.cameraflag:
            if not (r_color or color_color or r_c or color_c):
                self.api_ctl2(pic_path)
                return
            value = [localtime, color_c, r_c, color_color, r_color, self.apistr, self.pic_source]
            img_excel.excel_add(value)
            img_sql.sql(value[0], value[1], value[2], value[3], value[4], value[5], value[6])
        print(localtime, "|", color_c, r_c, "|", color_color, r_color, "| ", self.apistr, "|", self.pic_source)

    def from_pic(self):
        self.thread_run = False
        self.thread_run2 = False
        self.cameraflag = 0
        self.pic_path = askopenfilename(title="选择识别图片", filetypes=[("jpeg图片", "*.jpeg"), ("jpg图片", "*.jpg"), ("png图片", "*.png")])
        self.clean()
        self.pic_source = "本地文件：" + self.pic_path
        self.pic(self.pic_path)

    def from_pic2(self):
        self.pic_path3 = askdirectory(title="选择识别路径")
        self.get_img_list(self.pic_path3)
        self.thread7 = threading.Thread(target=self.pic_search, args=(self,))
        self.thread7.setDaemon(True)
        self.thread7.start()
        self.thread_run7 = True

    def get_img_list(self, images_path):
        self.count = 0
        self.array_of_img = []
        for filename in os.listdir(images_path):
            # print(filename)
            try:
                img = cv2.imread(images_path + "/" + filename)
                self.pilImage3 = Image.open(images_path + "/" + filename)
                self.array_of_img.append(images_path + "/" + filename)
                self.count = self.count + 1
                # images_path2 = images_path + "/" + filename
                # self.pic_path2 = images_path2
            except:
                pass
        print(self.array_of_img)

    def pic_search(self, self2):
        self.thread_run7 = True
        print("开始批量识别")
        wait_time = time.time()
        while self.thread_run7:
            while self.count:
                self.pic_path7 = self.array_of_img[self.count-1]

                if time.time()-wait_time > 2:
                    # print(self.pic_path7)
                    print("正在批量识别", self.count)
                    self.clean()
                    self.pic_source = "本地文件：" + self.pic_path7
                    try:
                        self.pic(self.pic_path7)
                    except:
                        pass
                    self.count = self.count - 1
                    wait_time = time.time()
            if self.count == 0:
                self.thread_run7 = False
                print("批量识别结束")
                return

    def vedio_thread(self):
        self.thread_run = True
        while self.thread_run:
            _, self.img_bgr = self.camera.read()
            self.imgtk = self.get_imgtk(self.img_bgr)
            self.image_ctl.configure(image=self.imgtk)
        print("run end")

    def video_pic2(self):
        self.thread_run2 = True
        predict_time = time.time()
        while self.thread_run2:
            if self.cameraflag:
                if time.time() - predict_time > 2:
                    print("实时识别中self.cameraflag", self.cameraflag)
                    cv2.imwrite("tmp/test.jpg", self.img_bgr)
                    self.pic_path = "tmp/test.jpg"
                    self.pic(self.pic_path)
                    predict_time = time.time()
        print("run end")

    def video_pic(self):
        if not self.thread_run:
            tkinter.messagebox.showinfo('提示', '请点击    [打开摄像头]    按钮！')
            return
        self.thread_run = False
        self.thread_run2 = False
        _, img_bgr = self.camera.read()
        cv2.imwrite("tmp/test.jpg", img_bgr)
        self.pic_path = "tmp/test.jpg"
        self.clean()
        self.pic(self.pic_path)
        print("video_pic")

    def url_pic(self):
        IMAGE_URL = self.getuser()
        URL_len = len(IMAGE_URL)
        if (IMAGE_URL == ""):
            tkinter.messagebox.showinfo('提示', '请输入网址！')
            return
        if (URL_len > 150):
            tkinter.messagebox.showinfo('提示', '网址过长！')
            return
        r = requests.get(IMAGE_URL)
        with open("tmp/url.png", 'wb') as f:
            f.write(r.content)
        # print(IMAGE_URL)
        self.thread_run = False
        self.thread_run2 = False
        self.cameraflag=0
        self.pic_path = "tmp/url.png"
        self.clean()
        self.pic_source = "网络地址：" + IMAGE_URL
        self.pic(self.pic_path)

    def url_pic2(self, self2):
        self.url_pic()

    def getuser(self):
        user = self.user_text.get()
        return user

    def api_ctl(self):
        if self.thread_run:
            return
        self.thread_run = False
        self.thread_run2 = False
        colorstr, textstr = api_pic(self.pic_path)
        self.apistr = colorstr + textstr
        self.show_roi1(textstr, None, colorstr)
        self.show_roi2(textstr, None, colorstr)
        localtime = time.asctime(time.localtime(time.time()))
        value = [localtime, None, None, None, None, self.apistr, self.pic_source]
        print(localtime, "|", "|", "| ", self.apistr, "|", self.pic_source)
        img_excel.excel_add(value)
        img_sql.sql(value[0], value[1], value[2], value[3], value[4], value[5], value[6])

    def api_ctl2(self, pic_path66):
        if self.thread_run:
            return
        self.thread_run = False
        self.thread_run2 = False
        colorstr, textstr = api_pic(pic_path66)
        self.apistr = colorstr + textstr
        self.show_roi1(textstr, None, colorstr)
        self.show_roi2(textstr, None, colorstr)
        localtime = time.asctime(time.localtime(time.time()))
        value = [localtime, None, None, None, None, self.apistr, self.pic_source]
        print(localtime, "|", "|", "| ", self.apistr, "|", self.pic_source)
        img_excel.excel_add(value)
        img_sql.sql(value[0], value[1], value[2], value[3], value[4], value[5], value[6])

    def show_img_pre(self):
        if self.thread_run:
            return
        self.thread_run = False
        self.thread_run2 = False
        filename = img_math.img_read("tmp/img_contours.jpg")
        screenwidth = win.winfo_screenwidth()
        screenheight = win.winfo_screenheight()
        win.update()
        width = win.winfo_width()
        height = win.winfo_height()
        laji1 = int((screenwidth - width)/2)
        laji2 = int((screenheight - height)/2)
        cv2.imshow("preimg", filename)
        cv2.moveWindow("preimg", laji1+100, laji2)

    def clean(self):
        if self.thread_run:
            self.cameraflag=0
            return
        self.thread_run = False
        self.thread_run2 = False
        self.p1.set("")
        img_bgr3 = img_math.img_read("pic/hy.png")
        self.imgtk2 = self.get_imgtk(img_bgr3)
        self.image_ctl.configure(image=self.imgtk2)

        self.r_ctl.configure(text="")
        self.color_ctl.configure(text="", state='enable')

        self.r_ct2.configure(text="")
        self.color_ct2.configure(text="", state='enable')

        self.pilImage3 = Image.open("pic/locate.png")
        w, h = self.pilImage3.size
        pil_image_resized = self.resize(w, h, self.pilImage3)
        self.tkImage3 = ImageTk.PhotoImage(image=pil_image_resized)
        self.roi_ctl.configure(image=self.tkImage3, state='enable')
        self.roi_ct2.configure(image=self.tkImage3, state='enable')


def close_window():
    print("destroy")
    if surface.thread_run:
        surface.thread_run = False
        surface.thread.join(2.0)
    win.destroy()


if __name__ == '__main__':
    win = tk.Tk()

    surface = Surface(win)
    # close,退出输出destroy
    win.protocol('WM_DELETE_WINDOW', close_window)
    # 进入消息循环
    win.mainloop()
