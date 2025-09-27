// Supabase配置
const SUPABASE_URL = 'https://itvcxveomumsrqsfkorv.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml0dmN4dmVvbXVtc3Jxc2Zrb3J2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5NTgwMTcsImV4cCI6MjA3NDUzNDAxN30.2URyy6xksVjp7PB4WGlJoUYST7mnNHTd36AjzQyceIY';

// 初始化Supabase客户端
const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// 当前用户状态
let currentUser = null;
let currentCounter = 0;

// 页面加载时检查登录状态
document.addEventListener('DOMContentLoaded', function() {
    checkLoginStatus();
});

// 检查登录状态
async function checkLoginStatus() {
    const { data: { session } } = await supabase.auth.getSession();
    if (session) {
        currentUser = session.user;
        await loadUserData();
        showMainPage();
    } else {
        showLogin();
    }
}

// 显示注册页面
function showRegister() {
    document.getElementById('registerForm').classList.remove('hidden');
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('mainPage').classList.add('hidden');
    clearErrors();
}

// 显示登录页面
function showLogin() {
    document.getElementById('registerForm').classList.add('hidden');
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('mainPage').classList.add('hidden');
    clearErrors();
}

// 显示主页
function showMainPage() {
    document.getElementById('registerForm').classList.add('hidden');
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('mainPage').classList.remove('hidden');
}

// 清除错误信息
function clearErrors() {
    const errorElements = document.querySelectorAll('.error');
    errorElements.forEach(element => {
        element.textContent = '';
    });
}

// 验证账号格式
function validateUsername(username) {
    return /^[a-zA-Z0-9]{3,}$/.test(username);
}

// 验证密码格式
function validatePassword(password) {
    return /^\d{6}$/.test(password);
}

// 注册处理
document.getElementById('register').addEventListener('submit', async function(e) {
    e.preventDefault();
    clearErrors();
    
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;
    
    // 验证输入
    if (!validateUsername(username)) {
        document.getElementById('regUsernameError').textContent = '账号必须是3位以上的字母或数字';
        return;
    }
    
    if (!validatePassword(password)) {
        document.getElementById('regPasswordError').textContent = '密码必须是6位数字';
        return;
    }
    
    try {
        // 注册用户
        const { data, error } = await supabase.auth.signUp({
            email: username + '@example.com', // 使用假邮箱
            password: password
        });
        
        if (error) {
            alert('注册失败：' + error.message);
            return;
        }
        
        // 在用户表中插入用户信息
        const { error: insertError } = await supabase
            .from('users')
            .insert([
                { 
                    id: data.user.id, 
                    username: username, 
                    counter: 0 
                }
            ]);
        
        if (insertError) {
            console.error('插入用户数据失败：', insertError);
        }
        
        alert('注册成功！请登录');
        showLogin();
        
    } catch (error) {
        alert('注册失败：' + error.message);
    }
});

// 登录处理
document.getElementById('login').addEventListener('submit', async function(e) {
    e.preventDefault();
    clearErrors();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        // 登录用户
        const { data, error } = await supabase.auth.signInWithPassword({
            email: username + '@example.com',
            password: password
        });
        
        if (error) {
            alert('登录失败：' + error.message);
            return;
        }
        
        currentUser = data.user;
        await loadUserData();
        showMainPage();
        
    } catch (error) {
        alert('登录失败：' + error.message);
    }
});

// 加载用户数据
async function loadUserData() {
    try {
        const { data, error } = await supabase
            .from('users')
            .select('counter')
            .eq('id', currentUser.id)
            .single();
        
        if (error) {
            console.error('加载用户数据失败：', error);
            currentCounter = 0;
        } else {
            currentCounter = data.counter || 0;
        }
        
        document.getElementById('counter').textContent = currentCounter;
        
    } catch (error) {
        console.error('加载用户数据失败：', error);
        currentCounter = 0;
        document.getElementById('counter').textContent = currentCounter;
    }
}

// 增加计数器
async function incrementCounter() {
    currentCounter++;
    document.getElementById('counter').textContent = currentCounter;
    
    // 保存到数据库
    try {
        const { error } = await supabase
            .from('users')
            .update({ counter: currentCounter })
            .eq('id', currentUser.id);
        
        if (error) {
            console.error('保存计数器失败：', error);
        }
    } catch (error) {
        console.error('保存计数器失败：', error);
    }
}

// 退出登录
async function logout() {
    try {
        await supabase.auth.signOut();
        currentUser = null;
        currentCounter = 0;
        showLogin();
    } catch (error) {
        console.error('退出登录失败：', error);
    }
}
