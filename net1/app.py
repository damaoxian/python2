from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import random
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# Supabase配置
SUPABASE_URL = 'https://itvcxveomumsrqsfkorv.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Iml0dmN4dmVvbXVtc3Jxc2Zrb3J2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTg5NTgwMTcsImV4cCI6MjA3NDUzNDAxN30.2URyy6xksVjp7PB4WGlJoUYST7mnNHTd36AjzQyceIY'

# 初始化Supabase客户端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/')
def index():
    """返回主页"""
    return app.send_static_file('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # 验证输入
        if not username or len(username) < 3:
            return jsonify({'success': False, 'message': '账号必须是3位以上的字母或数字'})
        
        if not password or not password.isdigit() or len(password) != 6:
            return jsonify({'success': False, 'message': '密码必须是6位数字'})
        
        # 检查用户名是否已存在
        result = supabase.table('users').select('username').eq('username', username).execute()
        if result.data:
            return jsonify({'success': False, 'message': '用户名已存在'})
        
        # 插入新用户
        result = supabase.table('users').insert({
            'username': username,
            'password': password,
            'counter': 0,
            'coins': 1000
        }).execute()
        
        if result.data:
            return jsonify({'success': True, 'message': '注册成功！请登录'})
        else:
            return jsonify({'success': False, 'message': '注册失败'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'注册失败：{str(e)}'})

@app.route('/api/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # 查询用户
        result = supabase.table('users').select('*').eq('username', username).eq('password', password).execute()
        
        if result.data:
            user = result.data[0]
            return jsonify({
                'success': True, 
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'counter': user['counter'],
                    'coins': user['coins']
                }
            })
        else:
            return jsonify({'success': False, 'message': '用户名或密码错误'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'登录失败：{str(e)}'})

@app.route('/api/update_counter', methods=['POST'])
def update_counter():
    """更新计数器"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        counter = data.get('counter')
        
        result = supabase.table('users').update({'counter': counter}).eq('id', user_id).execute()
        
        if result.data:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': '更新失败'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'更新失败：{str(e)}'})

@app.route('/api/bet_game', methods=['POST'])
def bet_game():
    """BET游戏逻辑"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        current_coins = data.get('current_coins')
        
        # 检查金币是否足够
        if current_coins < 100:
            return jsonify({'success': False, 'message': '金币不足，需要100金币才能游戏'})
        
        # 扣除100金币
        new_coins = current_coins - 100
        
        # 生成0-10000的随机数
        random_number = random.randint(0, 10000)
        
        # 判断单双数
        is_odd = random_number % 2 == 1
        
        if is_odd:
            # 单数，增加200金币
            new_coins += 200
            message = f"🎉 恭喜！随机数 {random_number} 是单数，获得200金币！"
        else:
            # 双数，不增加金币
            message = f"😔 随机数 {random_number} 是双数，没有获得金币"
        
        # 更新数据库
        result = supabase.table('users').update({'coins': new_coins}).eq('id', user_id).execute()
        
        if result.data:
            return jsonify({
                'success': True,
                'new_coins': new_coins,
                'random_number': random_number,
                'is_odd': is_odd,
                'message': message
            })
        else:
            return jsonify({'success': False, 'message': '更新失败'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'游戏失败：{str(e)}'})

@app.route('/api/get_user_data', methods=['POST'])
def get_user_data():
    """获取用户数据"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        result = supabase.table('users').select('counter, coins').eq('id', user_id).execute()
        
        if result.data:
            user_data = result.data[0]
            return jsonify({
                'success': True,
                'counter': user_data['counter'],
                'coins': user_data['coins']
            })
        else:
            return jsonify({'success': False, 'message': '获取用户数据失败'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取用户数据失败：{str(e)}'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
