# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
import tkinter.messagebox
from PIL import Image, ImageTk
import img_api2
import cv2
import threading
import time

class Login(ttk.Frame):
    def __init__(self, win):
        ttk.Frame.__init__(self, win)
        frame0 = ttk.Frame(self)
        frame1 = ttk.Frame(self)
        win.title("人脸识别")
        win.minsize(800, 550)
        self.center_window()
        self.thread_run = None
        self.thread_run2 = None
        self.camera = None

        self.pilImage = Image.open("img/start.png")
        self.tkImage = ImageTk.PhotoImage(image=self.pilImage)
        self.image_ctl = tk.Label(frame0, image=self.tkImage)
        self.image_ctl.pack()

        frame0.pack(side=TOP, fill=tk.Y, expand=1)
        frame1.pack(side=TOP, fill=tk.Y, expand=1)

        self.facer = ttk.Label(frame1, text='', font=('Times', '20'))
        self.facer.pack()

        self.face_button1 = ttk.Button(frame1, text="选择文件", width=15, command=self.file1)
        self.face_button1.pack(side=TOP)
        self.url_face_button = ttk.Button(frame1, text="使用相机识别", width=15, command=self.cv_face)
        self.url_face_button.pack(side=TOP)
        self.file_pic_button = ttk.Button(frame1, text="本地文件识别", width=15, command=self.file_pic)
        self.file_pic_button.pack(side=TOP)

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

    def cv_face(self):
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
        self.thread = threading.Thread(target=self.video_thread)
        self.thread.setDaemon(True)
        self.thread.start()
        self.thread_run = True

    def video_thread(self):
        self.thread_run = True
        self.thread2 = threading.Thread(target=self.video_pic)
        self.thread2.setDaemon(True)
        self.thread2.start()
        self.thread_run2 = True
        while self.thread_run:
            _, img_bgr = self.camera.read()
            img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(img)
            w, h = im.size
            pil_image_resized = self.resize(w, h, im)
            self.imgtk = ImageTk.PhotoImage(image=pil_image_resized)
            self.image_ctl.configure(image=self.imgtk)
        print("run end")

    def video_pic(self):
        self.thread_run2 = True
        predict_time = time.time()
        while self.thread_run2:
            if time.time() - predict_time > 2:
                print("实时识别中")
                _, img_bgr = self.camera.read()
                cv2.imwrite("tmp/test2.jpg", img_bgr)
                self.pic_path = "tmp/test2.jpg"
                try:
                    self.file_pic()
                except:
                    pass
                predict_time = time.time()
                print("video_pic")
        pass

    def file_pic(self):
        self.pic_path2 = "img/lock.jpg"
        facestr, result = img_api2.facef(self.pic_path, self.pic_path2)
        self.facer.configure(text=str(facestr))
        self.pic()
        if result > 80:
            self.thread_run = False
            self.thread_run2 = False
            tkinter.messagebox.showinfo('提示', '登录成功！')
            close_window()
            os.system("python3 ./main.py")
        else:
            tkinter.messagebox.showinfo('提示', '登录失败，请重试！')

    def pic(self):
        self.pilImage3 = Image.open(self.pic_path)
        w, h = self.pilImage3.size
        pil_image_resized = self.resize(w, h, self.pilImage3)
        self.tkImage3 = ImageTk.PhotoImage(image=pil_image_resized)
        self.image_ctl.configure(image=self.tkImage3)

    def resize(self, w, h, pil_image):
        w_box = 800
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
