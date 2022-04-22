#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import os
import base64
import jsonpath

from .config import settings


# ACCESS_TOKEN_URL 用于获取 ACCESS_TOKEN, POST请求,
# grant_type必须参数,固定为client_credentials,client_id必须参数,应用的API Key,client_secre 必须参数,应用的Secret Key.
ACCESS_TOKEN_URL = ''.join([
    'https://aip.baidubce.com/oauth/2.0/token?',
    'grant_type=client_credentials&',
    'client_id={API_KEY}&client_secret={SECRET_KEY}&'.format(
        API_KEY=settings.api_key,
        SECRET_KEY=settings.api_secret_key
    )
])
# 车牌识别 URL
LICENSE_PLATE = 'https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate?access_token={}'


def getToken():
    try:
        accessToken = requests.post(url=ACCESS_TOKEN_URL)
        accessTokenJson = accessToken.json()
        if dict(accessTokenJson).get('error') == 'invalid_client':
            print('获取accesstoken错误, 请检查API_KEY, SECRET_KEY是否正确!')
            return ""
        return accessTokenJson['access_token']
    except Exception as e:
        print("获取accesstoken错误", e)
        return ""


ACCESS_TOKEN = getToken()
LICENSE_PLATE_URL = LICENSE_PLATE.format(ACCESS_TOKEN)
HEADER = {
    'Content-Type': 'application/x-www-form-urlencoded',
}


def postLicensePlate(image_path):
    if not os.path.exists(image_path):
        return

    image_base64 = ""
    with open(image_path, 'rb') as image:
        image_base64 = base64.b64encode(image.read())
    if not image_base64:
        print('image参数不能为空!')
        return

    licensePlate = requests.post(
        url=LICENSE_PLATE_URL,
        headers=HEADER,
        data={'image': image_base64}
    )
    return licensePlate.json()


def api_pic(image_path):

    if not ACCESS_TOKEN:
        print("无 ACCESS_TOKEN")
        return "", ""

    # 车牌号识别
    try:
        testLicensePlatejson = postLicensePlate(image_path=image_path)
    except Exception as e:
        print("API 识别失败", e)
        return "", ""

    if not testLicensePlatejson:
        return "", ""

    testcolor = jsonpath.jsonpath(testLicensePlatejson, '$..color')
    testtext = jsonpath.jsonpath(testLicensePlatejson, '$..number')

    testcolorstr = "".join(testcolor) if testcolor else ""
    testtextstr = "".join(testtext) if testcolor else ""
    # print('车牌号api识别：', testcolorstr, testtextstr)
    return testcolorstr, testtextstr
