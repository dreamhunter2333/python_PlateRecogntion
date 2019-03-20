# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
import tkinter.messagebox
from PIL import Image, ImageTk
import requests
from hyperlpr import *
import cv2


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
        self.label2 = ttk.Label(frame2, text='图片2(右): ')
        self.label2.pack(side=LEFT)
        self.input2 = ttk.Entry(frame2, textvariable=self.s2, width=30)
        self.input2.pack(side=LEFT)
        self.face_button2 = ttk.Button(frame2, text="选择文件", width=15, command=self.file2)
        self.face_button2.pack(side=RIGHT)
        self.url_face_button = ttk.Button(frame3, text="网络地址识别", width=15, command=self.url_p)
        self.url_face_button.pack(side=LEFT)
        self.file_pic_button = ttk.Button(frame3, text="本地文件识别", width=15, command=self.file_pic)
        self.file_pic_button.pack(side=RIGHT)

        self.match = ttk.Label(frame4, text='', font=('Times', '20'))
        self.match.pack()

        self.pack(fill=tk.BOTH, expand=tk.YES, padx="10", pady="10")

    def center_window(self):
        screenwidth = log.winfo_screenwidth()
        screenheight = log.winfo_screenheight()
        log.update()
        width = log.winfo_width()
        height = log.winfo_height()
        size = '+%d+%d' % ((screenwidth - width)/2, (screenheight - height)/2)
        log.geometry(size)

    def file1(self):
        self.pic_path = askopenfilename(title="选择识别图片", filetypes=[("jpg图片", "*.jpg"), ("png图片", "*.png")])
        self.s1.set(self.pic_path)

    def file2(self):
        self.pic_path2 = askopenfilename(title="选择识别图片", filetypes=[("jpg图片", "*.jpg"), ("png图片", "*.png")])
        self.s2.set(self.pic_path2)

    def url_p(self):
        url1 = self.input1.get()
        url2 = self.input2.get()
        self.url_dpic1(url1)
        self.url_dpic2(url2)
        self.match_pic()

    def file_pic(self):
        self.match_pic()

    def match_pic(self):
        image1 = cv2.imread(self.pic_path)
        image2 = cv2.imread(self.pic_path2)
        Plate1 = HyperLPR_PlateRecogntion(image1)
        # print(Plate1[0][0])
        matchstr1 = Plate1[0][0]
        Plate2 = HyperLPR_PlateRecogntion(image2)
        # print(Plate2[0][0])
        matchstr2 = Plate2[0][0]
        if matchstr1==matchstr2:
            matchstr3 = "        车牌相符        "
        else:
            matchstr3 = "        车牌不符        "
        matchstr = matchstr1 + matchstr3 + matchstr2

        self.match.configure(text=str(matchstr))
        self.pilImage3 = Image.open(self.pic_path)
        w, h = self.pilImage3.size
        pil_image_resized = self.resize(w, h, self.pilImage3)
        self.tkImage3 = ImageTk.PhotoImage(image=pil_image_resized)
        self.image_ctl.configure(image=self.tkImage3)
        self.pilImage4 = Image.open(self.pic_path2)
        w, h = self.pilImage4.size
        pil_image_resized2 = self.resize(w, h, self.pilImage4)
        self.tkImage4 = ImageTk.PhotoImage(image=pil_image_resized2)
        self.image_ctl2.configure(image=self.tkImage4)
        self.s1.set("")
        self.s2.set("")

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
