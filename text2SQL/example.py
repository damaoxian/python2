# -*- coding: utf-8 -*-
"""
SQL Copilot 使用示例
"""

from sql_generator import SQLGeneratorFactory, batch_generate_sql
from sql_evaluator import SQLEvaluator, evaluate_sql_results
from utils import read_file_content, split_queries
from config import config

def example_single_query():
    """单个查询示例"""
    print("=" * 50)
    print("单个查询示例")
    print("=" * 50)
    
    # 创建生成器
    generator = SQLGeneratorFactory.create_generator("qwen_turbo")
    
    # 读取数据表描述
    table_description = read_file_content(config.table_description_file)
    
    # 单个查询
    query = "查询所有客户的姓名和联系电话"
    print(f"查询问题: {query}")
    
    # 生成SQL
    sql, use_time = generator.generate_sql(query, table_description)
    print(f"生成的SQL (耗时: {use_time:.2f}秒):")
    print(sql)
    
    return sql

def example_batch_queries():
    """批量查询示例"""
    print("\n" + "=" * 50)
    print("批量查询示例")
    print("=" * 50)
    
    # 读取查询问题
    qa_content = read_file_content(config.qa_list_2_file)
    queries = split_queries(qa_content)
    
    # 只处理前3个查询作为示例
    sample_queries = queries[:3]
    print(f"处理 {len(sample_queries)} 个查询问题")
    
    # 读取数据表描述
    table_description = read_file_content(config.table_description_file)
    
    # 批量生成SQL
    results = batch_generate_sql(
        queries=sample_queries,
        generator_type="qwen_turbo",
        table_description=table_description,
        output_file=f"{config.output_dir}/example_results.xlsx"
    )
    
    print(f"\n批量生成完成，结果保存到: {config.output_dir}/example_results.xlsx")
    return results

def example_sql_evaluation():
    """SQL评测示例"""
    print("\n" + "=" * 50)
    print("SQL评测示例")
    print("=" * 50)
    
    # 创建评测器
    evaluator = SQLEvaluator()
    
    # 测试数据库连接
    if not evaluator.test_connection():
        print("数据库连接失败，跳过评测示例")
        return
    
    # 评测单个SQL
    sql = "SELECT Name, PhoneNumber FROM CustomerInfo LIMIT 5"
    print(f"评测SQL: {sql}")
    
    result = evaluator.evaluate_single_sql(sql)
    print(f"执行结果: {'成功' if result['success'] else '失败'}")
    if result['success']:
        print("查询结果:")
        print(result['result_content'])
    else:
        print(f"错误信息: {result['result_content']}")

def example_different_models():
    """不同模型对比示例"""
    print("\n" + "=" * 50)
    print("不同模型对比示例")
    print("=" * 50)
    
    query = "查询每种保险类型的保险金额的平均值、最大值和最小值"
    table_description = read_file_content(config.table_description_file)
    
    models = ["qwen_turbo", "qwen_coder"]
    
    for model in models:
        print(f"\n使用模型: {model}")
        try:
            generator = SQLGeneratorFactory.create_generator(model)
            sql, use_time = generator.generate_sql(query, table_description)
            print(f"生成的SQL (耗时: {use_time:.2f}秒):")
            print(sql[:200] + "..." if len(sql) > 200 else sql)
        except Exception as e:
            print(f"模型 {model} 生成失败: {e}")

def main():
    """主函数"""
    print("SQL Copilot 使用示例")
    print("请确保已正确配置API密钥和数据库连接")
    
    try:
        # 单个查询示例
        example_single_query()
        
        # 批量查询示例
        example_batch_queries()
        
        # SQL评测示例
        example_sql_evaluation()
        
        # 不同模型对比示例
        example_different_models()
        
        print("\n" + "=" * 50)
        print("所有示例运行完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"运行示例时出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
