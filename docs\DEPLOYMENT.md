# 审思明辨——智判法案双擎系统
# 部署指南

## 目录

1. [环境要求](#环境要求)
2. [本地开发部署](#本地开发部署)
3. [生产环境部署](#生产环境部署)
4. [Docker 部署](#docker-部署)
5. [常见问题](#常见问题)

---

## 环境要求

### Python 版本

- Python 3.9 或更高版本
- 推荐使用 Python 3.10+

### 系统要求

- 内存: 最低 2GB，推荐 4GB+
- 磁盘: 最低 1GB 可用空间

### 依赖服务

- 腾讯云账号（用于混元大模型）
- 得理开放平台账号（提供 API 凭证）

---

## 本地开发部署

### 1. 克隆项目

```bash
git clone https://github.com/liumengyue1234/fuwuwaibao.git
cd fuwuwaibao
```

### 2. 创建虚拟环境

```bash
# 使用 venv
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入以下配置：
```

**.env 文件配置示例**:

```env
# 腾讯云配置
TC_SECRET_ID=your_secret_id
TC_SECRET_KEY=your_secret_key
TC_REGION=ap-guangzhou

# 腾讯混元大模型配置
HUNYUAN_APP_ID=your_hunyuan_app_id
HUNYUAN_APP_KEY=your_hunyuan_app_key

# 得理开放平台（测试环境）
DELILEGAL_APP_ID=QthdBErlyaYvyXul
DELILEGAL_SECRET=EC5D455E6BD348CE8E18BE05926D2EBE

# 腾讯文档配置
TENCENT_DOC_APP_ID=your_tencent_doc_app_id
TENCENT_DOC_SECRET=your_tencent_doc_secret
```

### 5. 启动应用

```bash
streamlit run app.py
```

应用将在浏览器中打开，默认地址: http://localhost:8501

---

## 生产环境部署

### 方案一：使用 Gunicorn + Nginx

#### 1. 安装 Gunicorn

```bash
pip install gunicorn
```

#### 2. 创建 Gunicorn 配置文件

**gunicorn_config.py**:

```python
bind = "0.0.0.0:8501"
workers = 4
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
timeout = 120
```

#### 3. 创建启动脚本

**start.sh**:

```bash
#!/bin/bash
gunicorn -c gunicorn_config.py app:app
```

#### 4. Nginx 配置

```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 方案二：使用 Docker

#### 1. 创建 Dockerfile

**Dockerfile**:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8501

# 启动命令
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

#### 2. 创建 docker-compose.yml

**docker-compose.yml**:

```yaml
version: '3.8'

services:
  fuwuwaibao:
    build: .
    ports:
      - "8501:8501"
    environment:
      - TC_SECRET_ID=${TC_SECRET_ID}
      - TC_SECRET_KEY=${TC_SECRET_KEY}
      - HUNYUAN_APP_ID=${HUNYUAN_APP_ID}
      - HUNYUAN_APP_KEY=${HUNYUAN_APP_KEY}
    restart: unless-stopped
```

#### 3. 启动服务

```bash
docker-compose up -d
```

---

## 云平台部署

### 腾讯云服务器

1. 使用腾讯云 CVM 实例
2. 安装 Docker 和 Docker Compose
3. 参考上述 Docker 部署方案

### 腾讯云函数/SCF

如需无服务器部署，可将核心功能封装为云函数。

---

## 环境变量说明

| 变量名 | 必填 | 说明 |
|--------|------|------|
| TC_SECRET_ID | 是 | 腾讯云 SecretId |
| TC_SECRET_KEY | 是 | 腾讯云 SecretKey |
| TC_REGION | 否 | 腾讯云地域，默认 ap-guangzhou |
| HUNYUAN_APP_ID | 是 | 腾讯元器智能体 ID |
| HUNYUAN_APP_KEY | 是 | 腾讯元器 API Key |
| DELILEGAL_APP_ID | 否 | 得理开放平台 AppId |
| DELILEGAL_SECRET | 否 | 得理开放平台 Secret |
| TENCENT_DOC_APP_ID | 否 | 腾讯文档 AppId |
| TENCENT_DOC_SECRET | 否 | 腾讯文档 Secret |

---

## 常见问题

### Q: 应用启动失败？

**A**: 检查以下内容：
1. Python 版本是否满足要求（3.9+）
2. 依赖是否安装成功
3. .env 文件是否配置正确

### Q: API 调用返回 null？

**A**: 
- 腾讯混元 API: 选择更长上下文的模型（200K/128K）
- 得理 API: 检查关键词格式

### Q: 如何提高响应速度？

**A**:
1. 使用缓存减少重复请求
2. 优化数据库查询
3. 增加服务器资源
4. 使用 CDN 加速静态资源

### Q: 如何扩展功能？

**A**:
1. 在 `core/` 目录添加新的核心模块
2. 在 `services/` 目录添加新的服务
3. 在 `app.py` 中添加新的页面和功能

---

## 安全建议

1. **敏感信息**: 不要将 .env 文件提交到代码仓库
2. **API 密钥**: 定期更换 API 密钥
3. **输入验证**: 对用户输入进行验证和过滤
4. **日志记录**: 记录关键操作日志，便于审计
5. **HTTPS**: 生产环境务必使用 HTTPS
