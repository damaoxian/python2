# Telegram 游戏机器人项目

这是一个完整的 Telegram 游戏机器人项目，包含机器人后端、数据库集成和网页小游戏。

## 📁 项目结构

```
telegram1/
├── bot.py                 # Telegram 机器人主程序
├── client.py              # Telegram 客户端连接脚本
├── database_simple.py     # 数据库操作模块（简化版）
├── database_schema.sql    # 数据库表结构
├── score_api.py           # 分数 API 服务器
├── config.py              # 项目配置文件
├── index.html             # 网页小游戏
├── requirements.txt       # Python 依赖包
└── README.md              # 项目说明文档
```

## 🚀 核心功能

### 1. Telegram 游戏机器人 (bot.py)

基于 python-telegram-bot 库的完整游戏机器人，支持用户数据存储和游戏集成。

**主要功能：**
- `/start` 命令：发送欢迎消息
- `/game` 命令：启动小游戏
- 游戏回调处理：记录用户信息并传递到游戏
- 数据库集成：自动保存用户数据
- 详细日志记录：便于调试和监控

**核心特性：**
- 🎮 游戏集成：支持 Telegram 小游戏
- 💾 数据存储：自动保存用户信息到 Supabase
- 🔗 URL 参数传递：将用户信息传递给游戏
- 📝 详细日志：完整的操作日志记录
- 🛡️ 错误处理：数据库失败时继续执行

### 2. 数据库模块 (database_simple.py)

简化的数据库操作模块，使用 HTTP 请求与 Supabase 交互。

**主要功能：**
- 用户数据保存和查询
- 重复用户检查
- 获取所有用户列表
- 错误处理和日志记录

**数据库表结构：**
- `users` 表：存储用户ID和创建时间
- `scores` 表：存储用户分数和游戏数据
- 支持行级安全策略 (RLS)
- 自动处理重复用户
- 分数查询和更新功能

### 3. 分数 API 服务器 (score_api.py)

基于 Flask 的 RESTful API 服务器，处理游戏分数操作。

**主要功能：**
- 📊 查询用户分数：`GET /api/score/{user_id}`
- 💾 更新用户分数：`POST /api/score/{user_id}`
- 🔍 健康检查：`GET /api/health`
- 📝 详细日志记录
- 🛡️ 错误处理

### 4. 网页小游戏 (index.html)

响应式点击计分游戏，支持用户信息显示和分数持久化。

**游戏特性：**
- 🎯 点击计分：简单的点击按钮增加分数
- 👤 用户信息显示：显示从 Telegram 传递的用户信息
- 💾 分数持久化：自动保存和加载用户分数
- 📱 响应式设计：适配各种设备
- 🎨 现代界面：简洁美观的设计
- ⏳ 加载状态：显示分数保存进度

### 5. Telegram 客户端 (client.py)

基于 Telethon 库的 Telegram 客户端，用于测试和开发。

**主要功能：**
- 连接 Telegram 服务器
- 获取用户信息
- 发送消息测试
- 获取聊天列表

## 🛠️ 快速开始

### 1. 安装依赖

```bash
# 安装所有依赖
pip install -r requirements.txt

# 使用国内镜像源（推荐）
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### 2. 配置项目

复制并编辑配置文件：
```bash
# 编辑 config.py 文件
# 填入你的 Telegram API 信息、机器人 Token 和 Supabase 配置
```

### 3. 设置数据库

在 Supabase 控制台中执行 `database_schema.sql` 中的 SQL 语句创建表结构。

### 4. 启动分数 API 服务器

```bash
python score_api.py
```

### 5. 运行机器人

```bash
python bot.py
```

## 📦 依赖说明

- `python-telegram-bot`: Telegram 机器人库
- `flask`: Web API 框架（用于分数 API 服务器）
- `httpx`: HTTP 客户端库（用于 Supabase 交互）
- `telethon`: Telegram 客户端库（可选，用于测试）

## ⚙️ 详细配置

### 1. Telegram 机器人设置

1. 在 Telegram 中找到 [@BotFather](https://t.me/botfather)
2. 发送 `/newbot` 创建新机器人
3. 获取机器人 Token
4. 发送 `/newgame` 创建新游戏
5. 设置游戏名称和描述
6. 获取游戏短名称
7. 在 `config.py` 中配置：
   ```python
   BOT_TOKEN = "你的机器人Token"
   GAME_SHORT_NAME = "你的游戏短名称"
   GAME_URL = "你的游戏部署地址"
   ```

### 2. Supabase 数据库设置

1. 在 [Supabase](https://supabase.com) 中创建新项目
2. 在 SQL 编辑器中执行 `database_schema.sql` 中的 SQL 语句
3. 获取项目的 URL 和 API Key
4. 在 `config.py` 中配置：
   ```python
   SUPABASE_URL = "你的Supabase项目URL"
   SUPABASE_KEY = "你的Supabase API Key"
   ```

### 3. 游戏部署

1. 将 `index.html` 上传到静态网站托管服务（推荐 Netlify、Vercel）
2. 确保使用 HTTPS 协议
3. 在 `config.py` 中更新 `GAME_URL`

## 🎯 工作流程

1. **用户发送 `/start`** → 机器人发送欢迎消息
2. **用户发送 `/game`** → 机器人发送游戏按钮
3. **用户点击游戏按钮** → 触发游戏回调处理
4. **记录用户信息** → 保存到 Supabase 数据库
5. **构建游戏URL** → 包含用户信息参数
6. **用户开始游戏** → 在网页中显示用户信息
7. **加载用户分数** → 从数据库查询用户历史分数
8. **用户点击计分** → 实时更新分数并保存到数据库

## 📝 注意事项

1. **API 密钥安全**：不要将真实的 API 密钥提交到公共仓库
2. **HTTPS 要求**：Telegram 游戏必须使用 HTTPS 协议
3. **数据库权限**：确保 Supabase RLS 策略允许匿名用户插入数据
4. **网络连接**：如果遇到连接问题，可能需要配置代理

## 🐛 常见问题

### 数据库连接问题
- 检查 Supabase URL 和 API Key 是否正确
- 确认数据库表已创建
- 检查 RLS 策略设置

### 机器人无响应
- 检查 BOT_TOKEN 是否正确
- 确认机器人已启动
- 查看日志输出

### 游戏无法加载
- 确认游戏 URL 使用 HTTPS
- 检查游戏页面是否正常访问
- 验证游戏短名称是否正确

## 📄 许可证

本项目仅供学习和研究使用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！
