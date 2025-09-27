# -*- coding: utf-8 -*-
"""
工具函数模块 - 包含通用功能函数
"""

import re
import time
import pandas as pd
from typing import List, Tuple, Optional
import os

def extract_sql_code(response_content: str) -> str:
    """
    从模型响应中提取SQL代码
    
    Args:
        response_content: 模型响应内容
        
    Returns:
        提取的SQL代码
    """
    # 查找```sql和```之间的内容
    pattern = r'```sql(.*?)```'
    match = re.search(pattern, response_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        # 如果没有找到```sql标记，尝试查找任何```之间的内容
        pattern = r'```(.*?)```'
        match = re.search(pattern, response_content, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            # 如果没有找到任何代码块，返回整个响应
            return response_content

def read_file_content(file_path: str, encoding: str = 'utf-8') -> str:
    """
    读取文件内容
    
    Args:
        file_path: 文件路径
        encoding: 文件编码
        
    Returns:
        文件内容
    """
    try:
        with open(file_path, 'r', encoding=encoding) as file:
            return file.read()
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return ""
    except Exception as e:
        print(f"读取文件出错: {e}")
        return ""

def save_results_to_excel(data: List[dict], file_path: str) -> None:
    """
    保存结果到Excel文件
    
    Args:
        data: 数据列表
        file_path: 保存路径
    """
    try:
        df = pd.DataFrame(data)
        df.to_excel(file_path, index=False)
        print(f"结果已保存到: {file_path}")
    except Exception as e:
        print(f"保存Excel文件出错: {e}")

def format_time(seconds: float) -> str:
    """
    格式化时间显示
    
    Args:
        seconds: 秒数
        
    Returns:
        格式化的时间字符串
    """
    if seconds < 60:
        return f"{seconds:.2f}秒"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}分{secs:.2f}秒"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        return f"{hours}小时{minutes}分{secs:.2f}秒"

def clean_query(query: str) -> str:
    """
    清理查询字符串
    
    Args:
        query: 原始查询字符串
        
    Returns:
        清理后的查询字符串
    """
    return query.replace('\n', '').strip()

def split_queries(query_list: str, separator: str = '=====') -> List[str]:
    """
    分割查询列表
    
    Args:
        query_list: 查询列表字符串
        separator: 分隔符
        
    Returns:
        分割后的查询列表
    """
    return [clean_query(q) for q in query_list.split(separator) if clean_query(q)]

def validate_sql(sql: str) -> Tuple[bool, str]:
    """
    验证SQL语法（基础验证）
    
    Args:
        sql: SQL语句
        
    Returns:
        (是否有效, 错误信息)
    """
    if not sql or sql.strip() == '':
        return False, "SQL语句为空"
    
    # 基础关键字检查
    sql_upper = sql.upper().strip()
    if not any(keyword in sql_upper for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']):
        return False, "SQL语句缺少主要操作关键字"
    
    return True, ""

def print_progress(current: int, total: int, item: str = "") -> None:
    """
    打印进度信息
    
    Args:
        current: 当前进度
        total: 总数
        item: 当前处理的项目
    """
    percentage = (current / total) * 100
    print(f"[{current}/{total}] ({percentage:.1f}%) {item}")

def ensure_directory(directory: str) -> None:
    """
    确保目录存在
    
    Args:
        directory: 目录路径
    """
    os.makedirs(directory, exist_ok=True)
