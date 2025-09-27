# -*- coding: utf-8 -*-
"""
主程序 - SQL Copilot 自助式数据报表开发工具
"""

import argparse
import os
import sys
from typing import List

from config import config
from utils import read_file_content, split_queries, save_results_to_excel, ensure_directory
from sql_generator import batch_generate_sql, SQLGeneratorFactory
from sql_evaluator import evaluate_sql_results

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='SQL Copilot - 自助式数据报表开发工具')
    parser.add_argument('--mode', choices=['generate', 'evaluate', 'full'], default='full',
                       help='运行模式: generate(仅生成SQL), evaluate(仅评测), full(完整流程)')
    parser.add_argument('--model', choices=['qwen_turbo', 'qwen_coder', 'local_qwen'], 
                       default='qwen_turbo', help='使用的模型类型')
    parser.add_argument('--input', type=str, help='输入文件路径')
    parser.add_argument('--output', type=str, help='输出文件路径')
    parser.add_argument('--qa-file', type=str, default=config.qa_list_2_file, 
                       help='查询问题文件路径')
    parser.add_argument('--table-desc', type=str, default=config.table_description_file,
                       help='数据表描述文件路径')
    
    args = parser.parse_args()
    
    # 确保输出目录存在
    config.ensure_output_dir()
    
    print("=" * 60)
    print("SQL Copilot - 自助式数据报表开发工具")
    print("=" * 60)
    
    if args.mode in ['generate', 'full']:
        print(f"\n开始生成SQL查询，使用模型: {args.model}")
        generate_sql(args)
    
    if args.mode in ['evaluate', 'full']:
        print(f"\n开始评测SQL查询结果")
        evaluate_sql(args)

def generate_sql(args):
    """生成SQL查询"""
    try:
        # 读取数据表描述
        table_description = read_file_content(args.table_desc)
        if not table_description:
            print(f"无法读取数据表描述文件: {args.table_desc}")
            return
        
        # 读取查询问题
        qa_content = read_file_content(args.qa_file)
        if not qa_content:
            print(f"无法读取查询问题文件: {args.qa_file}")
            return
        
        queries = split_queries(qa_content)
        print(f"读取到 {len(queries)} 个查询问题")
        
        # 设置输出文件
        output_file = args.output or f"{config.output_dir}/sql_result_{args.model}.xlsx"
        
        # 批量生成SQL
        results = batch_generate_sql(
            queries=queries,
            generator_type=args.model,
            table_description=table_description,
            output_file=output_file
        )
        
        print(f"\nSQL生成完成！结果已保存到: {output_file}")
        
        # 显示统计信息
        total_time = sum(result['time'] for result in results)
        avg_time = total_time / len(results) if results else 0
        
        print(f"总耗时: {total_time:.2f}秒")
        print(f"平均耗时: {avg_time:.2f}秒/查询")
        
    except Exception as e:
        print(f"生成SQL时出错: {e}")
        import traceback
        traceback.print_exc()

def evaluate_sql(args):
    """评测SQL查询"""
    try:
        # 确定输入文件
        input_file = args.input or f"{config.output_dir}/sql_result_{args.model}.xlsx"
        
        if not os.path.exists(input_file):
            print(f"输入文件不存在: {input_file}")
            print("请先运行生成模式或指定正确的输入文件")
            return
        
        # 设置输出文件
        output_file = args.output or input_file
        
        # 执行评测
        result_df = evaluate_sql_results(
            input_file=input_file,
            output_file=output_file
        )
        
        if not result_df.empty:
            print(f"\n评测完成！结果已保存到: {output_file}")
        
    except Exception as e:
        print(f"评测SQL时出错: {e}")
        import traceback
        traceback.print_exc()

def interactive_mode():
    """交互式模式"""
    print("\n进入交互式模式")
    print("输入 'help' 查看帮助，输入 'quit' 退出")
    
    # 选择模型
    print("\n请选择模型:")
    print("1. qwen_turbo (推荐)")
    print("2. qwen_coder")
    print("3. local_qwen (需要本地模型)")
    
    model_choice = input("请输入选择 (1-3): ").strip()
    model_map = {'1': 'qwen_turbo', '2': 'qwen_coder', '3': 'local_qwen'}
    model = model_map.get(model_choice, 'qwen_turbo')
    
    # 创建生成器
    try:
        generator = SQLGeneratorFactory.create_generator(model)
        print(f"已选择模型: {model}")
    except Exception as e:
        print(f"创建生成器失败: {e}")
        return
    
    # 读取数据表描述
    table_description = read_file_content(config.table_description_file)
    if not table_description:
        print("无法读取数据表描述文件")
        return
    
    while True:
        query = input("\n请输入查询问题 (或输入 'quit' 退出): ").strip()
        
        if query.lower() == 'quit':
            break
        elif query.lower() == 'help':
            print_help()
            continue
        elif not query:
            continue
        
        try:
            sql, use_time = generator.generate_sql(query, table_description)
            print(f"\n生成的SQL (耗时: {use_time:.2f}秒):")
            print("-" * 50)
            print(sql)
            print("-" * 50)
            
            # 询问是否执行SQL
            execute = input("\n是否执行此SQL查询? (y/n): ").strip().lower()
            if execute == 'y':
                from sql_evaluator import SQLEvaluator
                evaluator = SQLEvaluator()
                result = evaluator.evaluate_single_sql(sql)
                
                if result['success']:
                    print("\n执行结果:")
                    print(result['result_content'])
                else:
                    print(f"\n执行失败: {result['result_content']}")
        
        except Exception as e:
            print(f"生成SQL时出错: {e}")

def print_help():
    """打印帮助信息"""
    help_text = """
SQL Copilot 使用帮助:

1. 命令行模式:
   python main.py --mode generate --model qwen_turbo
   python main.py --mode evaluate --input result.xlsx
   python main.py --mode full --model qwen_coder

2. 交互式模式:
   python main.py --interactive

3. 支持的模型:
   - qwen_turbo: 通用对话模型，适合复杂查询
   - qwen_coder: 专业代码生成模型，SQL更准确
   - local_qwen: 本地部署模型，需要预先下载

4. 查询示例:
   - "查询所有客户的姓名和电话"
   - "统计每种保险类型的平均保费"
   - "找出保费最高的前10个客户"

5. 配置文件:
   - config.py: 修改API密钥和数据库连接
   - 数据文件: insurance/data/ 目录下
    """
    print(help_text)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 没有参数时进入交互式模式
        interactive_mode()
    elif '--interactive' in sys.argv:
        interactive_mode()
    else:
        main()
