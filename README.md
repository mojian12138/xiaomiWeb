# 小米运动（Zepp Life）步数更新 Web 工具

这是一个基于 Flask 的 Web 项目，提供可视化界面来提交 Zepp Life（原小米运动）账号、密码和目标步数，并调用接口完成步数更新。

## 项目功能

- 深色风格 Web 界面，支持账号、密码、步数输入和滑块调节
- 支持“步数更新 / 关于工具”双页签切换
- 支持提交后前端提示成功或失败信息
- 后端复用现有 `zepp_helper` 逻辑进行登录与步数上报
- 支持反向代理场景（已启用 `ProxyFix`）
- 默认步数为 `8888`
- 网站图标使用 `static/img/favicon.png`

## 目录说明

- `app.py`：Flask 入口，提供页面和 API
- `web_runner.py`：登录与步数更新的封装逻辑
- `templates/index.html`：前端页面模板
- `static/css/style.css`：页面样式
- `static/js/script.js`：页面交互脚本
- `util/`：接口与加密相关工具

## 本地运行

### 1) 安装依赖

```bash
pip install -r requirements.txt
```

### 2) 启动服务

```bash
python app.py
```

默认访问地址：

```text
http://127.0.0.1:12303
```

## 使用说明

1. 打开网页后，在“步数更新”页填写 Zepp Life 账号和密码  
2. 输入或拖动滑块设置目标步数  
3. 点击“动动吧”提交  
4. 页面底部会返回接口执行结果

## 注意事项

- 本项目仅用于学习和测试
- 账号请使用 Zepp Life 账号（不是小米主账号）
- 若 APP 未绑定手环/手表，步数可能无法同步到微信运动
- 请避免设置明显异常的超高步数

## 宝塔面板部署方案（含反代）

以下方案适用于 Linux 宝塔面板。

### 一、准备环境

1. 宝塔安装 `Python项目管理器`、`Nginx`
2. 上传项目代码到服务器目录，例如：
   - `/www/wwwroot/xiaomiWeb`

### 二、创建 Python 项目

1. 打开宝塔 `Python项目管理器` → `添加项目`
2. 项目路径选择 `/www/wwwroot/xiaomiWeb`
3. 启动文件选择 `app.py`
4. 安装依赖：
   - `pip install -r requirements.txt`
5. 监听端口示例：`12303`
6. 启动项目并确认可访问：
   - `http://127.0.0.1:12303`

### 三、配置 Nginx 反向代理

在宝塔创建站点（如 `step.yourdomain.com`）后，进入该站点的 Nginx 配置，设置反代到 Flask 端口。

示例配置：

```nginx
location / {
    proxy_pass http://127.0.0.1:12303;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

保存并重载 Nginx 后，通过域名访问即可。

### 四、HTTPS（推荐）

1. 在宝塔站点中申请 SSL 证书（Let’s Encrypt）
2. 开启强制 HTTPS
3. 保持反代配置不变

### 五、反代兼容说明

项目在 `app.py` 中已启用：

- `werkzeug.middleware.proxy_fix.ProxyFix`

可正确识别反代传入的 `X-Forwarded-*` 头部，支持宝塔 Nginx 反向代理场景。
