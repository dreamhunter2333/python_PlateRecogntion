# Python opencv 车牌识别

## 原理简介

* 车牌字符识别使用的算法是opencv的SVM

* opencv的SVM使用代码来自于opencv附带的sample，StatModel类和SVM类都是sample中的代码

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
        # 缩小图片 转化成灰度图像 创建20*20的元素为1的矩阵 开操作，并和img重合 基于OTSU的二值化处理 找到图像边缘
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

### 一. 车牌图像预处理
* 1.将彩色图像转化为灰度图，并采用20*20模版对图像进行高斯模糊来缓解由照相机或其他环境噪声（如果不这么做，我们会得到很多垂直边缘，导致错误检测。）

![img_gray](/pic/img_pre/img_gray.jpg)

![img_opening](/pic/img_pre/img_opening.jpg)

* 2.使用Otsu自适应阈值算法获得图像二值化的阈值，并由此得到一副二值化图片

![img_edge](/pic/img_pre/img_edge.jpg)

* 3.采用闭操作，去除每个垂直边缘线之间的空白空格，并连接所有包含 大量边缘的区域（这步过后，我们将有许多包含车牌的候选区域）

![img_contours](/pic/img_pre/img_contours.jpg)

* 4.由于大多数区域并不包含车牌，我们使用轮廓外接矩形的纵横比和区域面积，对这些区域进行区分。
    * a.首先使用findContours找到外部轮廓
    * b.使用minAreaRect获得这些轮廓的最小外接矩形，存储在vector向量中
    * c.使用面积和长宽比阈值，作基本的验证 


### 二. 车牌定位
  车牌定位的主要工作是从摄入的汽车图像中找到汽车牌照所在位置，并把车牌从该区域中准确地分割出来，供字符分割使用。
因此，牌照区域的确定是影响系统性能的重要因素之一，牌照的定位与否直接影响到字符分割和字符识别的准确率。
目前车牌定位的方法很多，但总的来说可以分为以下4类：
* （1）基于颜色的分割方法，这种方法主要利用颜色空间的信息，实现车牌分割，包括彩色边缘算法、颜色距离和相似度算法等；
* （2）基于纹理的分割方法，这种方法主要利用车牌区域水平方向的纹理特征进行分割，包括小波纹理、水平梯度差分纹理等；
* （3）基于边缘检测的分割方法；
* （4）基于数学形态法的分割方法。 
为了代码实现上的方便，我采用的是基于边缘检测的分割方法和基于颜色的分割方法。

### 二. 车牌图像矩形矫正
