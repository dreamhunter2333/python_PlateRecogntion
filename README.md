# Python opencv 车牌识别
## 简介
### 车牌搜索识别找出某个车牌号
### 对比识别车牌
### 文件图片识别车牌
### 网络图片地址识别车牌
### 实时截图识别车牌
### 图片自适应窗口大小
### 摄像头拍照识别车牌
### 摄像头实时识别车牌(测试)
### 使用[hyperlpr](https://github.com/zeusees/HyperLPR)提高识别率
毕业设计基于Opencv的车牌识别系统 \
安装 python3.4(macos下python3.7测试是可以的，摄像头卡卡的，win10+python3.7下摄像头狂闪) \
由于样本数据来自网络，因此识别率只是看看而已。但清楚的图片还是可以识别出来的。 \
使用hyperlpr提高识别率 \
两种方法都无法识别时调用百度api(有手动按钮)

``` bash

# 按顺序安装
pip3 install -U pip

pip3 install hyperlpr

python3 -m pip install numpy==1.14.6

pip3 install opencv-python==3.4.5.20

pip3 install pillow

pip3 install xlutils

pip3 install pymysql

pip3 install requests

pip3 install xlutils

```

## 运行演示
``` bash

# 运行
# 查看img_sql.py文件 数据库相关改为自己的(地址，用户名。密码，数据库名字)
# db = pymysql.connect("localhost", "python", "Python12345@", "chepai")
# GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost'
mysql.server start

# 运行登录界面
python3 login.py

# 运行主界面
python3 main.py

# 运行车牌对比识别主界面
python3 match.py

# 运行车牌搜索识别主界面
python3 search.py

```


## 车牌搜索识别找出某个车牌号
![演示](pic/searchpic.png)
## 车牌对比识别前后是否一致
![演示](pic/duibi.gif)
\
由于样本数据来自网络，使用hyperlpr提高识别率。但清楚的图片还是可以识别出来的。  \
![演示](pic/3.png)
## 两种方法都无法识别时百度api(手动按钮)
![log](pic/api.png)
## 登录注册页面
![log](pic/log.gif)
## 运行数据写入数据库
![sql](pic/sql.png)
## 本次运行数据写入excel (data.xls)
![界面](pic/1.png)
![界面](pic/4.png)
## 欢迎界面
![欢迎界面](pic/2.png)