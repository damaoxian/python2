# 简单注册登录系统

这是一个使用 Supabase 作为后端，部署到 Netlify 的简单注册登录网页。

## 功能特性

- ✅ 用户注册（用户名格式：6-12位数字或字母）
- ✅ 用户登录
- ✅ 用户退出登录
- ✅ 响应式设计
- ✅ 美观的界面

## 技术栈

- **前端**: HTML, CSS, JavaScript
- **后端**: Supabase (认证服务)
- **部署**: Netlify

## 快速开始

### 1. 设置 Supabase

1. 访问 [Supabase](https://supabase.com) 并创建新项目
2. 在项目设置中找到 API 设置
3. 复制项目 URL 和 anon key
4. 在 `config.js` 文件中替换以下内容：
   ```javascript
   const SUPABASE_URL = 'YOUR_SUPABASE_URL';
   const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';
   ```
5. **重要**：在 Supabase 项目设置中，进入 Authentication > Settings，将 "Enable email confirmations" 设置为关闭，以简化注册流程

### 2. 本地运行

1. 克隆或下载项目文件
2. 用浏览器打开 `index.html` 文件
3. 或者使用本地服务器：
   ```bash
   # 使用 Python
   python -m http.server 8000
   
   # 或使用 Node.js
   npx serve .
   ```

### 3. 部署到 Netlify

#### 方法一：拖拽部署
1. 将整个项目文件夹拖拽到 [Netlify](https://netlify.com) 的部署区域
2. 等待部署完成

#### 方法二：Git 部署
1. 将代码推送到 GitHub/GitLab
2. 在 Netlify 中连接你的仓库
3. 设置构建命令为空（因为是静态网站）
4. 发布目录设置为根目录

## 项目结构

```
nettest/
├── index.html          # 主页面
├── style.css          # 样式文件
├── script.js          # JavaScript 逻辑
├── config.js          # Supabase 配置
├── netlify.toml       # Netlify 部署配置
└── README.md          # 说明文档
```

## 使用说明

1. **注册新用户**：
   - 点击"立即注册"链接
   - 填写用户名（6-12位数字或字母）和密码
   - 点击注册按钮
   - 注册成功后可以直接登录

2. **登录**：
   - 输入注册时的用户名和密码
   - 点击登录按钮

3. **退出登录**：
   - 登录成功后点击"退出登录"按钮

## 注意事项

⚠️ **安全提醒**：此项目仅用于学习和测试，不包含任何安全措施，请勿在生产环境中使用。

## 常见问题

### Q: 注册后无法登录？
A: 确保在 Supabase 项目设置中关闭了邮箱验证功能（Authentication > Settings > Enable email confirmations 设为关闭）。

### Q: 登录失败？
A: 确保用户名和密码正确，并且 Supabase 配置正确。

### Q: 用户名格式要求？
A: 用户名必须是6-12位的数字或字母组合，不能包含特殊字符。

### Q: 部署后无法正常工作？
A: 检查 `config.js` 中的 Supabase URL 和 API Key 是否正确配置。

## 许可证

MIT License
