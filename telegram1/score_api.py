# -*- coding: utf-8 -*-
"""
分数 API 服务器
处理游戏分数的查询和更新
"""

from flask import Flask, request, jsonify
import logging
from database_simple import db_manager

# 配置日志
logging.basicConfig(level=logging.INFO, encoding='utf-8')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/api/score/<int:user_id>', methods=['GET'])
def get_score(user_id):
    """获取用户分数"""
    try:
        logger.info(f"📊 查询用户 {user_id} 的分数")
        score = db_manager.get_user_score(user_id)
        return jsonify({
            'success': True,
            'user_id': user_id,
            'score': score
        })
    except Exception as e:
        logger.error(f"❌ 查询分数失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/score/<int:user_id>', methods=['POST'])
def update_score(user_id):
    """更新用户分数"""
    try:
        data = request.get_json()
        score = data.get('score', 0)
        
        logger.info(f"📊 更新用户 {user_id} 的分数为: {score}")
        success = db_manager.update_user_score(user_id, score)
        
        if success:
            return jsonify({
                'success': True,
                'user_id': user_id,
                'score': score
            })
        else:
            return jsonify({
                'success': False,
                'error': '更新分数失败'
            }), 500
            
    except Exception as e:
        logger.error(f"❌ 更新分数失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'message': '分数 API 服务正常运行'
    })

if __name__ == '__main__':
    logger.info("🚀 分数 API 服务器启动")
    app.run(host='0.0.0.0', port=5000, debug=True)
