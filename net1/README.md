# 简单计数器项目

这是一个简单的网页应用，包含用户注册、登录和计数器功能。

## 功能特性

- **用户注册**：输入账号（3位以上字母或数字）和密码（6位数字）
- **用户登录**：验证账号密码，登录后跳转到主页
- **计数器**：点击按钮增加数字，数据保存到数据库
- **数据持久化**：用户下次登录时读取之前的计数

## 技术栈

- **前端**：HTML + CSS + JavaScript
- **后端**：Python Flask
- **数据库**：Supabase PostgreSQL
- **部署**：Fly.io

## 设置步骤

### 1. 设置Supabase

1. 访问 [Supabase](https://supabase.com) 创建新项目
2. 在SQL编辑器中执行以下SQL创建用户表：

```sql
-- 创建用户表
CREATE TABLE users (
  id UUID REFERENCES auth.users(id) PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  counter INTEGER DEFAULT 0,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 启用行级安全策略
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- 创建策略：用户只能访问自己的数据
CREATE POLICY "Users can view own data" ON users
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own data" ON users
  FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own data" ON users
  FOR INSERT WITH CHECK (auth.uid() = id);
```

3. 在项目设置中获取：
   - Project URL
   - Anon public key

### 2. 配置前端

1. 编辑 `script.js` 文件
2. 替换以下配置：
   ```javascript
   const SUPABASE_URL = 'YOUR_SUPABASE_URL';
   const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';
   ```

### 3. 部署到Fly.io

#### 方法一：使用部署脚本（推荐）

1. **安装Fly.io CLI**：
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **运行部署脚本**：
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

#### 方法二：手动部署

1. **安装Fly.io CLI**：
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **登录Fly.io**：
   ```bash
   flyctl auth login
   ```

3. **创建应用**：
   ```bash
   flyctl apps create net1
   ```

4. **部署应用**：
   ```bash
   flyctl deploy
   ```

5. **访问应用**：
   部署完成后，访问 `https://net1.fly.dev`

## 项目结构

```
├── app.py              # Flask后端主程序
├── requirements.txt    # Python依赖包
├── fly.toml           # Fly.io配置文件
├── Dockerfile         # Docker配置
├── deploy.sh          # 部署脚本
├── static/
│   ├── index.html     # 前端页面
│   └── script.js      # 前端JavaScript
└── README.md          # 项目说明
```

## 使用说明

1. 访问部署的网站 `https://net1.fly.dev`
2. 点击"没有账号？点击注册"进行注册
3. 输入账号（3位以上字母或数字）和密码（6位数字）
4. 注册成功后登录
5. 在主页可以：
   - 点击"点击增加"按钮增加计数
   - 玩BET游戏：花费100金币，随机数单数获得200金币
6. 退出登录后再次登录，计数和金币都会保持

## BET游戏规则

- **初始金币**：每个用户注册时获得1000金币
- **游戏成本**：每次BET花费100金币
- **随机数生成**：0-10000之间的随机数
- **奖励机制**：
  - 单数：获得200金币（净赚100金币）
  - 双数：无奖励（净亏100金币）
- **数据持久化**：所有金币变更都保存到数据库

## 注意事项

- 本项目仅用于学习和测试
- 未考虑安全问题和异常处理
- 代码尽可能简化，便于理解
