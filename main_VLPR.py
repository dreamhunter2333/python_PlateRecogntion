# -*- coding: utf-8 -*-
__author__ = '樱花落舞'
import cv2
import img_function
import tkinter as tk
from tkinter.filedialog import *
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
import numpy as np


filename = askopenfilename(title="选择识别图片", filetypes=[("jpg图片", "*.jpg"),("png图片","*.png")])




ans = img_function.img_main()
first_img,oldimg = ans.img_first_pre(filename)
ans.img_color_Contours(first_img,oldimg)

