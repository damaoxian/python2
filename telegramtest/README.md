# Telegram 游戏机器人项目

这是一个简化的 Telegram 游戏机器人项目，支持游戏跳转和用户信息传递。

## 📁 项目结构

```
telegram1/
├── bot.py                 # Telegram 机器人主程序
├── client.py              # Telegram 客户端连接脚本
├── config.py              # 项目配置文件
├── requirements.txt       # Python 依赖包
└── README.md              # 项目说明文档
```

## 🚀 核心功能

### 1. Telegram 游戏机器人 (bot.py)

基于 python-telegram-bot 库的简化游戏机器人，支持游戏跳转和用户信息传递。

**主要功能：**
- `/start` 命令：发送欢迎消息
- `/game` 命令：启动小游戏
- 游戏回调处理：记录用户信息并传递到游戏
- 详细日志记录：便于调试和监控

**核心特性：**
- 🎮 游戏集成：支持 Telegram 小游戏
- 🔐 initData 模式：使用 Telegram 官方推荐的 initData 方式传递用户信息
- 📝 详细日志：完整的操作日志记录
- 👤 用户信息：通过 initData 安全传递用户信息

### 2. Telegram 客户端 (client.py)

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

### 2. 游戏配置

1. 在 `config.py` 中配置游戏 URL：
   ```python
   GAME_URL = "https://your-game-url.com"
   ```
2. 确保游戏 URL 使用 HTTPS 协议
3. 游戏页面可以接收用户信息参数

## 🎯 工作流程

1. **用户发送 `/start`** → 机器人发送欢迎消息
2. **用户发送 `/game`** → 机器人发送游戏按钮
3. **用户点击游戏按钮** → 触发游戏回调处理
4. **记录用户信息** → 记录到日志
5. **返回游戏URL** → 使用 initData 模式，不直接传递用户信息
6. **用户开始游戏** → Telegram 自动通过 initData 传递用户信息到游戏

## 📝 注意事项

1. **API 密钥安全**：不要将真实的 API 密钥提交到公共仓库
2. **HTTPS 要求**：Telegram 游戏必须使用 HTTPS 协议
3. **网络连接**：如果遇到连接问题，可能需要配置代理

## 🐛 常见问题

### 机器人无响应
- 检查 BOT_TOKEN 是否正确
- 确认机器人已启动
- 查看日志输出

### 游戏无法加载
- 确认游戏 URL 使用 HTTPS
- 检查游戏页面是否正常访问
- 验证游戏短名称是否正确

### 用户信息传递问题
- 检查游戏页面是否能正确解析 initData
- 确认 initData 验证逻辑正确
- 验证时间戳是否在有效期内

## 🔐 initData 模式说明

### 什么是 initData？
initData 是 Telegram 官方推荐的安全方式，用于在 WebApp 和机器人之间传递用户信息。相比直接通过 URL 参数传递，initData 模式具有以下优势：

1. **安全性**：使用 HMAC-SHA256 签名验证，防止数据篡改
2. **时效性**：数据具有 24 小时的有效期
3. **完整性**：Telegram 自动处理用户信息的传递

### 在游戏页面中使用 initData

游戏页面可以通过以下方式获取用户信息：

```javascript
// 获取 initData
const initData = new URLSearchParams(window.location.search).get('tgWebAppData');

// 验证 initData（可选，但推荐）
// 使用机器人提供的验证函数验证数据完整性

// 解析用户信息
const urlParams = new URLSearchParams(initData);
const userData = JSON.parse(urlParams.get('user'));
```

### initData 验证

机器人提供了 `validate_init_data()` 函数来验证 initData 的有效性：

```python
# 验证 initData
is_valid = validate_init_data(init_data_string, bot_token)

# 解析用户信息
user_info = parse_init_data(init_data_string)
```

## 📄 许可证

本项目仅供学习和研究使用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！
