# -*- coding: utf-8 -*-
"""
配置测试脚本 - 验证新的配置信息是否正确
"""

from config import config
from sql_evaluator import SQLEvaluator
from sql_generator import SQLGeneratorFactory

def test_database_config():
    """测试数据库配置"""
    print("=" * 50)
    print("测试数据库配置")
    print("=" * 50)
    
    print(f"数据库类型: MySQL")
    print(f"主机: {config.db_host}")
    print(f"端口: {config.db_port}")
    print(f"用户名: {config.db_user}")
    print(f"数据库名: {config.db_name}")
    print(f"字符集: {config.db_charset}")
    print(f"连接URL: {config.get_database_url()}")
    
    # 测试数据库连接
    print("\n测试数据库连接...")
    try:
        evaluator = SQLEvaluator()
        if evaluator.test_connection():
            print("✅ 数据库连接成功！")
        else:
            print("❌ 数据库连接失败！")
    except Exception as e:
        print(f"❌ 数据库连接测试出错: {e}")

def test_llm_config():
    """测试LLM配置"""
    print("\n" + "=" * 50)
    print("测试LLM配置")
    print("=" * 50)
    
    print(f"模型类型: {config.model_type}")
    print(f"API密钥: {config.dashscope_api_key[:20]}...")
    print(f"默认模型: {config.qwen_turbo_model}")
    print(f"温度参数: {config.temperature}")
    print(f"最大令牌数: {config.max_tokens}")
    
    # 测试模型连接
    print("\n测试模型连接...")
    try:
        generator = SQLGeneratorFactory.create_generator("qwen_turbo")
        print("✅ 模型初始化成功！")
        
        # 测试简单查询
        test_query = "SELECT 1 as test"
        sql, use_time = generator.generate_sql(test_query, "测试表")
        print(f"✅ 模型响应测试成功！耗时: {use_time:.2f}秒")
        
    except Exception as e:
        print(f"❌ 模型连接测试出错: {e}")

def test_file_paths():
    """测试文件路径配置"""
    print("\n" + "=" * 50)
    print("测试文件路径配置")
    print("=" * 50)
    
    import os
    
    paths_to_check = [
        ("数据目录", config.data_dir),
        ("表描述文件", config.table_description_file),
        ("SQL创建文件", config.create_sql_file),
        ("查询问题文件1", config.qa_list_1_file),
        ("查询问题文件2", config.qa_list_2_file),
        ("输出目录", config.output_dir)
    ]
    
    for name, path in paths_to_check:
        if os.path.exists(path):
            print(f"✅ {name}: {path}")
        else:
            print(f"❌ {name}: {path} (文件不存在)")

def main():
    """主函数"""
    print("SQL Copilot 配置测试")
    print("=" * 60)
    
    # 测试数据库配置
    test_database_config()
    
    # 测试LLM配置
    test_llm_config()
    
    # 测试文件路径
    test_file_paths()
    
    print("\n" + "=" * 60)
    print("配置测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()
