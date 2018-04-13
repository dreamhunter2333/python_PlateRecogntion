# -*- coding: utf-8 -*-
__author__ = '樱花落舞'
import cv2
import numpy as np
import img_math

MAX_WIDTH = 1000
Min_Area = 2000







class img_main:
    def __init__(self):
        pass


    def img_first_pre(self,car_pic_file):
        if type(car_pic_file) == type(""):
            img = img_math.img_read(car_pic_file)
        else:
            img = car_pic_file

        pic_hight,pic_width = img.shape[:2]

        if pic_width > MAX_WIDTH:
            resize_rate = MAX_WIDTH / pic_width
            img = cv2.resize(img, (MAX_WIDTH, int(pic_hight * resize_rate)), interpolation=cv2.INTER_AREA)
        #缩小图片

        blur = 3
        img = cv2.GaussianBlur(img,(blur,blur),0)
        oldimg = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #转化成灰度图像

        kernel = np.ones((20, 20), np.uint8)
        #创建20*20的元素为1的矩阵

        img_opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        img_opening = cv2.addWeighted(img, 1, img_opening, -1, 0)
        #开操作，并和img重合

        ret, img_thresh = cv2.threshold(img_opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img_edge = cv2.Canny(img_thresh, 100, 200)

        #找到图像边缘

        kernel = np.ones((4, 19), np.uint8)
        img_edge1 = cv2.morphologyEx(img_edge, cv2.MORPH_CLOSE, kernel)
        img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, kernel)
        return img_edge2,oldimg

    def img_color_Contours(self,img_contours,oldimg):
        pic_hight,pic_width = img_contours.shape[:2]
        card_contours = img_math.img_findContours(img_contours,oldimg)
        card_imgs = img_math.img_Transform(card_contours,oldimg,pic_width,pic_hight)
        colors = img_math.img_color(card_imgs)



    def img_only_color(self,filename,oldimg):
        lower_blue = np.array([100, 110, 110])
        upper_blue = np.array([130, 255, 255])


        hsv = cv2.cvtColor(filename, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        output = cv2.bitwise_and(hsv, hsv, mask=mask)
        # 根据阈值找到对应颜色
        output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

        card_contours = img_math.img_findContours(output,oldimg)

