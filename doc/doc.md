# Python opencv 车牌识别

## 原理简介

* 训练数据文件`svm.dat`和`svmchinese.dat`

* 使用`图像边缘`和`车牌颜色`定位车牌,再识别`字符`

```bash
self.predictor = predict.CardPredictor()
self.predictor.train_svm()
```
