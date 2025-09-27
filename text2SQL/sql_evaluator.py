# -*- coding: utf-8 -*-
"""
SQL评测模块 - 执行SQL查询并评测结果
"""

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import traceback
from typing import Tuple, List, Dict
from config import config
from utils import ensure_directory

class SQLEvaluator:
    """SQL评测器类"""
    
    def __init__(self, database_url: str = None):
        """
        初始化SQL评测器
        
        Args:
            database_url: 数据库连接URL
        """
        self.database_url = database_url or config.get_database_url()
        self.engine = None
        self._create_engine()
    
    def _create_engine(self):
        """创建数据库引擎"""
        try:
            self.engine = create_engine(self.database_url)
            print(f"数据库连接成功: {self.database_url}")
        except Exception as e:
            print(f"数据库连接失败: {e}")
            self.engine = None
    
    def get_session(self):
        """获取数据库会话"""
        if self.engine is None:
            raise Exception("数据库引擎未初始化")
        
        Session = sessionmaker(bind=self.engine)
        return Session()
    
    def execute_sql(self, sql: str) -> Tuple[bool, str, str]:
        """
        执行SQL查询
        
        Args:
            sql: SQL语句
            
        Returns:
            (是否成功, 结果类型, 结果内容)
        """
        if not sql or sql.strip() == '':
            return False, "error", "SQL语句为空"
        
        session = None
        try:
            session = self.get_session()
            
            # 如果有多个SQL语句，只执行第一个
            sqls = sql.split(';')
            sql = sqls[0].strip()
            
            if not sql:
                return False, "error", "SQL语句为空"
            
            # 执行SQL查询
            result = session.execute(text(sql))
            
            # 获取列名
            columns = result.keys()
            
            # 获取所有数据
            rows = result.fetchall()
            
            if not rows:
                return True, "empty", "查询结果为空"
            
            # 构建markdown表格
            markdown = self._build_markdown_table(columns, rows)
            return True, "success", markdown
            
        except Exception as e:
            error_msg = str(e)
            traceback_msg = traceback.format_exc()
            return False, "error", f'SQL执行错误: {error_msg}'
        finally:
            if session:
                session.close()
    
    def _build_markdown_table(self, columns: List[str], rows: List) -> str:
        """
        构建markdown格式的表格
        
        Args:
            columns: 列名列表
            rows: 数据行列表
            
        Returns:
            markdown格式的表格字符串
        """
        # 构建表头
        markdown = '| ' + ' | '.join(columns) + ' |\n'
        markdown += '| ' + ' | '.join(['---' for _ in columns]) + ' |\n'
        
        # 添加数据行
        for row in rows:
            markdown += '| ' + ' | '.join(str(cell) for cell in row) + ' |\n'
        
        return markdown
    
    def evaluate_sql_file(self, input_file: str, output_file: str = None) -> pd.DataFrame:
        """
        评测SQL文件中的查询
        
        Args:
            input_file: 输入文件路径（Excel格式）
            output_file: 输出文件路径
            
        Returns:
            评测结果DataFrame
        """
        try:
            # 读取输入文件
            df = pd.read_excel(input_file)
            print(f"读取到 {len(df)} 条SQL查询")
            
            # 添加评测列
            df['能否运行'] = ''
            df['执行结果'] = ''
            
            for index, row in df.iterrows():
                sql = row['SQL']
                print(f"评测第 {index + 1} 条SQL...")
                
                if pd.isna(sql) or str(sql).strip() == '':
                    df.loc[index, '能否运行'] = 'No 没有找到SQL'
                    df.loc[index, '执行结果'] = 'SQL为空'
                    continue
                
                # 执行SQL
                success, result_type, result_content = self.execute_sql(str(sql))
                
                if success:
                    df.loc[index, '能否运行'] = 'Yes'
                    df.loc[index, '执行结果'] = result_content
                else:
                    df.loc[index, '能否运行'] = f'No {result_content}'
                    df.loc[index, '执行结果'] = result_content
                
                print(f"执行结果: {'成功' if success else '失败'}")
                print("-" * 50)
            
            # 保存结果
            if output_file:
                df.to_excel(output_file, index=False)
                print(f"评测结果已保存到: {output_file}")
            else:
                # 默认保存到原文件
                df.to_excel(input_file, index=False)
                print(f"评测结果已保存到: {input_file}")
            
            return df
            
        except Exception as e:
            print(f"评测过程中出错: {e}")
            return pd.DataFrame()
    
    def evaluate_single_sql(self, sql: str) -> Dict:
        """
        评测单个SQL查询
        
        Args:
            sql: SQL语句
            
        Returns:
            评测结果字典
        """
        success, result_type, result_content = self.execute_sql(sql)
        
        return {
            'success': success,
            'result_type': result_type,
            'result_content': result_content,
            'sql': sql
        }
    
    def test_connection(self) -> bool:
        """
        测试数据库连接
        
        Returns:
            连接是否成功
        """
        try:
            session = self.get_session()
            session.execute(text("SELECT 1"))
            session.close()
            print("数据库连接测试成功")
            return True
        except Exception as e:
            print(f"数据库连接测试失败: {e}")
            return False

def evaluate_sql_results(input_file: str, output_file: str = None, database_url: str = None):
    """
    评测SQL结果的便捷函数
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
        database_url: 数据库连接URL
    """
    evaluator = SQLEvaluator(database_url)
    
    # 测试连接
    if not evaluator.test_connection():
        print("数据库连接失败，无法进行评测")
        return
    
    # 执行评测
    result_df = evaluator.evaluate_sql_file(input_file, output_file)
    
    # 统计结果
    if not result_df.empty:
        total_count = len(result_df)
        success_count = len(result_df[result_df['能否运行'] == 'Yes'])
        success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
        
        print(f"\n评测完成!")
        print(f"总查询数: {total_count}")
        print(f"成功执行: {success_count}")
        print(f"成功率: {success_rate:.1f}%")
    
    return result_df
