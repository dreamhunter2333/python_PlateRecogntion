# -*- coding: utf-8 -*-
import os
import uuid
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flask import send_from_directory
from flask_img.db import get_db

import time
import cv2
import numpy
from .lib import img_function as predict
from .lib import img_math as img_math
from pyzbar import pyzbar
import shutil


predictor = predict.CardPredictor()
predictor.train_svm()

bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
IMAGE_FOLDER = os.path.join(bp.root_path, '..', 'images')
TMP_FOLDER = os.path.join(bp.root_path, 'tmp')
CARD_COLOR = {
    "blue": "蓝色",
    "yello": "黄色",
    "green": "绿色"
}

try:
    shutil.rmtree(IMAGE_FOLDER)
    os.makedirs(IMAGE_FOLDER)
except OSError:
    pass

try:
    shutil.rmtree(TMP_FOLDER)
    os.makedirs(TMP_FOLDER)
except OSError:
    pass


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        if 'car_image' not in request.files:
            flash('请选择识别文件')
            return redirect(request.url)
        image = request.files['car_image']
        if image.filename == '':
            flash('请选择识别文件')
            return redirect(request.url)
        if 'recon_option' not in request.form:
            flash('请选择识别类型')
            return redirect(request.url)
        recon_option = request.form['recon_option']
        image = request.files['car_image']
        if not image or not allowed_file(image.filename):
            flash('文件不存在或后缀不合法')
            return redirect(request.url)
        image_uuid = uuid.uuid4().hex
        filename = ''.join([image_uuid, '.', image.filename.rsplit('.', 1)[1]])
        image.save(os.path.join(IMAGE_FOLDER, filename))
        result = {}
        try:
            db = get_db()

            if recon_option == 'car':
                result = car_pic(filename)
            elif recon_option == 'barcode':
                result = barcode_pic(filename)
            db.execute(
                'INSERT INTO img_info (img_color_contours, img_only_color, barcode_info)'
                ' VALUES (?, ?, ?)',
                (
                    result.get('img_color_contours', ''),
                    result.get('img_only_color', ''),
                    ' '.join(result['text']) if result.get('text') else ''
                )
            )
            db.commit()
            result.update({
                'result': '识别成功'
            })
        except Exception as e:
            flash(e)
            result.update({
                'result': '识别失败'
            })
        return render_template('index.html', result=result)
    return render_template('index.html')


@bp.route('/image/<filename>')
def show_img(filename):
    return send_from_directory(IMAGE_FOLDER, filename)


@bp.route('/tmp/<filename>')
def show_tmp_img(filename):
    return send_from_directory(TMP_FOLDER, filename)


def car_pic(filename):
    pic_path = os.path.join(IMAGE_FOLDER, filename)
    img_bgr = img_math.img_read(pic_path)
    first_img, oldimg = predictor.img_first_pre(img_bgr)
    r_c, roi_c, color_c = predictor.img_color_contours(first_img, oldimg)
    r_color, roi_color, color_color = predictor.img_only_color(oldimg, oldimg, first_img)
    if roi_c is None and roi_color is None:
        raise ValueError('没有找到车牌')
    cv2.cv2.imwrite(os.path.join(TMP_FOLDER, "img_color_contours_"+filename), roi_c)
    cv2.cv2.imwrite(os.path.join(TMP_FOLDER, "img_only_color_"+filename), roi_color)
    # print(color_c, r_c, "|", color_color, r_color)
    return {
        'car': True,
        'img_color_contours': '颜色形状识别结果: ' + CARD_COLOR.get(color_c) + ' ' + r_c,
        'img_color_contours_path': '/tmp/img_color_contours_'+filename,
        'img_only_color': '颜色识别结果: ' + CARD_COLOR.get(color_color) + ' ' + r_color,
        'img_only_color_path': '/tmp/img_only_color_'+filename,
        'filepath': '/image/'+filename,
    }


def barcode_pic(filename):
    # load the input image
    image_path = os.path.join(IMAGE_FOLDER, filename)
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
    cv2.cv2.imwrite(os.path.join(TMP_FOLDER, filename), image)
    return {
        'barcode': True,
        'text': text_list,
        'filepath': '/tmp/' + filename,
    }
