# Python Flask Bootstrap opencv 车牌识别 二维码条形码识别

[![img](https://img.shields.io/github/stars/jinmu333/python_PlateRecogntion.svg?logoColor=blue&style=for-the-badge) ![img](https://img.shields.io/github/forks/jinmu333/python_PlateRecogntion.svg?logoColor=blue&style=for-the-badge) ![img](https://img.shields.io/github/last-commit/jinmu333/python_PlateRecogntion.svg?color=blue&style=for-the-badge) ![img](https://img.shields.io/badge/python-3-blue.svg?style=for-the-badge)](https://github.com/jinmu333/python_PlateRecogntion)
[![img](https://img.shields.io/badge/link-996.icu-red.svg?style=for-the-badge)](https://github.com/996icu/996.ICU)

## 简介

* Flask Bootstrap 网页实现
* 基于Opencv的车牌识别系统 二维码条形码识别系统

## [原理简介](doc/doc.md)

![demo](README/demo.png)

![demo2](README/demo2.png)

![demo3](README/demo3.png)

## ## docker 依赖安装 或者本机依赖安装二选一

## docker 依赖安装

安装docker

```bash
cd docker
bash start.sh build
bash start.sh
```

打开 [localhost:9999](http://localhost:9999)

## 本机依赖安装

```bash
# Installing ZBar for Ubuntu can be accomplished with the following command:
# An OpenCV barcode and QR code scanner with ZBar
sudo apt-get install libzbar0
```

```bash
# Installing ZBar for macOS
# Installing ZBar for macOS using brew is equally as easy (assuming you have Homebrew installed):
brew install zbar
```

```bash
cd docker
python3 -m pip install -r requirements.txt
```

## 运行

```bash
# 运行
python3 start
```
