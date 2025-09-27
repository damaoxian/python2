# -*- coding: utf-8 -*-
"""
配置文件 - 管理API密钥和数据库连接信息
"""

import os
from typing import Optional

class Config:
    """配置类，管理所有配置信息"""
    
    def __init__(self):
        # API配置
        self.dashscope_api_key = os.getenv('DASHSCOPE_API_KEY', 'sk-01b44ce9c5fa4aaaa636f59a655d0723')
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        
        # 数据库配置
        self.db_host = os.getenv('DB_HOST', '206.233.249.253')
        self.db_user = os.getenv('DB_USER', 'gamestore')
        self.db_password = os.getenv('DB_PASSWORD', 'gamestore')
        self.db_port = int(os.getenv('DB_PORT', '33066'))
        self.db_name = os.getenv('DB_NAME', 'gamestore')
        self.db_charset = os.getenv('DB_CHARSET', 'utf8mb4')
        
        # 模型配置
        self.model_type = os.getenv('MODEL_TYPE', 'qwen')
        self.qwen_turbo_model = 'qwen-turbo'
        self.qwen_coder_model = 'qwen-coder-plus'
        self.local_model_path = '/root/autodl-tmp/models/Qwen/Qwen2___5-Coder-7B-Instruct'
        
        # LLM参数配置
        self.temperature = float(os.getenv('TEMPERATURE', '0.1'))
        self.max_tokens = int(os.getenv('MAX_TOKENS', '1000'))
        
        # 文件路径配置
        self.data_dir = './insurance/data'
        self.table_description_file = f'{self.data_dir}/数据表字段说明-精简1.txt'
        self.create_sql_file = f'{self.data_dir}/create_sql.txt'
        self.qa_list_1_file = './insurance/qa_list-1.txt'
        self.qa_list_2_file = './insurance/qa_list-2.txt'
        
        # 输出配置
        self.output_dir = './output'
        self.sql_result_file = f'{self.output_dir}/sql_result.xlsx'
        
    def get_database_url(self) -> str:
        """获取数据库连接URL"""
        return f'mysql+mysqlconnector://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}?charset={self.db_charset}'
    
    def ensure_output_dir(self):
        """确保输出目录存在"""
        os.makedirs(self.output_dir, exist_ok=True)

# 全局配置实例
config = Config()
