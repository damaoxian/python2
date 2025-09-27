#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SQL Copilot 启动脚本
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """检查依赖包是否安装"""
    required_packages = [
        'dashscope', 'pandas', 'sqlalchemy', 'openai'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("缺少以下依赖包:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/")
        return False
    
    return True

def check_config():
    """检查配置文件"""
    config_file = Path("config.py")
    if not config_file.exists():
        print("配置文件 config.py 不存在")
        return False
    
    # 检查数据文件
    data_dir = Path("insurance/data")
    if not data_dir.exists():
        print("数据目录不存在，请确保项目结构完整")
        return False
    
    return True

def show_menu():
    """显示菜单"""
    print("\n" + "=" * 60)
    print("SQL Copilot - 自助式数据报表开发工具")
    print("=" * 60)
    print("1. 运行示例")
    print("2. 交互式查询")
    print("3. 批量生成SQL")
    print("4. 评测SQL结果")
    print("5. 查看帮助")
    print("6. 退出")
    print("=" * 60)

def run_example():
    """运行示例"""
    print("运行SQL Copilot示例...")
    try:
        subprocess.run([sys.executable, "example.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"运行示例失败: {e}")
    except KeyboardInterrupt:
        print("\n示例运行被中断")

def run_interactive():
    """运行交互式模式"""
    print("启动交互式模式...")
    try:
        subprocess.run([sys.executable, "main.py", "--interactive"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"启动交互式模式失败: {e}")
    except KeyboardInterrupt:
        print("\n交互式模式被中断")

def run_batch_generate():
    """批量生成SQL"""
    print("批量生成SQL...")
    print("请选择模型:")
    print("1. qwen_turbo (推荐)")
    print("2. qwen_coder")
    print("3. local_qwen (需要本地模型)")
    
    choice = input("请输入选择 (1-3): ").strip()
    model_map = {'1': 'qwen_turbo', '2': 'qwen_coder', '3': 'local_qwen'}
    model = model_map.get(choice, 'qwen_turbo')
    
    try:
        subprocess.run([
            sys.executable, "main.py", 
            "--mode", "generate", 
            "--model", model
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"批量生成失败: {e}")
    except KeyboardInterrupt:
        print("\n批量生成被中断")

def run_evaluation():
    """评测SQL结果"""
    print("评测SQL结果...")
    try:
        subprocess.run([
            sys.executable, "main.py", 
            "--mode", "evaluate"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"评测失败: {e}")
    except KeyboardInterrupt:
        print("\n评测被中断")

def show_help():
    """显示帮助信息"""
    help_text = """
SQL Copilot 使用帮助:

1. 环境准备:
   - 确保已安装Python 3.8+
   - 安装依赖: pip install -r requirements.txt
   - 配置API密钥和数据库连接

2. 配置文件 (config.py):
   - 修改API密钥: dashscope_api_key
   - 修改数据库连接信息
   - 修改文件路径配置

3. 使用方法:
   - 交互式模式: python main.py --interactive
   - 批量生成: python main.py --mode generate --model qwen_turbo
   - 评测结果: python main.py --mode evaluate
   - 完整流程: python main.py --mode full

4. 支持的模型:
   - qwen_turbo: 通用对话模型
   - qwen_coder: 专业代码生成模型
   - local_qwen: 本地部署模型

5. 数据文件:
   - insurance/data/: 数据文件目录
   - insurance/qa_list-*.txt: 查询问题文件
   - output/: 输出结果目录

6. 常见问题:
   - API密钥错误: 检查config.py中的API密钥
   - 数据库连接失败: 检查数据库配置和网络连接
   - 模型加载失败: 检查模型路径和依赖包
    """
    print(help_text)

def main():
    """主函数"""
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查配置
    if not check_config():
        return
    
    while True:
        show_menu()
        choice = input("请选择操作 (1-6): ").strip()
        
        if choice == '1':
            run_example()
        elif choice == '2':
            run_interactive()
        elif choice == '3':
            run_batch_generate()
        elif choice == '4':
            run_evaluation()
        elif choice == '5':
            show_help()
        elif choice == '6':
            print("感谢使用SQL Copilot！")
            break
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被中断，再见！")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        import traceback
        traceback.print_exc()
