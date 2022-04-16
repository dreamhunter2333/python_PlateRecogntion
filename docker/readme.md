# docker 运行

修改代码中的数据库链接地址为 mysql-db

## 测试

```bash
docker-compose up -d
# 浏览器打开 http://127.0.0.1:6080/
# 打开远程桌面中的终端
# 数据库改为 docker-compose 文件的地址密码
docker exec -it ubuntu-plate bash
export DISPLAY=:1
cd /app
python3 main.py
```

## 开发

安装 vscode remote container, 点击reopen in container

### 添加启动文件

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "login",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/login.py",
            "env": {
                "DISPLAY": ":1"
            },
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}

```

启动后 浏览器打开 `http://127.0.0.1:6080/`
