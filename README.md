# Python opencv 车牌识别
[![img](https://img.shields.io/github/stars/jinmu333/python_PlateRecogntion.svg?logoColor=blue&style=for-the-badge) ![img](https://img.shields.io/github/forks/jinmu333/python_PlateRecogntion.svg?logoColor=blue&style=for-the-badge) ![img](https://img.shields.io/github/last-commit/jinmu333/python_PlateRecogntion.svg?color=blue&style=for-the-badge) ![img](https://img.shields.io/badge/python-3-blue.svg?style=for-the-badge)](https://github.com/jinmu333/python_PlateRecogntion)
[![img](https://img.shields.io/badge/link-996.icu-red.svg?style=for-the-badge)](https://github.com/996icu/996.ICU)
## 简介  [原理简介](doc/doc.md)

****

* 车牌搜索识别找出某个车牌号
* 对比识别车牌系统
* 车牌数据库认证系统
* 车牌图文搜索系统
* 车牌数据库搜索系统
* 文件图片识别车牌
* 网络图片地址识别车牌
* 实时截图识别车牌
* 图片自适应窗口大小
* 摄像头拍照识别车牌
* 使用 [hyperlpr](https://github.com/zeusees/HyperLPR) 提高识别率

****

* 毕业设计基于Opencv的车牌识别系统
* 安装 python3.6 或 python3.7
* 使用hyperlpr提高识别率
* 两种方法都无法识别时调用百度api(有手动按钮)

****

## 开发环境配置

### windows 快速搭建环境

#### 下载虚拟环境 zip 解压到项目目录 venv 下

[https://github.com/jinmu333/python_PlateRecogntion/releases/download/v0.0.1/venv.zip](https://github.com/jinmu333/python_PlateRecogntion/releases/download/v0.0.1/venv.zip)

结构如下

```bash
$ ls -l venv/
total 10
drwxr-xr-x 1 dreamhunter 197609  0 Apr 16 17:18 Include/
drwxr-xr-x 1 dreamhunter 197609  0 Apr 16 17:18 Lib/
-rw-r--r-- 1 dreamhunter 197609 61 Apr 16 17:24 pip-selfcheck.json
-rw-r--r-- 1 dreamhunter 197609 92 Apr 16 17:18 pyvenv.cfg
drwxr-xr-x 1 dreamhunter 197609  0 Apr 16 17:24 Scripts/
```

#### 下载 mysql 便携版

[https://github.com/jinmu333/python_PlateRecogntion/releases/download/v0.0.1/mysql-server-winx64.zip](https://github.com/jinmu333/python_PlateRecogntion/releases/download/v0.0.1/mysql-server-winx64.zip)

解压后，cmd 执行 start.bat

### 手动安装依赖

``` bash
./venv/bin/python3 -m pip install -r requirements.txt
```

## 运行演示

windows 替换 python3 命令为 `venv\\Scripts\\python.exe`

[百度api网址](https://cloud.baidu.com/product/ocr)

``` bash
# 首次运行修改 img_api.py中的 ID,KEY的配置信息为自己百度api信息
INFO_CONFIG = {
    'ID': ' ',
    'API_KEY': ' ',
    'SECRET_KEY': ' '
}
# 运行
# 查看img_sql.py文件 数据库相关改为自己的(地址，用户名。密码，数据库名字)
# db = pymysql.connect("localhost", "python", "Python12345@", "chepai")
# GRANT ALL PRIVILEGES ON *.* TO 'username'@'localhost'
# windows 下载便携版
mysql.server start

# 运行登录界面
# 如为虚拟环境，需要替换文件中 python3 命令为
# windows 替换文件中 python3 命令为 exe 路径，如我提供的虚拟环境的 venv\\Scripts\\python.exe
python3 login.py

# 运行主界面
python3 main.py

# 运行车牌对比识别主界面
python3 match.py

# 运行车牌搜索识别主界面
python3 search.py

# 运行车牌认证主界面
python3 identification.py

# 运行车牌数据库搜索主界面
python3 search_sql.py

```

* [android数据库查询软件](https://github.com/jinmu333/android_sql)

## 图片展示

### 车牌搜索识别找出某个车牌号

![演示](pic/searchpic.png)

### 车牌对比识别前后是否一致

![演示](pic/duibi.gif)

### 主界面

![界面](pic/4.png)

### 网络图片识别

![演示](pic/3.png)

### 车牌认证

![identificationdemo](pic/identificationdemo.png)

### 车牌数据库搜索

![log](pic/search_sql.png)

### 两种方法都无法识别时百度api(有手动按钮)

![log](pic/api.png)

### 登录注册页面

![log](pic/log.gif)

### 运行数据写入数据库

![sql](pic/sql.png)

### 本次运行数据写入excel (data.xls)

![界面](pic/1.png)

### 欢迎界面

![欢迎界面](pic/2.png)
