// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 检查用户是否已经登录
    checkAuth();
    
    // 绑定表单提交事件
    document.getElementById('login').addEventListener('submit', handleLogin);
    document.getElementById('register').addEventListener('submit', handleRegister);
});

// 检查用户认证状态
async function checkAuth() {
    try {
        const { data: { user } } = await supabase.auth.getUser();
        if (user) {
            showUserInfo(user);
        }
    } catch (error) {
        console.log('检查认证状态时出错:', error);
    }
}

// 处理登录
async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    // 验证用户名格式
    if (!validateUsername(username)) {
        showMessage('用户名格式不正确，请输入6-12位数字或字母', 'error');
        return;
    }
    
    try {
        // 将用户名转换为邮箱格式（添加@example.com后缀）
        const email = username + '@example.com';
        const { data, error } = await supabase.auth.signInWithPassword({
            email: email,
            password: password
        });
        
        if (error) {
            showMessage('登录失败: ' + error.message, 'error');
        } else {
            showMessage('登录成功！', 'success');
            showUserInfo(data.user);
        }
    } catch (error) {
        showMessage('登录时发生错误: ' + error.message, 'error');
    }
}

// 处理注册
async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('registerUsername').value;
    const password = document.getElementById('registerPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    // 验证用户名格式
    if (!validateUsername(username)) {
        showMessage('用户名格式不正确，请输入6-12位数字或字母', 'error');
        return;
    }
    
    // 验证密码是否一致
    if (password !== confirmPassword) {
        showMessage('两次输入的密码不一致', 'error');
        return;
    }
    
    // 验证密码长度
    if (password.length < 6) {
        showMessage('密码长度至少为6位', 'error');
        return;
    }
    
    try {
        // 将用户名转换为邮箱格式（添加@example.com后缀）
        const email = username + '@example.com';
        const { data, error } = await supabase.auth.signUp({
            email: email,
            password: password,
            options: {
                emailRedirectTo: undefined // 禁用邮箱验证
            }
        });
        
        if (error) {
            showMessage('注册失败: ' + error.message, 'error');
        } else {
            showMessage('注册成功！可以直接登录', 'success');
            showLogin(); // 切换到登录表单
        }
    } catch (error) {
        showMessage('注册时发生错误: ' + error.message, 'error');
    }
}

// 显示用户信息
function showUserInfo(user) {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('userInfo').style.display = 'block';
    // 从邮箱中提取用户名（去掉@example.com后缀）
    const username = user.email.replace('@example.com', '');
    document.getElementById('userUsername').textContent = username;
}

// 退出登录
async function logout() {
    try {
        const { error } = await supabase.auth.signOut();
        if (error) {
            showMessage('退出登录失败: ' + error.message, 'error');
        } else {
            showMessage('已退出登录', 'success');
            showLogin();
        }
    } catch (error) {
        showMessage('退出登录时发生错误: ' + error.message, 'error');
    }
}

// 显示注册表单
function showRegister() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'block';
    document.getElementById('userInfo').style.display = 'none';
    
    // 清空表单
    document.getElementById('register').reset();
}

// 显示登录表单
function showLogin() {
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('userInfo').style.display = 'none';
    
    // 清空表单
    document.getElementById('login').reset();
}

// 验证用户名格式（6-12位数字或字母）
function validateUsername(username) {
    const regex = /^[a-zA-Z0-9]{6,12}$/;
    return regex.test(username);
}

// 显示消息提示
function showMessage(message, type) {
    const messageEl = document.getElementById('message');
    messageEl.textContent = message;
    messageEl.className = `message ${type} show`;
    
    // 3秒后自动隐藏
    setTimeout(() => {
        messageEl.classList.remove('show');
    }, 3000);
}
