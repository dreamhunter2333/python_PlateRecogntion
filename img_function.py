# -*- coding: utf-8 -*-
__author__ = '樱花落舞'
import cv2
import numpy as np
import img_math
import debug
MAX_WIDTH = 1000
Min_Area = 2000







class img_main:
    def __init__(self):
        pass


    def img_first_pre(self,car_pic_file):
        """
        :param car_pic_file: 图像文件
        :return:已经处理好的图像文件 原图像文件
        """
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

        Matrix = np.ones((20, 20), np.uint8)
        img_opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, Matrix)
        img_opening = cv2.addWeighted(img, 1, img_opening, -1, 0)
        #创建20*20的元素为1的矩阵 开操作，并和img重合

        ret, img_thresh = cv2.threshold(img_opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img_edge = cv2.Canny(img_thresh, 100, 200)
        #Otsu’s二值化 找到图像边缘

        Matrix = np.ones((4, 19), np.uint8)
        img_edge1 = cv2.morphologyEx(img_edge, cv2.MORPH_CLOSE, Matrix)
        img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, Matrix)
        return img_edge2,oldimg

    def img_color_contours(self,img_contours,oldimg):
        """
        :param img_contours: 预处理好的图像
        :param oldimg: 原图像
        :return: 已经定位好的车牌
        """

        pic_hight,pic_width = img_contours.shape[:2]
        card_contours = img_math.img_findContours(img_contours,oldimg)
        card_imgs = img_math.img_Transform(card_contours,oldimg,pic_width,pic_hight)
        colors,car_imgs = img_math.img_color(card_imgs)



    def img_only_color(self,filename,oldimg,img_contours):
        """
        :param filename: 图像文件
        :param oldimg: 原图像文件
        :return: 已经定位好的车牌
        """
        pic_hight, pic_width = img_contours.shape[:2]
        lower_blue = np.array([100, 110, 110])
        upper_blue = np.array([130, 255, 255])
        lower_yellow = np.array([15, 55, 55])
        upper_yellow = np.array([50, 255, 255])
        hsv = cv2.cvtColor(filename, cv2.COLOR_BGR2HSV)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        output = cv2.bitwise_and(hsv, hsv, mask=mask_blue+mask_yellow)
        # 根据阈值找到对应颜色
        output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)

        Matrix = np.ones((20, 20), np.uint8)
        img_edge1 = cv2.morphologyEx(output, cv2.MORPH_CLOSE, Matrix)
        img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, Matrix)
        debug.img_show(img_edge2)
        card_contours = img_math.img_findContours(img_edge2,oldimg)
        card_imgs = img_math.img_Transform(card_contours, oldimg, pic_width, pic_hight)
        colors,car_imgs = img_math.img_color(card_imgs)

    def img_mser(self,filename):
        if type(filename) == type(""):
            img = img_math.img_read(filename)
        else:
            img = filename
        oldimg = img
        mser = cv2.MSER_create(_min_area=600)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        regions, boxes = mser.detectRegions(gray)
        colors_img = []
        for box in boxes:
            x, y, w, h = box
            width, height = w, h
            if width < height:
                width, height = height, width
            ration = width / height

            if w * h > 1500 and ration > 3 and ration < 4 and w > h:
                cropimg = img[y:y+h,x:x+w]
                colors_img.append(cropimg)

        debug.img_show(img)
        colors,car_imgs = img_math.img_color(colors_img)
        for i, color in enumerate(colors):
            if color !="no":
                print(color)
                debug.img_show(car_imgs[i])

