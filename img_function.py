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

    def img_color_findContours(self,img_contours,oldimg):
        pic_hight,pic_width = img_contours.shape[:2]
        #print(pic_hight,pic_width)
        img,contours,hierarchy = cv2.findContours(img_contours, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = [cnt for cnt in contours if cv2.contourArea(cnt)>Min_Area]
        print("findContours len = ",len(contours))
        #排除面积最小的点

        car_contours = []
        for cnt in contours:
            ant = cv2.minAreaRect(cnt)
            width,height = ant[1]

            if width < height:
                width,height = height,width

            ration = width/height
            print(ration)
            if ration > 2 and ration < 5.5:
                car_contours.append(ant)
                box = cv2.boxPoints(ant)
                box = np.int0(box)

        card_imgs=img_math.img_Transform(car_contours,oldimg,pic_width,pic_hight)
        colors = img_math.img_color(card_imgs)



    def img_only_color(self,filename):
        lower_blue = np.array([100, 110, 110])
        upper_blue = np.array([130, 255, 255])

        # 根据阈值找到对应颜色
        hsv = cv2.cvtColor(filename, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        output = cv2.bitwise_and(filename, filename, mask=mask)

        # 展示图片
        cv2.imshow("images", output)
        cv2.waitKey(0)

