#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'jinmu333'

import xlrd
import xlwt
from xlutils import copy

row = 0
i = 0


def create_excel():
    global row
    row = 0
    i = 0
    excel_path2 = "data.xls"
    w = xlwt.Workbook()
    w_sheet = w.add_sheet('1')
    alignment = xlwt.Alignment() #创建居中
    style = xlwt.XFStyle() # 创建样式
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style.alignment = alignment # 给样式添加文字居中属性
    tall_style = xlwt.easyxf('font:height 720')  # 36pt
    first_row = w_sheet.row(0)
    first_row.set_style(tall_style)
    value2 = ["时间", "形状识别车牌颜色", "形状识别车牌号", "颜色识别车牌颜色", "颜色识别车牌号", "api", "图像来源"]
    i = 0
    while (i <= 6):
        clo = i
        w_sheet.write(row, clo, value2[i], style)
        w_sheet.col(i).width = 7777
        i = i + 1
    w_sheet.col(6).width = 30000
    row = 1
    first_row = w_sheet.row(row)
    first_row.set_style(tall_style)
    w.save(excel_path2)
    print("excel创建成功")


def excel_add(the_value):
    excel_path = "data.xls"
    rbook = xlrd.open_workbook(excel_path, formatting_info=True)
    wbook = copy.copy(rbook)
    w_sheet = wbook.get_sheet(0)
    alignment = xlwt.Alignment() #创建居中
    style = xlwt.XFStyle() # 创建样式
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    alignment.vert = xlwt.Alignment.VERT_CENTER
    style.alignment = alignment # 给样式添加文字居中属性
    tall_style = xlwt.easyxf('font:height 720')  # 36pt
    global row
    first_row = w_sheet.row(row)
    first_row.set_style(tall_style)
    i = 0
    while (i <= 6):
        clo = i
        w_sheet.write(row, clo, the_value[i], style)
        i = i + 1
    row = row + 1
    wbook.save(excel_path)
    print("excel写入成功")
