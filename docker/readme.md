# docker 运行

## 注意

请先修改 `.env.docker` 中的配置信息，数据库、已经配置好，修改后需要 `docker compose down` 清理

## 测试

```bash
docker-compose up -d
# 浏览器打开 http://127.0.0.1:6080/
# 打开远程桌面中的终端
# 数据库改为 docker-compose 文件的地址密码
docker exec -it ubuntu-plate bash
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
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}

```

启动后 浏览器打开 `http://127.0.0.1:6080/`
