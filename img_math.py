# -*- coding: utf-8 -*-
__author__ = '樱花落舞'
import cv2
import numpy as np
MAX_WIDTH = 1000
Min_Area = 2000
"""
该文件包含读文件函数
取零值函数
矩阵校正函数
颜色判断函数
"""
def img_read(filename):
    return  cv2.imdecode(np.fromfile(filename, dtype=np.uint8), cv2.IMREAD_COLOR)
    #以uint8方式读取filename 放入imdecode中，cv2.IMREAD_COLOR读取彩色照片

def point_limit(point):
    if point[0] < 0:
        point[0] = 0
    if point[1] < 0:
        point[1] = 0

def img_findContours(img_contours,oldimg):
    img, contours, hierarchy = cv2.findContours(img_contours, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > Min_Area]
    print("findContours len = ", len(contours))
    # 排除面积最小的点

    car_contours = []
    for cnt in contours:
        ant = cv2.minAreaRect(cnt)
        width, height = ant[1]

        if width < height:
            width, height = height, width

        ration = width / height
        print(ration)
        if ration > 2 and ration < 5.5:
            car_contours.append(ant)
            box = cv2.boxPoints(ant)
            box = np.int0(box)
            # oldimg = cv2.drawContours(oldimg, [box], 0, (0, 0, 255), 2)
            # cv2.imshow("edge4", oldimg)
            # cv2.waitKey(0)
    return  car_contours

def img_Transform(car_contours,oldimg,pic_width,pic_hight):
    car_imgs = []

    for car_rect in car_contours:
        if car_rect[2] > -1 and car_rect[2] < 1:
            angle = 1
            # 对于角度为-1 1之间时，默认为1
        else:
            angle = car_rect[2]

        car_rect = (car_rect[0], (car_rect[1][0] + 5, car_rect[1][1] + 5), angle)
        box = cv2.boxPoints(car_rect)
        heigth_point = right_point = [0, 0]
        left_point = low_point = [pic_width, pic_hight]
        for point in box:
            if left_point[0] > point[0]:
                left_point = point
            if low_point[1] > point[1]:
                low_point = point
            if heigth_point[1] < point[1]:
                heigth_point = point
            if right_point[0] < point[0]:
                right_point = point

        if left_point[1] <= right_point[1]:  # 正角度
            new_right_point = [right_point[0], heigth_point[1]]
            pts2 = np.float32([left_point, heigth_point, new_right_point])  # 字符只是高度需要改变
            pts1 = np.float32([left_point, heigth_point, right_point])
            M = cv2.getAffineTransform(pts1, pts2)
            dst = cv2.warpAffine(oldimg, M, (pic_width, pic_hight))
            point_limit(new_right_point)
            point_limit(heigth_point)
            point_limit(left_point)
            car_img = dst[int(left_point[1]):int(heigth_point[1]), int(left_point[0]):int(new_right_point[0])]
            car_imgs.append(car_img)
            cv2.imshow("card", car_img)
            cv2.waitKey(0)
        elif left_point[1] > right_point[1]:  # 负角度
            new_left_point = [left_point[0], heigth_point[1]]
            pts2 = np.float32([new_left_point, heigth_point, right_point])  # 字符只是高度需要改变
            pts1 = np.float32([left_point, heigth_point, right_point])
            M = cv2.getAffineTransform(pts1, pts2)
            dst = cv2.warpAffine(oldimg, M, (pic_width, pic_hight))
            point_limit(right_point)
            point_limit(heigth_point)
            point_limit(new_left_point)
            car_img = dst[int(right_point[1]):int(heigth_point[1]), int(new_left_point[0]):int(right_point[0])]
            car_imgs.append(car_img)
            cv2.imshow("card", car_img)
            cv2.waitKey(0)
    return car_imgs

def img_color(card_imgs):
    colors = []
    for card_index, card_img in enumerate(card_imgs):
        green = yello = blue = black = white = 0
        card_img_hsv = cv2.cvtColor(card_img, cv2.COLOR_BGR2HSV)
        # 有转换失败的可能，原因来自于上面矫正矩形出错
        if card_img_hsv is None:
            continue
        row_num, col_num = card_img_hsv.shape[:2]
        card_img_count = row_num * col_num

        for i in range(row_num):
            for j in range(col_num):
                H = card_img_hsv.item(i, j, 0)
                S = card_img_hsv.item(i, j, 1)
                V = card_img_hsv.item(i, j, 2)
                if 11 < H <= 34 and S > 34:  # 图片分辨率调整
                    yello += 1
                elif 35 < H <= 99 and S > 34:  # 图片分辨率调整
                    green += 1
                elif 99 < H <= 124 and S > 34:  # 图片分辨率调整
                    blue += 1

                if 0 < H < 180 and 0 < S < 255 and 0 < V < 46:
                    black += 1
                elif 0 < H < 180 and 0 < S < 43 and 221 < V < 225:
                    white += 1
        color = "no"

        limit1 = limit2 = 0
        if yello * 2 >= card_img_count:
            color = "yello"
            limit1 = 11
            limit2 = 34  # 有的图片有色偏偏绿
        elif green * 2 >= card_img_count:
            color = "green"
            limit1 = 35
            limit2 = 99
        elif blue * 2 >= card_img_count:
            color = "blue"
            limit1 = 100
            limit2 = 124  # 有的图片有色偏偏紫
        elif black + white >= card_img_count * 0.7:
            color = "bw"
        print(color)
        colors.append(color)
        # print(blue, green, yello, black, white, card_img_count)
        # cv2.imshow("color", card_img)
        # cv2.waitKey(0)
        if limit1 == 0:
            continue

    return  colors