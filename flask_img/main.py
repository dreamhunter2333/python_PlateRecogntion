# -*- coding: utf-8 -*-
import os
import cv2
import time
import base64
import numpy
import functools
from pyzbar import pyzbar

from flask import Blueprint, request
from flask_restful import Resource, Api

from .lib import img_function as predict
from .lib import img_math as img_math
from .lib.tempdir import tempdir


predictor = predict.CardPredictor()
predictor.train_svm()

bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
CARD_COLOR = {
    "blue": "蓝色",
    "yello": "黄色",
    "green": "绿色"
}


def errortrack(f):
    @functools.wraps(f)
    def wrap(*args, **kw):
        try:
            return f(*args, **kw)
        except Exception as e:
            return {
                'code': 400,
                'message': str(e)
            }
    return wrap

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

api = Api(bp)

class ReconPic(Resource):

    @errortrack
    def post(self):
        image = request.files.get('image')
        recon_option = request.form.get('recon_option')

        if not image:
            return {
                'code': 400,
                'message':'请选择识别文件'
            }
        if not allowed_file(image.filename):
            return {
                'code': 400,
                'message':'文件不存在或后缀不合法'
            }
        if recon_option not in ('car', 'barcode'):
            return {
                'code': 400,
                'message':'请选择识别类型'
            }
        with tempdir() as img_dir:
            pic_path = os.path.join(img_dir, image.filename)
            image.save(pic_path)
            if recon_option == 'car':
                return car_pic(img_dir, pic_path)
            elif recon_option == 'barcode':
                return barcode_pic(img_dir, pic_path)
            return {
                'code': 400,
                'message':'识别失败'
            }

api.add_resource(ReconPic, '/recon_pic')


def car_pic(img_dir, pic_path):
    img_bgr = img_math.img_read(pic_path)
    first_img, oldimg = predictor.img_first_pre(img_bgr)
    r_c, roi_c, color_c = predictor.img_color_contours(first_img, oldimg)
    r_color, roi_color, color_color = predictor.img_only_color(oldimg, oldimg, first_img)
    if roi_c is None and roi_color is None:
        raise ValueError('没有找到车牌')
    img_color_contours_path = os.path.join(img_dir, "img_color_contours.png")
    cv2.cv2.imwrite(img_color_contours_path, roi_c)
    img_only_color_path = os.path.join(img_dir, "img_only_color.png")
    cv2.cv2.imwrite(img_only_color_path, roi_color)

    with open(img_only_color_path, 'rb') as f1, open(img_only_color_path, 'rb') as f2:
        img_color_contours_pic = base64.b64encode(f1.read())
        img_only_color_pic = base64.b64encode(f2.read())

    return {
        'code': 200,
        'text': [
            '颜色形状识别结果: ' + CARD_COLOR.get(color_c) + ' ' + r_c,
            '颜色识别结果: ' + CARD_COLOR.get(color_color) + ' ' + r_color
        ],
        'pic': [img_color_contours_pic.decode(), img_only_color_pic.decode()]
    }


def barcode_pic(img_dir, image_path):
    image = cv2.cv2.imread(image_path)
    # find the barcodes in the image and decode each of the barcodes
    barcodes = pyzbar.decode(image)
    # loop over the detected barcodes
    text_list = []
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        # draw the barcode data and barcode type on the image
        text = "({}): {}".format(barcodeType, barcodeData)
        text_list.append(text)
        cv2.cv2.putText(image, text, (x, y - 10), cv2.cv2.FONT_HERSHEY_TRIPLEX,
            0.5, (0, 255, 0), 1)
    barcode_path = os.path.join(img_dir, 'barcode.png')
    cv2.cv2.imwrite(barcode_path, image)

    with open(barcode_path, 'rb') as f:
        barcode_pic = base64.b64encode(f.read())

    return {
        'code': 200,
        'text': text_list,
        'pic': [barcode_pic.decode()],
    }
