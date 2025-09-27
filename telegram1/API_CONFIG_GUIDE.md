# API 服务器配置指南

## 🌐 当前服务器信息

- **本机 IP**: 192.168.10.78
- **公网 IP**: 188.253.121.62
- **API 端口**: 5000
- **服务器状态**: ✅ 正常运行

## 📋 配置选项

### 1. 本地开发环境
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```
**适用场景**: 游戏和 API 都在同一台机器上运行

### 2. 局域网访问
```javascript
const API_BASE_URL = 'http://192.168.10.78:5000/api';
```
**适用场景**: 游戏部署在局域网内的其他设备上

### 3. 公网访问
```javascript
const API_BASE_URL = 'http://188.253.121.62:5000/api';
```
**适用场景**: 游戏部署在公网上，需要配置端口转发

### 4. 生产环境 (推荐)
```javascript
const API_BASE_URL = 'https://your-domain.com/api';
```
**适用场景**: 使用域名和 HTTPS 的专业部署

## 🚀 部署步骤

### 步骤 1: 修改游戏配置
在 `index.html` 中修改 API_BASE_URL：

```javascript
// 根据部署环境选择对应的配置
const API_BASE_URL = 'http://192.168.10.78:5000/api';  // 局域网
// const API_BASE_URL = 'http://188.253.121.62:5000/api';  // 公网
// const API_BASE_URL = 'https://your-domain.com/api';  // 生产环境
```

### 步骤 2: 启动 API 服务器
```bash
python score_api.py
```

### 步骤 3: 部署游戏
将修改后的 `index.html` 部署到静态网站托管服务

## 🔧 高级配置

### 使用 Nginx 反向代理 (推荐)

1. 安装 Nginx
2. 配置反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /api/ {
        proxy_pass http://localhost:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location / {
        root /path/to/your/game;
        index index.html;
    }
}
```

### 使用 PM2 管理进程

```bash
# 安装 PM2
npm install -g pm2

# 启动 API 服务器
pm2 start score_api.py --name "score-api"

# 设置开机自启
pm2 startup
pm2 save
```

## 🛡️ 安全注意事项

1. **防火墙配置**: 确保 5000 端口对需要的客户端开放
2. **HTTPS 使用**: 生产环境必须使用 HTTPS
3. **CORS 配置**: 如果需要跨域访问，在 `score_api.py` 中添加 CORS 支持
4. **访问控制**: 考虑添加 API 密钥验证

## 📊 监控和日志

API 服务器会输出详细的日志信息，包括：
- 用户分数查询
- 分数更新操作
- 错误处理

## 🆘 故障排除

### 常见问题

1. **API 无法访问**
   - 检查防火墙设置
   - 确认 API 服务器正在运行
   - 验证 IP 地址和端口

2. **跨域问题**
   - 在 `score_api.py` 中添加 CORS 支持
   - 使用代理服务器

3. **HTTPS 问题**
   - 确保使用有效的 SSL 证书
   - 检查证书链配置

### 测试连接

```bash
# 测试本地连接
curl http://localhost:5000/api/health

# 测试局域网连接
curl http://192.168.10.78:5000/api/health

# 测试公网连接
curl http://188.253.121.62:5000/api/health
```
