# -*- coding: utf-8 -*-
"""
简化的数据库操作模块
使用直接的HTTP请求与Supabase交互，避免依赖问题
"""

import httpx
import logging
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY, DATABASE_CONFIG

# 初始化日志
logger = logging.getLogger(__name__)

class SimpleDatabaseManager:
    """简化的数据库管理器"""
    
    def __init__(self):
        """初始化数据库连接"""
        self.base_url = f"{SUPABASE_URL}/rest/v1"
        self.headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
        logger.info("✅ 简化数据库管理器初始化成功")
    
    def save_user(self, user_data):
        """
        保存用户ID到数据库
        
        Args:
            user_data (dict): 用户数据字典，只需要包含 id
        
        Returns:
            bool: 保存是否成功
        """
        try:
            user_id = user_data.get('id')
            if not user_id:
                logger.error("❌ 用户ID不能为空")
                return False
            
            # 检查用户是否已存在
            existing_user = self.get_user_by_id(user_id)
            
            if existing_user:
                logger.info(f"✅ 用户已存在: {user_id}")
                return True
            else:
                # 只保存用户ID和时间戳
                now = datetime.now()
                user_record = {
                    'userID': user_id,
                    'created_at': now.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                # 发送POST请求插入数据
                response = httpx.post(
                    f"{self.base_url}/{DATABASE_CONFIG['users_table']}",
                    headers=self.headers,
                    json=user_record,
                    timeout=10
                )
                
                if response.status_code in [200, 201]:
                    logger.info(f"✅ 新用户已保存: {user_id}")
                    return True
                else:
                    logger.error(f"❌ 保存用户失败: {response.status_code} - {response.text}")
                    return False
            
        except Exception as e:
            logger.error(f"❌ 保存用户数据失败: {e}")
            return False
    
    def get_user_by_id(self, user_id):
        """
        根据用户ID获取用户信息
        
        Args:
            user_id (int): 用户ID
        
        Returns:
            dict: 用户信息，如果不存在返回 None
        """
        try:
            # 发送GET请求查询用户
            response = httpx.get(
                f"{self.base_url}/{DATABASE_CONFIG['users_table']}",
                headers=self.headers,
                params={'userID': f'eq.{user_id}', 'select': '*'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    logger.info(f"📋 找到用户: {user_id}")
                    return data[0]
                else:
                    logger.info(f"📋 用户不存在: {user_id}")
                    return None
            else:
                logger.error(f"❌ 查询用户失败: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"❌ 查询用户失败: {e}")
            return None
    
    def get_all_users(self):
        """
        获取所有用户列表
        
        Returns:
            list: 用户列表
        """
        try:
            response = httpx.get(
                f"{self.base_url}/{DATABASE_CONFIG['users_table']}",
                headers=self.headers,
                params={'select': '*'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                logger.info(f"📋 获取到 {len(data)} 个用户")
                return data
            else:
                logger.error(f"❌ 获取用户列表失败: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"❌ 获取用户列表失败: {e}")
            return []
    
    def get_user_score(self, user_id):
        """
        获取用户当前分数
        
        Args:
            user_id (int): 用户ID
        
        Returns:
            int: 用户分数，如果不存在返回 0
        """
        try:
            response = httpx.get(
                f"{self.base_url}/{DATABASE_CONFIG['scores_table']}",
                headers=self.headers,
                params={'user_id': f'eq.{user_id}', 'select': '*', 'order': 'created_at.desc', 'limit': '1'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data:
                    score = data[0].get('score', 0)
                    logger.info(f"📊 用户 {user_id} 当前分数: {score}")
                    return score
                else:
                    logger.info(f"📊 用户 {user_id} 没有分数记录，返回 0")
                    return 0
            else:
                logger.error(f"❌ 查询用户分数失败: {response.status_code} - {response.text}")
                return 0
        except Exception as e:
            logger.error(f"❌ 查询用户分数失败: {e}")
            return 0
    
    def update_user_score(self, user_id, score):
        """
        更新用户分数
        
        Args:
            user_id (int): 用户ID
            score (int): 新分数
        
        Returns:
            bool: 更新是否成功
        """
        try:
            score_record = {
                'user_id': user_id,
                'score': score,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            response = httpx.post(
                f"{self.base_url}/{DATABASE_CONFIG['scores_table']}",
                headers=self.headers,
                json=score_record,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"✅ 用户 {user_id} 分数已更新为: {score}")
                return True
            else:
                logger.error(f"❌ 更新用户分数失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 更新用户分数失败: {e}")
            return False

# 创建全局数据库管理器实例
db_manager = SimpleDatabaseManager()
