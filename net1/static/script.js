// 当前用户状态
let currentUser = null;
let currentCounter = 0;
let currentCoins = 1000;

// 页面加载时检查登录状态
document.addEventListener('DOMContentLoaded', function() {
    checkLoginStatus();
});

// 检查登录状态
async function checkLoginStatus() {
    // 检查本地存储中是否有用户信息
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
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
        // 调用Python API注册
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message);
            showLogin();
        } else {
            alert(result.message);
        }
        
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
        // 调用Python API登录
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentUser = result.user;
            // 保存用户信息到本地存储
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            await loadUserData();
            showMainPage();
        } else {
            alert(result.message);
        }
        
    } catch (error) {
        alert('登录失败：' + error.message);
    }
});

// 加载用户数据
async function loadUserData() {
    try {
        const response = await fetch('/api/get_user_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUser.id
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentCounter = result.counter;
            currentCoins = result.coins;
            document.getElementById('counter').textContent = currentCounter;
            document.getElementById('coins').textContent = currentCoins;
        } else {
            console.error('加载用户数据失败：', result.message);
        }
        
    } catch (error) {
        console.error('加载用户数据失败：', error);
    }
}

// 增加计数器
async function incrementCounter() {
    currentCounter++;
    document.getElementById('counter').textContent = currentCounter;
    
    // 保存到数据库
    try {
        const response = await fetch('/api/update_counter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUser.id,
                counter: currentCounter
            })
        });
        
        const result = await response.json();
        
        if (!result.success) {
            console.error('保存计数器失败：', result.message);
        }
    } catch (error) {
        console.error('保存计数器失败：', error);
    }
}

// BET游戏
async function playBetGame() {
    if (currentCoins < 100) {
        alert('金币不足，需要100金币才能游戏！');
        return;
    }
    
    try {
        const response = await fetch('/api/bet_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUser.id,
                current_coins: currentCoins
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentCoins = result.new_coins;
            document.getElementById('coins').textContent = currentCoins;
            document.getElementById('gameResult').textContent = result.message;
            
            // 根据结果显示不同颜色
            if (result.is_odd) {
                document.getElementById('gameResult').style.color = '#28a745';
            } else {
                document.getElementById('gameResult').style.color = '#dc3545';
            }
        } else {
            alert(result.message);
        }
        
    } catch (error) {
        alert('游戏失败：' + error.message);
    }
}

// 退出登录
async function logout() {
    try {
        // 清除本地存储
        localStorage.removeItem('currentUser');
        currentUser = null;
        currentCounter = 0;
        currentCoins = 1000;
        showLogin();
    } catch (error) {
        console.error('退出登录失败：', error);
    }
}
