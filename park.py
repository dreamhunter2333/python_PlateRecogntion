#!/usr/bin/python3
# -*- coding: utf-8 -*-
import cv2
import tkinter as tk
import tkinter.messagebox

from datetime import timedelta, timezone, datetime
from PIL import Image, ImageTk
from hyperlpr import HyperLPR_PlateRecogntion
from tkinter import LEFT, RIGHT, ttk
from tkinter.filedialog import askopenfilename


from lib import img_math
import lib.img_function as predict
from models.park_models import ParkHistory


PARK_SIZE = 100
TZ = timezone(timedelta(hours=8))


class Park(ttk.Frame):
    def __init__(self, win):
        ttk.Frame.__init__(self, win)

        frame_left = ttk.Frame(self)
        frame_right = ttk.Frame(self)

        win.title("停车场系统")
        win.minsize(850, 700)

        self.center_window()
        self.pic_path = ""

        self.pack(fill=tk.BOTH, expand=tk.YES, padx="10", pady="10")
        frame_left.pack(side=LEFT, expand=1)
        frame_right.pack(side=RIGHT, expand=0)

        self.image_ctl = ttk.Label(frame_left)
        self.image_ctl.pack(anchor="nw")

        from_pic_ctl = ttk.Button(
            frame_right, text="选择图片", width=20,
            command=self.from_pic
        )
        car_in_btn = ttk.Button(
            frame_right, text="进入停车场", width=20,
            command=self.car_in
        )
        pay_btn = ttk.Button(
            frame_right, text="缴费", width=20,
            command=self.pay
        )
        car_out_btn = ttk.Button(
            frame_right, text="退出停车场", width=20,
            command=self.car_out
        )
        clean_ctrl = ttk.Button(
            frame_right, text="清除识别数据", width=20,
            command=self.clean
        )

        from_pic_ctl.pack(anchor="se", pady="5")
        clean_ctrl.pack(anchor="se", pady="5")
        car_in_btn.pack(anchor="se", pady="5")
        pay_btn.pack(anchor="se", pady="5")
        car_out_btn.pack(anchor="se", pady="5")

        self.clean()
        self.predictor = predict.CardPredictor()
        self.predictor.train_svm()

    def reset(self):
        win.geometry("850x700")
        self.clean()
        self.count = 0
        self.center_window()

    def center_window(self):
        screenwidth = win.winfo_screenwidth()
        screenheight = win.winfo_screenheight()
        win.update()
        width = win.winfo_width()
        height = win.winfo_height()
        size = '+%d+%d' % ((screenwidth - width)/2, (screenheight - height)/2)
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

    def from_pic(self):
        self.pic_path = askopenfilename(
            title="选择识别图片",
            filetypes=[
                ("jpg 图片", "*.jpg"), ("jpeg 图片", "*.jpeg"), ("png 图片", "*.png")
            ]
        )
        self.clean()
        img_bgr = img_math.img_read(self.pic_path)
        self.imgtk = self.get_imgtk(img_bgr)
        self.image_ctl.configure(image=self.imgtk)

    def recogntion(self):
        if not self.pic_path:
            tkinter.messagebox.showinfo(title='停车场系统', message='请选择图片')
            raise Exception("请选择图片")

        img_bgr = cv2.imread(self.pic_path)
        first_img, oldimg = self.predictor.img_first_pre(img_bgr)

        try:
            r_c, _, _ = self.predictor.img_color_contours(first_img, oldimg)
            r_color, _, _ = self.predictor.img_only_color(
                oldimg, oldimg, first_img)
        except Exception as e:
            print(e)
            pass
        if r_c:
            return r_c
        if r_color:
            return r_color

        try:
            Plate = HyperLPR_PlateRecogntion(img_bgr)
            res = Plate[0][0]
        except Exception as e:
            print(e)
            pass
        if res:
            return res

    def car_in(self):
        plate = self.recogntion()
        if not plate:
            tkinter.messagebox.showinfo(title='停车场系统', message='识别失败')
            return
        count = ParkHistory.count_car()
        if count >= PARK_SIZE:
            tkinter.messagebox.showinfo(
                title='停车场系统',
                message='{} 车位已满'.format(plate)
            )
            return
        res = ParkHistory.add_car(plate)
        if not res:
            tkinter.messagebox.showinfo(
                title='停车场系统',
                message='{} 重复进入'.format(plate)
            )
            return
        tkinter.messagebox.showinfo(
            title='停车场系统',
            message='{} 请进, 剩余车位: {}'.format(plate, PARK_SIZE - count)
        )

    def pay(self):
        plate = self.recogntion()
        if not plate:
            tkinter.messagebox.showinfo(title='停车场系统', message='识别失败')
            return
        history_time = ParkHistory.calc_car(plate)
        if not history_time:
            tkinter.messagebox.showinfo(
                title='停车场系统', message='{} 未进入'.format(plate)
            )
            return
        delta = datetime.now(tz=TZ) - history_time
        tkinter.messagebox.showinfo(
            title='请缴费',
            message='{}: 上次进入: {}, \n 停车时长: {} 天 {} 小时 {} 分钟'.format(
                plate, history_time, delta.days,
                (delta.seconds // 3600),
                ((delta.seconds % 3600) // 60)
            )
        )

    def car_out(self):
        plate = self.recogntion()
        if not plate:
            tkinter.messagebox.showinfo(title='停车场系统', message='识别失败')
            return
        ParkHistory.del_car(plate)
        tkinter.messagebox.showinfo(
            title='停车场系统',
            message='{}: 一路顺风'.format(plate)
        )
        return

    def clean(self):
        self.welcome_img = self.get_imgtk(img_math.img_read("pic/hy.png"))
        self.image_ctl.configure(image=self.welcome_img)


def close_window():
    print("win destroy")
    win.destroy()


win = tk.Tk()
park = Park(win)
win.protocol('WM_DELETE_WINDOW', close_window)
win.mainloop()