#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import tkinter as tk

from PIL import Image, ImageTk
from tkinter import LEFT, RIGHT, ttk
from tkinter.filedialog import askopenfilename

import lib.img_function as predict
import lib.img_math as img_math


COLORS = {
    "green": (0, 255, 0),
    "yello": (255, 255, 0),
    "blue": (0, 0, 255)
}


class Replace(ttk.Frame):
    pic_path = ""

    def __init__(self, win):
        ttk.Frame.__init__(self, win)

        frame_left = ttk.Frame(self)
        frame_right = ttk.Frame(self)

        win.title("车牌识别")
        win.minsize(850, 700)

        self.center_window()

        self.pack(fill=tk.BOTH, expand=tk.YES, padx="10", pady="10")
        frame_left.pack(side=LEFT, expand=1)
        frame_right.pack(side=RIGHT, expand=0)

        self.image_ctl = ttk.Label(frame_left)
        self.image_ctl.pack(anchor="nw")

        from_pic_ctl = ttk.Button(
            frame_right, text="选择图片", width=20,
            command=self.from_pic
        )
        clean_ctrl = ttk.Button(
            frame_right, text="清除识别数据", width=20,
            command=self.clean
        )

        from_pic_ctl.pack(anchor="se", pady="5")
        clean_ctrl.pack(anchor="se", pady="5")

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
                ("jpeg 图片", "*.jpeg"), ("jpg 图片", "*.jpg"), ("png 图片", "*.png")
            ]
        )
        self.clean()
        img_bgr = img_math.img_read(self.pic_path)
        first_img, oldimg = self.predictor.img_first_pre(img_bgr)

        r_c, roi_c, color_c, car_img_box = self.predictor.img_color_contours(
            first_img, oldimg, add_contours=True
        )

        x0 = int(min(p[0] for p in car_img_box))
        x1 = int(max(p[0] for p in car_img_box))
        y0 = int(min(p[1] for p in car_img_box))
        y1 = int(max(p[1] for p in car_img_box))

        cover_img = cv2.imread('pic/cover.png')
        cover = cv2.resize(
            cover_img, (x1 - x0 + 10, y1 - y0 + 10),
            interpolation=cv2.INTER_AREA
        )
        oldimg[y0:y0 + cover.shape[0], x0:x0 + cover.shape[1]] = cover

        coverd_img = cv2.cvtColor(oldimg, cv2.COLOR_BGR2RGB)
        coverd_img = Image.fromarray(coverd_img)
        self.coverd_img = ImageTk.PhotoImage(image=coverd_img)
        self.image_ctl.configure(image=self.coverd_img)

    def clean(self):
        self.welcome_img = self.get_imgtk(img_math.img_read("pic/hy.png"))
        self.image_ctl.configure(image=self.welcome_img)


def close_window():
    print("destroy")
    win.destroy()


if __name__ == '__main__':
    win = tk.Tk()

    replace = Replace(win)
    # close,退出输出destroy
    win.protocol('WM_DELETE_WINDOW', close_window)
    # 进入消息循环
    win.mainloop()
