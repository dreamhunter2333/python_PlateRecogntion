#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'jinmu333'

import os
import cv2
from PIL import Image
import numpy as np
import lib.img_math as img_math
import lib.img_recognition as img_recognition

SZ = 20  # 训练图片长宽
MAX_WIDTH = 1000  # 原始图片最大宽度
Min_Area = 2000  # 车牌区域允许最大面积
PROVINCE_START = 1000


class StatModel(object):
    def load(self, fn):
        self.model = self.model.load(fn)

    def save(self, fn):
        self.model.save(fn)


class SVM(StatModel):
    def __init__(self, C=1, gamma=0.5):
        self.model = cv2.ml.SVM_create()
        self.model.setGamma(gamma)
        self.model.setC(C)
        self.model.setKernel(cv2.ml.SVM_RBF)
        self.model.setType(cv2.ml.SVM_C_SVC)

    # 训练svm
    def train(self, samples, responses):
        self.model.train(samples, cv2.ml.ROW_SAMPLE, responses)

    # 字符识别
    def predict(self, samples):
        r = self.model.predict(samples)
        return r[1].ravel()


class CardPredictor:
    def __init__(self):
        pass

    def train_svm(self):
        # 识别英文字母和数字
        self.model = SVM(C=1, gamma=0.5)
        # 识别中文
        self.modelchinese = SVM(C=1, gamma=0.5)
        if os.path.exists("lib/svm.dat"):
            self.model.load("lib/svm.dat")
        if os.path.exists("lib/svmchinese.dat"):
            self.modelchinese.load("lib/svmchinese.dat")


    def img_first_pre(self, car_pic_file):
        """
        :param car_pic_file: 图像文件
        :return:已经处理好的图像文件 原图像文件
        """
        if type(car_pic_file) == type(""):
            img = img_math.img_read(car_pic_file)
        else:
            img = car_pic_file

        pic_hight, pic_width = img.shape[:2]
        if pic_width > MAX_WIDTH:
            resize_rate = MAX_WIDTH / pic_width
            img = cv2.resize(img, (MAX_WIDTH, int(pic_hight * resize_rate)), interpolation=cv2.INTER_AREA)
        # 缩小图片

        blur = 5
        img = cv2.GaussianBlur(img, (blur, blur), 0)
        oldimg = img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite("tmp/img_gray.jpg", img)
        # 转化成灰度图像

        Matrix = np.ones((20, 20), np.uint8)
        img_opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, Matrix)
        img_opening = cv2.addWeighted(img, 1, img_opening, -1, 0)
        # cv2.imwrite("tmp/img_opening.jpg", img_opening)
        # 创建20*20的元素为1的矩阵 开操作，并和img重合

        ret, img_thresh = cv2.threshold(img_opening, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        img_edge = cv2.Canny(img_thresh, 100, 200)
        # cv2.imwrite("tmp/img_edge.jpg", img_edge)
        # Otsu’s二值化 找到图像边缘

        Matrix = np.ones((4, 19), np.uint8)
        img_edge1 = cv2.morphologyEx(img_edge, cv2.MORPH_CLOSE, Matrix)
        img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, Matrix)
        return img_edge2, oldimg

    def img_color_contours(self, img_contours, oldimg, add_box_point=False):
        """
        :param img_contours: 预处理好的图像
        :param oldimg: 原图像
        :return: 已经定位好的车牌
        """

        if img_contours.any():
            #config.set_name(img_contours)
            cv2.imwrite("tmp/img_contours.jpg", img_contours)

        pic_hight, pic_width = img_contours.shape[:2]

        card_contours, boxPoints = img_math.img_findContours(img_contours)
        card_imgs = img_math.img_Transform(card_contours, oldimg, pic_width, pic_hight)
        colors, car_imgs = img_math.img_color(card_imgs)
        predict_result = []
        predict_str = ""
        roi = None
        card_color = None
        box_point = None

        for i, color in enumerate(colors):
            if color in ("blue", "yello", "green"):
                card_img = card_imgs[i]
                # cv2.imwrite("tmp/card_img.jpg", card_img)
                try:
                    gray_img = cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY)
                    # cv2.imwrite("tmp/card_gray_img.jpg", gray_img)

                    # 黄、绿车牌字符比背景暗、与蓝车牌刚好相反，所以黄、绿车牌需要反向
                except:
                    pass
                if color == "green" or color == "yello":
                    gray_img = cv2.bitwise_not(gray_img)
                    # cv2.imwrite("tmp/card_gray_img2.jpg", gray_img)

                ret, gray_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                # cv2.imwrite("tmp/card_gray_img3.jpg", gray_img)

                x_histogram = np.sum(gray_img, axis=1)
                x_min = np.min(x_histogram)
                x_average = np.sum(x_histogram) / x_histogram.shape[0]
                x_threshold = (x_min + x_average) / 2

                wave_peaks = img_math.find_waves(x_threshold, x_histogram)
                if len(wave_peaks) == 0:
                    # print("peak less 0:")
                    continue
                # 认为水平方向，最大的波峰为车牌区域
                wave = max(wave_peaks, key=lambda x: x[1] - x[0])
                gray_img = gray_img[wave[0]:wave[1]]
                # cv2.imwrite("tmp/card_gray_img4.jpg", gray_img)

                # 查找垂直直方图波峰
                row_num, col_num = gray_img.shape[:2]
                # 去掉车牌上下边缘1个像素，避免白边影响阈值判断
                gray_img = gray_img[1:row_num - 1]
                # cv2.imwrite("tmp/card_gray_img5.jpg", gray_img)

                y_histogram = np.sum(gray_img, axis=0)
                y_min = np.min(y_histogram)
                y_average = np.sum(y_histogram) / y_histogram.shape[0]
                y_threshold = (y_min + y_average) / 5  # U和0要求阈值偏小，否则U和0会被分成两半
                wave_peaks = img_math.find_waves(y_threshold, y_histogram)
                if len(wave_peaks) <= 6:
                    # print("peak less 1:", len(wave_peaks))
                    continue

                wave = max(wave_peaks, key=lambda x: x[1] - x[0])
                max_wave_dis = wave[1] - wave[0]
                # 判断是否是左侧车牌边缘
                if wave_peaks[0][1] - wave_peaks[0][0] < max_wave_dis / 3 and wave_peaks[0][0] == 0:
                    wave_peaks.pop(0)

                # 组合分离汉字
                cur_dis = 0
                for wi, wave in enumerate(wave_peaks):
                    if wave[1] - wave[0] + cur_dis > max_wave_dis * 0.6:
                        break
                    else:
                        cur_dis += wave[1] - wave[0]
                if wi > 0:
                    wave = (wave_peaks[0][0], wave_peaks[wi][1])
                    wave_peaks = wave_peaks[wi + 1:]
                    wave_peaks.insert(0, wave)
                point = wave_peaks[2]
                point_img = gray_img[:, point[0]:point[1]]
                if np.mean(point_img) < 255 / 5:
                    wave_peaks.pop(2)

                if len(wave_peaks) <= 6:
                    # print("peak less 2:", len(wave_peaks))
                    continue

                part_cards = img_math.seperate_card(gray_img, wave_peaks)
                # i = 0
                # for wave in wave_peaks:
                #     cv2.imwrite("tmp/part_cards" + str(i) + ".jpg", part_cards[i])
                #     i += 1

                for pi, part_card in enumerate(part_cards):
                    # 可能是固定车牌的铆钉

                    if np.mean(part_card) < 255 / 5:
                        # print("a point")
                        continue
                    part_card_old = part_card

                    w = abs(part_card.shape[1] - SZ) // 2

                    part_card = cv2.copyMakeBorder(part_card, 0, 0, w, w, cv2.BORDER_CONSTANT, value=[0, 0, 0])
                    part_card = cv2.resize(part_card, (SZ, SZ), interpolation=cv2.INTER_AREA)
                    part_card = img_recognition.preprocess_hog([part_card])
                    if pi == 0:
                        resp = self.modelchinese.predict(part_card)
                        charactor = img_recognition.provinces[int(resp[0]) - PROVINCE_START]
                    else:
                        resp = self.model.predict(part_card)
                        charactor = chr(resp[0])
                    # 判断最后一个数是否是车牌边缘，假设车牌边缘被认为是1
                    if charactor == "1" and i == len(part_cards) - 1:
                        if part_card_old.shape[0] / part_card_old.shape[1] >= 7:  # 1太细，认为是边缘
                            continue
                    predict_result.append(charactor)
                    predict_str = "".join(predict_result)

                roi = card_img
                card_color = color
                box_point = boxPoints[i]
                break

        if (add_box_point == True):
            return predict_str, roi, card_color, box_point
        return predict_str, roi, card_color  # 识别到的字符、定位的车牌图像、车牌颜色

    def img_only_color(self, filename, oldimg, img_contours, add_box_point=False):
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
        lower_green = np.array([50, 50, 50])
        upper_green = np.array([100, 255, 255])
        hsv = cv2.cvtColor(filename, cv2.COLOR_BGR2HSV)
        mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask_green = cv2.inRange(hsv, lower_yellow, upper_green)
        output = cv2.bitwise_and(hsv, hsv, mask=mask_blue + mask_yellow + mask_green)
        # 根据阈值找到对应颜色

        output = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        Matrix = np.ones((20, 20), np.uint8)
        img_edge1 = cv2.morphologyEx(output, cv2.MORPH_CLOSE, Matrix)
        img_edge2 = cv2.morphologyEx(img_edge1, cv2.MORPH_OPEN, Matrix)

        card_contours, boxPoints = img_math.img_findContours(img_edge2)
        card_imgs = img_math.img_Transform(card_contours, oldimg, pic_width, pic_hight)
        colors, car_imgs = img_math.img_color(card_imgs)

        predict_result = []
        predict_str = ""
        roi = None
        card_color = None
        box_point = None

        for i, color in enumerate(colors):

            if color in ("blue", "yello", "green"):
                card_img = card_imgs[i]
                box_point = boxPoints[i]

                try:
                    gray_img = cv2.cvtColor(card_img, cv2.COLOR_BGR2GRAY)
                except:
                    print("gray转换失败")

                # 黄、绿车牌字符比背景暗、与蓝车牌刚好相反，所以黄、绿车牌需要反向
                if color == "green" or color == "yello":
                    gray_img = cv2.bitwise_not(gray_img)
                ret, gray_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                x_histogram = np.sum(gray_img, axis=1)

                x_min = np.min(x_histogram)
                x_average = np.sum(x_histogram) / x_histogram.shape[0]
                x_threshold = (x_min + x_average) / 2
                wave_peaks = img_math.find_waves(x_threshold, x_histogram)
                if len(wave_peaks) == 0:
                    # print("peak less 0:")
                    continue
                # 认为水平方向，最大的波峰为车牌区域
                wave = max(wave_peaks, key=lambda x: x[1] - x[0])
                gray_img = gray_img[wave[0]:wave[1]]
                # 查找垂直直方图波峰
                row_num, col_num = gray_img.shape[:2]
                # 去掉车牌上下边缘1个像素，避免白边影响阈值判断
                gray_img = gray_img[1:row_num - 1]
                y_histogram = np.sum(gray_img, axis=0)
                y_min = np.min(y_histogram)
                y_average = np.sum(y_histogram) / y_histogram.shape[0]
                y_threshold = (y_min + y_average) / 5  # U和0要求阈值偏小，否则U和0会被分成两半
                wave_peaks = img_math.find_waves(y_threshold, y_histogram)
                if len(wave_peaks) < 6:
                    # print("peak less 1:", len(wave_peaks))
                    continue

                wave = max(wave_peaks, key=lambda x: x[1] - x[0])
                max_wave_dis = wave[1] - wave[0]
                # 判断是否是左侧车牌边缘
                if wave_peaks[0][1] - wave_peaks[0][0] < max_wave_dis / 3 and wave_peaks[0][0] == 0:
                    wave_peaks.pop(0)

                # 组合分离汉字
                cur_dis = 0
                for wi, wave in enumerate(wave_peaks):
                    if wave[1] - wave[0] + cur_dis > max_wave_dis * 0.6:
                        break
                    else:
                        cur_dis += wave[1] - wave[0]
                if wi > 0:
                    wave = (wave_peaks[0][0], wave_peaks[i][1])
                    wave_peaks = wave_peaks[wi + 1:]
                    wave_peaks.insert(0, wave)

                # 存在 wave_peaks < 3 的情况，导致下面语法错误
                if (len(wave_peaks) < 3):
                    continue

                point = wave_peaks[2]
                point_img = gray_img[:, point[0]:point[1]]
                if np.mean(point_img) < 255 / 5:
                    wave_peaks.pop(2)

                if len(wave_peaks) <= 6:
                    # print("peak less 2:", len(wave_peaks))
                    continue

                part_cards = img_math.seperate_card(gray_img, wave_peaks)

                for pi, part_card in enumerate(part_cards):
                    # 可能是固定车牌的铆钉

                    if np.mean(part_card) < 255 / 5:
                        # print("a point")
                        continue
                    part_card_old = part_card

                    w = abs(part_card.shape[1] - SZ) // 2

                    part_card = cv2.copyMakeBorder(part_card, 0, 0, w, w, cv2.BORDER_CONSTANT, value=[0, 0, 0])
                    part_card = cv2.resize(part_card, (SZ, SZ), interpolation=cv2.INTER_AREA)
                    part_card = img_recognition.preprocess_hog([part_card])
                    if pi == 0:
                        resp = self.modelchinese.predict(part_card)
                        charactor = img_recognition.provinces[int(resp[0]) - PROVINCE_START]
                    else:
                        resp = self.model.predict(part_card)
                        charactor = chr(resp[0])
                    # 判断最后一个数是否是车牌边缘，假设车牌边缘被认为是1
                    if charactor == "1" and i == len(part_cards) - 1:
                        if part_card_old.shape[0] / part_card_old.shape[1] >= 7:  # 1太细，认为是边缘
                            continue
                    predict_result.append(charactor)
                    predict_str = "".join(predict_result)

                roi = card_img
                card_color = color
                break
        if add_box_point:
            # 识别到的字符、定位的车牌图像、车牌颜色、图片位置
            return predict_str, roi, card_color, box_point
        # 识别到的字符、定位的车牌图像、车牌颜色
        return predict_str, roi, card_color

    def img_mser(self, filename):
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

            if w * h > 1500 and 3 < ration < 4 and w > h:
                cropimg = img[y:y + h, x:x + w]
                colors_img.append(cropimg)

    # 根据区域位置 points, 用 cover img 覆盖该区域, 并返回新的 img
    def img_cover(self, origImg, coverImg, points):
        direction = 'horizontal'
        if (origImg.size[0] < origImg.size[1]):
            direction = 'vertical'

        # Read source image.
        # src = cv2.imread('original.jpg')
        coverImg.show()
        src = cv2.cvtColor(np.asarray(coverImg), cv2.COLOR_RGB2BGR)

        # resizedCoverImg = coverImg.resize((wh[0], wh[1]), Image.ANTIALIAS)
        # resizedCoverImg.save('/app/tmp/resize_cover_img.png')

        # Four corners of source image
        # Coordinates are in x,y system with x horizontal to the right and y vertical downward
        # listed clockwise from top left
        # pts_src = np.float32([[0, 0], [src.shape[1], 0], [src.shape[1], src.shape[0]], [0, src.shape[0]]])
        pts_src = np.float32([[0, 0], [src.shape[1], 0], [src.shape[1], src.shape[0]], [0, src.shape[0]]])

        # # Read destination image.
        # dst = cv2.imread('green_rect.png')
        origImg.show()
        dst = cv2.cvtColor(np.asarray(origImg), cv2.COLOR_RGB2BGR)

        # ### 竖屏
        # points[0] ## 左下角坐标
        # points[1] ## 左上角坐标
        # points[2] ## 右上角坐标
        # points[3] ## 右下角坐标
        # ### 横屏
        # points[0] ## 右下角坐标
        # points[1] ## 左下角坐标
        # points[2] ## 左上角坐标
        # points[3] ## 右上角坐标

        # 竖屏情况下需要转换下 points
        if direction == 'vertical':
            br = [points[3][0], points[3][1]]
            bl = [points[0][0], points[0][1]]
            tl = [points[1][0], points[1][1]]
            tr = [points[2][0], points[2][1]]
            points[0] = br
            points[1] = bl
            points[2] = tl
            points[3] = tr

        # 确定车牌位置
        w1 = None
        w2 = None
        h1 = None
        h2 = None
        if (points[1][0] > points[2][0]):
            w1 = int(points[2][0])
        else:
            w1 = int(points[1][0])

        if (points[0][0] > points[3][0]):
            w2 = int(points[0][0])
        else:
            w2 = int(points[3][0])

        if (points[2][1] > points[3][1]):
            h1 = int(points[3][1])
        else:
            h1 = int(points[2][1])

        if (points[0][1] > points[1][1]):
            h2 = int(points[0][1])
        else:
            h2 = int(points[1][1])

        # dst = cv2.imread('/app/car_pic/ganzou6.png')
        # [高度开始位置:高度结束位置, 宽度开始位置:宽度结束位置]
        dst[h1:h2,w1:w2] = [0, 255, 0]
        # print('dst ============ : ', h1, h2, w1, w2, dst.shape[1], direction)

        # # Four corners of destination image.
        # pts_dst = np.float32(points)
        pts_dst = np.float32([points[2], points[3], points[0], points[1]]) # 2 3 0 1
        # # Calculate Homography if more than 4 points
        # # h = forward transformation matrix
        # #h, status = cv2.findHomography(pts_src, pts_dst)

        # # Alternate if only 4 points
        h = cv2.getPerspectiveTransform(pts_src,pts_dst)

        # # Warp source image to destination based on homography
        # # size argument is width x height, so have to reverse shape values
        src_warped = cv2.warpPerspective(src, h, (dst.shape[1],dst.shape[0]))

        # # Set BGR color ranges
        lowerBound = np.array([0, 255, 0])
        upperBound = np.array([0, 255, 0])

        # # Compute mask (roi) from ranges in dst
        mask = cv2.inRange(dst, lowerBound, upperBound);

        # # Dilate mask, if needed, when green border shows
        kernel = np.ones((3,3),np.uint8)
        mask = cv2.dilate(mask,kernel,iterations = 1)

        # # Invert mask
        inv_mask = cv2.bitwise_not(mask)

        # # Mask dst with inverted mask
        dst_masked = cv2.bitwise_and(dst, dst, mask=inv_mask)

        # # Put src_warped over dst
        result = cv2.add(dst_masked, src_warped)

        # # Save outputs
        cv2.imwrite('tmp/warped_src.jpg', src_warped)
        cv2.imwrite('tmp/inverted_mask.jpg', inv_mask)
        cv2.imwrite('tmp/masked_dst.jpg', dst_masked)
        cv2.imwrite('tmp/perspective_composite.jpg', result)
        return src_warped, inv_mask, dst_masked, result
