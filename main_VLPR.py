# -*- coding: utf-8 -*-
__author__ = '樱花落舞'
import tkinter as tk
from tkinter.filedialog import *
from tkinter import ttk
import img_function as predict
import cv2
from PIL import Image, ImageTk
import threading
import time
import img_math
import traceback
import debug
import config
from threading import Thread

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return1 = None
        self._return2 = None
        self._return3 = None
    def run(self):
        if self._target is not None:
            self._return1,self._return2,self._return3 = self._target(*self._args, **self._kwargs)
    def join(self):
        Thread.join(self)
        return self._return1,self._return2,self._return3





class Surface(ttk.Frame):
    pic_path = ""
    viewhigh = 600
    viewwide = 600
    update_time = 0
    thread = None
    thread_run = False
    camera = None
    color_transform = {"green": ("绿牌", "#55FF55"), "yello": ("黄牌", "#FFFF00"), "blue": ("蓝牌", "#6666FF")}

    def __init__(self, win):
        ttk.Frame.__init__(self, win)
        frame_left = ttk.Frame(self)
        frame_right1 = ttk.Frame(self)
        frame_right2 = ttk.Frame(self)
        win.title("车牌识别")
        win.state("zoomed")
        self.pack(fill=tk.BOTH, expand=tk.YES, padx="10", pady="10")
        frame_left.pack(side=LEFT, expand=1, fill=BOTH)
        frame_right1.pack(side=TOP, expand=1, fill=tk.Y)
        frame_right2.pack(side=RIGHT, expand=0)
        ttk.Label(frame_left, text='原图：').pack(anchor="nw")
        ttk.Label(frame_right1, text='形状定位车牌位置：').grid(column=0, row=0, sticky=tk.W)

        from_pic_ctl = ttk.Button(frame_right2, text="来自图片", width=20, command=self.from_pic)
        from_vedio_ctl = ttk.Button(frame_right2, text="来自摄像头", width=20, command=self.from_vedio)
        from_img_pre = ttk.Button(frame_right2, text="查看形状预处理图像", width=20,command = self.show_img_pre)
        self.image_ctl = ttk.Label(frame_left)
        self.image_ctl.pack(anchor="nw")

        self.roi_ctl = ttk.Label(frame_right1)
        self.roi_ctl.grid(column=0, row=1, sticky=tk.W)
        ttk.Label(frame_right1, text='形状定位识别结果：').grid(column=0, row=2, sticky=tk.W)
        self.r_ctl = ttk.Label(frame_right1, text="",font=('Times','20'))
        self.r_ctl.grid(column=0, row=3, sticky=tk.W)
        self.color_ctl = ttk.Label(frame_right1, text="", width="20")
        self.color_ctl.grid(column=0, row=4, sticky=tk.W)
        from_vedio_ctl.pack(anchor="se", pady="5")
        from_pic_ctl.pack(anchor="se", pady="5")
        from_img_pre.pack(anchor="se", pady="5")

        ttk.Label(frame_right1, text='颜色定位车牌位置：').grid(column=0, row=5, sticky=tk.W)
        self.roi_ct2 = ttk.Label(frame_right1)
        self.roi_ct2.grid(column=0, row=6, sticky=tk.W)
        ttk.Label(frame_right1, text='颜色定位识别结果：').grid(column=0, row=7, sticky=tk.W)
        self.r_ct2 = ttk.Label(frame_right1, text="",font=('Times','20'))
        self.r_ct2.grid(column=0, row=8, sticky=tk.W)
        self.color_ct2 = ttk.Label(frame_right1, text="", width="20")
        self.color_ct2.grid(column=0, row=9, sticky=tk.W)

        self.predictor = predict.CardPredictor()
        self.predictor.train_svm()

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
            self.imgtk_roi = ImageTk.PhotoImage(image=roi)
            self.roi_ctl.configure(image=self.imgtk_roi, state='enable')
            self.r_ctl.configure(text=str(r))
            self.update_time = time.time()
            try:
                c = self.color_transform[color]
                self.color_ctl.configure(text=c[0], background=c[1], state='enable')
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
            self.imgtk_roi = ImageTk.PhotoImage(image=roi)
            self.roi_ct2.configure(image=self.imgtk_roi, state='enable')
            self.r_ct2.configure(text=str(r))
            self.update_time = time.time()
            try:
                c = self.color_transform[color]
                self.color_ct2.configure(text=c[0], background=c[1], state='enable')
            except:
                self.color_ct2.configure(state='disabled')
        elif self.update_time + 8 < time.time():

            self.roi_ct2.configure(state='disabled')
            self.r_ct2.configure(text="")
            self.color_ct2.configure(state='disabled')

    def show_img_pre(self):

        filename = config.get_name()
        if filename.any() == True:
            debug.img_show(filename)


    def from_vedio(self):
        if self.thread_run:
            return
        if self.camera is None:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                mBox.showwarning('警告', '摄像头打开失败！')
                self.camera = None
                return
        self.thread = threading.Thread(target=self.vedio_thread, args=(self,))
        self.thread.setDaemon(True)
        self.thread.start()
        self.thread_run = True

    def from_pic(self):
        self.thread_run = False
        self.pic_path = askopenfilename(title="选择识别图片", filetypes=[("jpg图片", "*.jpg"), ("png图片", "*.png")])
        if self.pic_path:
            img_bgr = img_math.img_read(self.pic_path)
            first_img, oldimg = self.predictor.img_first_pre(img_bgr)
            self.imgtk = self.get_imgtk(img_bgr)
            self.image_ctl.configure(image=self.imgtk)
            th1 = ThreadWithReturnValue(target=self.predictor.img_color_contours,args=(first_img,oldimg))
            th2 = ThreadWithReturnValue(target=self.predictor.img_only_color,args=(oldimg,oldimg,first_img))
            th1.start()
            th2.start()
            r_c, roi_c, color_c = th1.join()
            r_color,roi_color,color_color = th2.join()
            print(r_c,r_color)

            self.show_roi2(r_color, roi_color, color_color)

            self.show_roi1(r_c, roi_c, color_c)


    @staticmethod
    def vedio_thread(self):
        self.thread_run = True
        predict_time = time.time()
        while self.thread_run:
            _, img_bgr = self.camera.read()
            self.imgtk = self.get_imgtk(img_bgr)
            self.image_ctl.configure(image=self.imgtk)
            if time.time() - predict_time > 2:
                r, roi, color = self.predictor(img_bgr)
                self.show_roi(r, roi, color)
                predict_time = time.time()
        print("run end")


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