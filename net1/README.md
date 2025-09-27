# 简单计数器项目

这是一个简单的网页应用，包含用户注册、登录和计数器功能。

## 功能特性

- **用户注册**：输入账号（3位以上字母或数字）和密码（6位数字）
- **用户登录**：验证账号密码，登录后跳转到主页
- **计数器**：点击按钮增加数字，数据保存到数据库
- **数据持久化**：用户下次登录时读取之前的计数

## 技术栈

- **前端**：HTML + CSS + JavaScript
- **后端**：Supabase
- **数据库**：Supabase PostgreSQL
- **部署**：Netlify

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

### 3. 部署到Netlify

1. 将代码推送到GitHub仓库
2. 在Netlify中连接GitHub仓库
3. 设置构建命令：留空（静态网站）
4. 设置发布目录：`/`（根目录）
5. 部署

## 项目结构

```
├── index.html          # 主页面
├── script.js           # JavaScript逻辑
├── netlify.toml        # Netlify配置
└── README.md           # 项目说明
```

## 使用说明

1. 访问部署的网站
2. 点击"没有账号？点击注册"进行注册
3. 输入账号（3位以上字母或数字）和密码（6位数字）
4. 注册成功后登录
5. 在主页点击"点击增加"按钮增加计数
6. 退出登录后再次登录，计数会保持

## 注意事项

- 本项目仅用于学习和测试
- 未考虑安全问题和异常处理
- 代码尽可能简化，便于理解
