# -*- coding: utf-8 -*-

import threading
import time
import tkinter as tk
import cv2
import img_function as predict
import img_math
import img_excel
import img_sql
import img_api
import screencut
from threading import Thread
from tkinter import ttk
from tkinter.filedialog import *
from PIL import Image, ImageTk, ImageGrab
import tkinter.messagebox
import requests
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
        win.minsize(850, 550)
        # win.wm_attributes('-topmost', 1)
        self.center_window()

        top.pack(side=TOP, expand=1, fill=tk.Y)
        L1 = Label(top, text='网络地址:')
        L1.pack(side = LEFT)
        self.p1 = StringVar()
        self.user_text = ttk.Entry(top, textvariable=self.p1, width=50)
        self.user_text.pack(side = LEFT)
        self.user_text.bind('<Key-Return>', self.url_pic2)
        url_ctl = ttk.Button(top, text="识别网络图片", width=20, command=self.url_pic)
        url_ctl.pack(side = RIGHT)

        self.pack(fill=tk.BOTH, expand=tk.YES, padx="10", pady="10")
        frame_left.pack(side=LEFT, expand=1)
        frame_right1.pack(side=TOP, expand=1, fill=tk.Y)
        frame_right2.pack(side=RIGHT, expand=0)
        #ttk.Label(frame_left, text='地址：').pack(anchor="nw")

        self.image_ctl = ttk.Label(frame_left)
        self.image_ctl.pack(anchor="nw")

        ttk.Label(frame_right1, text='形状定位车牌位置：').grid(column=0, row=0, sticky=tk.W)
        from_pic_ctl = ttk.Button(frame_right2, text="来自图片", width=20, command=self.from_pic)
        from_vedio_ctl = ttk.Button(frame_right2, text="打开/关闭摄像头", width=20, command=self.from_vedio)
        from_video_ctl = ttk.Button(frame_right2, text="拍照并识别", width=20, command=self.video_pic)
        from_img_pre = ttk.Button(frame_right2, text="查看预处理图像", width=20, command=self.show_img_pre)
        clean_ctrl = ttk.Button(frame_right2, text="清除识别数据", width=20, command=self.clean)
        exit_ctrl = ttk.Button(frame_right2, text="退出", width=20, command=close_window)
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
        imgtk = ImageTk.PhotoImage(image=im)
        wide = imgtk.width()
        high = imgtk.height()
        if wide > self.viewwide or high > self.viewhigh:
            wide_factor = self.viewwide / wide
            high_factor = self.viewhigh / high
            factor = min(wide_factor, high_factor)
            wide = int(wide * factor)
            if wide <= 0: wide = 1
            high = int(high * factor)
            if high <= 0: high = 1
            im = im.resize((wide, high), Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(image=im)
        return imgtk

    def show_roi1(self, r, roi, color):
        if r:
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            roi = Image.fromarray(roi)
            self.imgtk_roi1 = ImageTk.PhotoImage(image=roi)
            self.roi_ctl.configure(image=self.imgtk_roi1, state='enable')
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
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
            roi = Image.fromarray(roi)
            self.imgtk_roi2 = ImageTk.PhotoImage(image=roi)
            self.roi_ct2.configure(image=self.imgtk_roi2, state='enable')
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
        else:
            self.cameraflag = 0
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
        self.cameraflag=0
        self.thread = threading.Thread(target=self.vedio_thread, args=(self,))
        self.thread.setDaemon(True)
        self.thread.start()
        self.thread_run = True

    def pic(self, pic_path):
        img_bgr = img_math.img_read(pic_path)
        first_img, oldimg = self.predictor.img_first_pre(img_bgr)
        self.imgtk = self.get_imgtk(img_bgr)
        self.image_ctl.configure(image=self.imgtk)
        th1 = ThreadWithReturnValue(target=self.predictor.img_color_contours, args=(first_img, oldimg))
        th2 = ThreadWithReturnValue(target=self.predictor.img_only_color, args=(oldimg, oldimg, first_img))
        th1.start()
        th2.start()
        r_c, roi_c, color_c = th1.join()
        r_color, roi_color, color_color = th2.join()

        localtime = time.asctime( time.localtime(time.time()))
        value = [localtime, color_c, r_c, color_color, r_color, self.pic_source]
        if not self.cameraflag:
            img_excel.excel_add(value)
            img_sql.sql(value[0], value[1], value[2], value[3], value[4], value[5])

        print(localtime, "|", color_c, r_c, "|", color_color, r_color, "|", self.pic_source)
        self.show_roi2(r_color, roi_color, color_color)
        self.show_roi1(r_c, roi_c, color_c)
        #img_api.api_pic(pic_path)
        self.center_window()

    def from_pic(self):
        self.thread_run = False
        self.cameraflag = 0
        self.pic_path = askopenfilename(title="选择识别图片", filetypes=[("jpg图片", "*.jpg"), ("png图片", "*.png")])
        self.clean()
        self.pic_source = "本地文件：" + self.pic_path
        self.pic(self.pic_path)

    def vedio_thread(delf,self):
        self.thread_run = True
        predict_time = time.time()
        while self.thread_run:
            _, img_bgr = self.camera.read()
            self.imgtk = self.get_imgtk(img_bgr)
            self.image_ctl.configure(image=self.imgtk)
            if self.cameraflag :
                if time.time() - predict_time > 2:
                    print("实时识别中self.cameraflag", self.cameraflag)
                    cv2.imwrite("tmp/test.jpg", img_bgr)
                    self.pic_path = "tmp/test.jpg"
                    self.pic(self.pic_path)
                    predict_time = time.time()
        print("run end")

    def video_pic(self):
        if not self.thread_run:
            tkinter.messagebox.showinfo('提示', '请点击    [打开摄像头]    按钮！')
            return
        self.thread_run = False
        _, img_bgr = self.camera.read()
        cv2.imwrite("tmp/test.jpg", img_bgr)
        self.pic_path = "tmp/test.jpg"
        self.clean()
        self.pic(self.pic_path)
        print("video_pic")

    def url_pic(self):
        IMAGE_URL = self.getuser()
        if (IMAGE_URL == ""):
            tkinter.messagebox.showinfo('提示', '请输入网址！')
            return
        r = requests.get(IMAGE_URL)
        with open("tmp/url.png", 'wb') as f:
            f.write(r.content)
        #print(IMAGE_URL)
        self.thread_run = False
        self.cameraflag=0
        self.pic_path = "tmp/url.png"
        self.clean()
        self.pic_source = "网络地址：" + IMAGE_URL
        self.pic(self.pic_path)

    def url_pic2(self, self2):
        self.url_pic()

    def getuser(self):
        user = self.user_text.get() #获取文本框内容
        return user

    def show_img_pre(self):
        if self.thread_run:
            return
        self.thread_run = False
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
        self.center_window()
        self.p1.set("")
        img_bgr3 = img_math.img_read("pic/hy.png")
        self.imgtk2 = self.get_imgtk(img_bgr3)
        self.image_ctl.configure(image=self.imgtk2)

        self.r_ctl.configure(text="")
        self.color_ctl.configure(text="", state='enable')

        self.r_ct2.configure(text="")
        self.color_ct2.configure(text="", state='enable')

        self.roi_ctl.configure(state='disabled')
        self.roi_ct2.configure(state='disabled')


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
