#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'jinmu333'

import tkinter
import tkinter.filedialog
from PIL import ImageGrab
from time import sleep


class MyCapture:
    def __init__(self, root, png):
        # 变量X和Y用来记录鼠标左键按下的位置
        self.X = tkinter.IntVar(value=0)
        self.Y = tkinter.IntVar(value=0)
        self.sel = False
        # 屏幕尺寸
        self.screenWidth = root.winfo_screenwidth()
        self.screenHeight = root.winfo_screenheight()
        # 创建顶级组件容器
        self.top = tkinter.Toplevel(root, width=self.screenWidth, height=self.screenHeight)
        #self.top.update()
        #self.top.resizable(0, 0)
        self.top.geometry('+0+0')
        # 不显示最大化、最小化按钮
        self.top.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.top, bg='white', width=self.screenWidth, height=self.screenHeight)
        # 显示全屏截图，在全屏截图上进行区域截图
        self.image = tkinter.PhotoImage(file=png)
        self.canvas.create_image(self.screenWidth//2, self.screenHeight//2, image=self.image)
        self.canvas.pack()
 
        # 鼠标左键按下的位置
        def onLeftButtonDown(event):
            # pdb.set_trace()
            self.X.set(event.x)
            self.Y.set(event.y)
            # 开始截图
            self.sel = True
        self.canvas.bind('<Button-1>', onLeftButtonDown)
 
        # 鼠标左键移动，显示选取的区域
        def onLeftButtonMove(event):
            # pdb.set_trace()
            global lastDraw, r, c
            try:
                # 删除刚画完的图形，要不然鼠标移动的时候是黑乎乎的一片矩形
                self.canvas.delete(lastDraw)
                self.canvas.delete(r)
                self.canvas.delete(c)
            except Exception as e:
                pass
            if not self.sel:
                # 没有点击左键时绘制十字线
                r = self.canvas.create_line(0, event.y, self.screenWidth, event.y, fill='white')
                c = self.canvas.create_line(event.x, 0, self.screenHeight, event.x, fill='white')
                #print(event.x, event.y, self.screenWidth, self.screenHeight)
            else:
                lastDraw = self.canvas.create_rectangle(self.X.get(), self.Y.get(), event.x, event.y, outline='orange')
                #print(event.x, event.y, self.screenWidth, self.screenWidth)
        self.canvas.bind('<B1-Motion>', onLeftButtonMove)
        # 获取鼠标左键抬起的位置，保存区域截图

        def onLeftButtonUp(event):
            self.sel =False
            try:
                self.canvas.delete(lastDraw)
            except Exception as e:
                pass
            sleep(0.1)
            # 考虑鼠标左键从右下方按下而从左上方抬起的截图
            left, right = sorted([self.X.get(), event.x])
            top, bottom = sorted([self.Y.get(), event.y])
            pic =ImageGrab.grab((left+1, top+1, right, bottom))
            # 关闭顶级容器
            self.top.destroy()
            if pic:
                pic.save('tmp/cut.png')
        self.canvas.bind('<ButtonRelease-1>', onLeftButtonUp)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)


