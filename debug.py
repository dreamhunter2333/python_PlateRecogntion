# -*- coding: utf-8 -*-
__author__ = '樱花落舞'
import cv2

def img_show(filename):
    cv2.imshow("img_show",filename)
    cv2.waitKey(0)

def img_contours(oldimg,box):
    oldimg = cv2.drawContours(oldimg, [box], 0, (0, 0, 255), 2)
    cv2.imshow("img_contours", oldimg)
    cv2.waitKey(0)

