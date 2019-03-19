#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import os
import base64
import json

ACCESS_TOKEN = ''
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ID,KEY的配置信息
INFO_CONFIG = {
    'ID': '15788358',
    'API_KEY': 'ohtGa5yYoQEZ8Try8lnL99UK',
    'SECRET_KEY': 'qaDjyuXkf5MZ28g5C8pwFngDZenhswC3'
}

# URL配置
URL_LIST_URL = {
    # ACCESS_TOKEN_URL用于获取ACCESS_TOKEN, POST请求,
    #  grant_type必须参数,固定为client_credentials,client_id必须参数,应用的API Key,client_secre 必须参数,应用的Secret Key.
    'ACCESS_TOKEN_URL': 'https://aip.baidubce.com/oauth/2.0/token?' + 'grant_type=client_credentials&client_id={API_KEYS}&client_secret={SECRET_KEYS}&'.format(
        API_KEYS=INFO_CONFIG['API_KEY'], SECRET_KEYS=INFO_CONFIG['SECRET_KEY']),
    # 人脸识别
    'FACE_PLATE': 'https://aip.baidubce.com/rest/2.0/face/v3/match',

}


class AccessTokenSuper(object):
    pass


class AccessToken(AccessTokenSuper):
    def getToken(self):
        accessToken = requests.post(url=URL_LIST_URL['ACCESS_TOKEN_URL'])
        accessTokenJson = accessToken.json()
        if dict(accessTokenJson).get('error') == 'invalid_client':
            return '获取accesstoken错误，请检查API_KEY，SECRET_KEY是否正确！'
        return accessTokenJson


ACCESS_TOKEN = AccessToken().getToken()['access_token']

LICENSE_PLATE_URL = URL_LIST_URL['FACE_PLATE'] + '?access_token={}'.format(ACCESS_TOKEN)


class faceSuper(object):
    pass


class face(faceSuper):

    def __init__(self, image=None, image2=None):
        self.HEADER = {
            'Content-Type': 'application/json; charset=UTF-8',
        }
        if image is not None:
            imagepath = os.path.exists(image)
            if imagepath == True:
                images = image
                with open(images, 'rb') as images:
                    img1 = base64.b64encode(images.read())
            else:
                print("img1 not exits")
                return
        if image2 is not None:
            imagepath2 = os.path.exists(image2)
            if imagepath2 == True:
                images2 = image2
                with open(images2, 'rb') as images2:
                    img2 = base64.b64encode(images2.read())
            else:
                print("img2 not exits")
                return
        self.img = img1
        self.imgs = img2
        self.IMAGE_CONFIG1 = {"image": str(img1, 'utf-8'), "image_type": "BASE64"}
        self.IMAGE_CONFIG2 = {"image": str(img2, 'utf-8'), "image_type": "BASE64"}
        self.IMAGE_CONFIG = json.dumps([self.IMAGE_CONFIG1, self.IMAGE_CONFIG2])

    def postface(self):
        if (self.img==None and self.imgs==None):
            return 'image参数不能为空！'
        face = requests.post(url=LICENSE_PLATE_URL, headers=self.HEADER, data=self.IMAGE_CONFIG)
        return face.json()


def facef(FA1, FA2):
    testAccessToken = AccessToken()
    testface = face(image=FA1, image2=FA2)
    result_json = testface.postface()
    result = result_json['result']['score']
    print('人脸相似度：', result)
    if result > 80:
        print("是同一个人")
    else:
        print("不是同一个人")
    return '人脸相似度：' + str(result), result

