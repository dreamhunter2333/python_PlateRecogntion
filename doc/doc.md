# Python opencv 车牌识别

## 原理简介

* 车牌字符识别使用的算法是opencv的SVM，opencv的SVM使用代码来自于opencv附带的sample，StatModel类和SVM类都是sample中的代码

* 训练数据文件`svm.dat`和`svmchinese.dat`

* 使用`图像边缘`和`车牌颜色`定位车牌,再识别`字符`

```bash
# 主函数中初始化车牌识别需要的算法函数，并加载训练数据文件
self.predictor = predict.CardPredictor()
self.predictor.train_svm()
# lib下算法函数加载训练数据文件
class CardPredictor:
    def __init__(self):
        pass
    # 加载训练数据文件
    def train_svm(self):
        # 识别英文字母和数字
        self.model = SVM(C=1, gamma=0.5)
        # 识别中文
        self.modelchinese = SVM(C=1, gamma=0.5)
        if os.path.exists("lib/svm.dat"):
            self.model.load("lib/svm.dat")
        if os.path.exists("lib/svmchinese.dat"):
            self.modelchinese.load("lib/svmchinese.dat")

```

```bash
# main.py 主函数中车牌识别函数
    def pic(self, pic_path):
        # 以uint8方式读取 pic_path 放入 img_bgr 中，cv2.IMREAD_COLOR读取彩色照片
        img_bgr = img_math.img_read(pic_path)
        # 缩小图片 转化成灰度图像 创建20*20的元素为1的矩阵 开操作，并和img重合 Otsu’s二值化 找到图像边缘
        # first_img, oldimg 已经处理好的图像文件 原图像文件
        first_img, oldimg = self.predictor.img_first_pre(img_bgr)
        # 未开启摄像头时显示经过resize的图片
        if not self.cameraflag:
            self.imgtk = self.get_imgtk(img_bgr)
            self.image_ctl.configure(image=self.imgtk)
        # 开始进行识别
        # img_color_contours形状定位识别 输入 预处理好的图像 原图像 
        # 排除面积最小的点 进行矩形矫正 转换 分隔字符 分离车牌字符 
        # return 识别到的字符、定位的车牌图像、车牌颜色
        # img_only_color颜色定位识别  输入 预处理好的图像 原图像 
        # 根据阈值找到对应颜色 认为水平方向，最大的波峰为车牌区域 查找垂直直方图波峰 去掉车牌上下边缘1个像素，避免白边影响阈值判断 分隔字符 分离车牌字符 
        # return 识别到的字符、定位的车牌图像、车牌颜色
        th1 = ThreadWithReturnValue(target=self.predictor.img_color_contours, args=(first_img, oldimg))
        th2 = ThreadWithReturnValue(target=self.predictor.img_only_color, args=(oldimg, oldimg, first_img))
        th1.start()
        th2.start()
        r_c, roi_c, color_c = th1.join()
        r_color, roi_color, color_color = th2.join()
        # 显示 识别到的字符、定位的车牌图像、车牌颜色
        self.show_roi2(r_color, roi_color, color_color)
        self.show_roi1(r_c, roi_c, color_c)
```