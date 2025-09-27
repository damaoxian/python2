# -*- coding: utf-8 -*-
"""
SQL生成器模块 - 使用不同的大语言模型生成SQL查询
"""

import time
import dashscope
from dashscope.api_entities.dashscope_response import Role
from typing import List, Dict, Tuple
from config import config
from utils import extract_sql_code, clean_query, print_progress

class SQLGenerator:
    """SQL生成器基类"""
    
    def __init__(self):
        self.api_key = config.dashscope_api_key
        dashscope.api_key = self.api_key
    
    def get_response(self, messages: List[Dict[str, str]]):
        """获取模型响应（需要在子类中实现）"""
        raise NotImplementedError
    
    def generate_sql(self, query: str, table_description: str = None) -> Tuple[str, float]:
        """
        生成SQL查询
        
        Args:
            query: 自然语言查询
            table_description: 数据表描述
            
        Returns:
            (生成的SQL, 耗时)
        """
        start_time = time.time()
        
        try:
            response = self._get_sql_response(query, table_description)
            sql = extract_sql_code(response.output.choices[0].message.content)
            use_time = time.time() - start_time
            
            return sql, use_time
        except Exception as e:
            print(f"生成SQL时出错: {e}")
            return "", time.time() - start_time
    
    def _get_sql_response(self, query: str, table_description: str = None):
        """获取SQL响应（需要在子类中实现）"""
        raise NotImplementedError

class QwenTurboGenerator(SQLGenerator):
    """使用Qwen-turbo模型生成SQL"""
    
    def __init__(self):
        super().__init__()
        self.model = config.qwen_turbo_model
    
    def get_response(self, messages: List[Dict[str, str]]):
        """获取Qwen-turbo模型响应"""
        response = dashscope.Generation.call(
            model=self.model,
            messages=messages,
            result_format='message',
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
        return response
    
    def _get_sql_response(self, query: str, table_description: str = None):
        """获取SQL响应"""
        sys_prompt = """我正在编写SQL，以下是数据库中的数据表和字段，请思考：哪些数据表和字段是该SQL需要的，然后编写对应的SQL，如果有多个查询语句，请尝试合并为一个。编写SQL请采用```sql
        """
        
        user_prompt = f"""{table_description}
=====
我要写的SQL是：{query}
请思考：哪些数据表和字段是该SQL需要的，然后编写对应的SQL
"""
        
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self.get_response(messages)

class QwenCoderGenerator(SQLGenerator):
    """使用Qwen-coder-plus模型生成SQL"""
    
    def __init__(self):
        super().__init__()
        self.model = config.qwen_coder_model
    
    def get_response(self, messages: List[Dict[str, str]]):
        """获取Qwen-coder-plus模型响应"""
        response = dashscope.Generation.call(
            model=self.model,
            messages=messages,
            result_format='message',
            temperature=config.temperature,
            max_tokens=config.max_tokens
        )
        return response
    
    def _get_sql_response(self, query: str, table_description: str = None):
        """获取SQL响应"""
        sys_prompt = """我正在编写SQL，以下是数据库中的数据表和字段，请思考：哪些数据表和字段是该SQL需要的，然后编写对应的SQL，如果有多个查询语句，请尝试合并为一个。编写SQL请采用```sql
        """
        
        user_prompt = f"""-- language: SQL
### Question: {query}
### Input: {table_description}
### Response:
Here is the SQL query I have generated to answer the question `{query}`:
```sql
"""
        
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self.get_response(messages)

class LocalQwenGenerator(SQLGenerator):
    """使用本地Qwen模型生成SQL"""
    
    def __init__(self, model_path: str = None):
        super().__init__()
        self.model_path = model_path or config.local_model_path
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """加载本地模型"""
        try:
            from modelscope import AutoModelForCausalLM, AutoTokenizer
            
            print(f"正在加载本地模型: {self.model_path}")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                torch_dtype="auto",
                device_map="auto"
            )
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            print("本地模型加载完成")
        except Exception as e:
            print(f"加载本地模型失败: {e}")
            print("请确保已安装modelscope和torch，并且模型路径正确")
    
    def get_response(self, messages: List[Dict[str, str]]):
        """获取本地模型响应"""
        if self.model is None or self.tokenizer is None:
            raise Exception("本地模型未正确加载")
        
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=512
        )
        
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # 模拟API响应格式
        class MockResponse:
            def __init__(self, content):
                self.output = MockOutput(content)
        
        class MockOutput:
            def __init__(self, content):
                self.choices = [MockChoice(content)]
        
        class MockChoice:
            def __init__(self, content):
                self.message = MockMessage(content)
        
        class MockMessage:
            def __init__(self, content):
                self.content = content
        
        return MockResponse(response)
    
    def _get_sql_response(self, query: str, table_description: str = None):
        """获取SQL响应"""
        sys_prompt = """你是一个专业的SQL查询助手。请根据用户的问题和数据库表结构，生成准确的SQL查询语句。"""
        
        user_prompt = f"""数据库表结构：
{table_description}

用户问题：{query}

请生成对应的SQL查询语句，使用```sql标记包围代码。"""
        
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return self.get_response(messages)

class SQLGeneratorFactory:
    """SQL生成器工厂类"""
    
    @staticmethod
    def create_generator(generator_type: str = "qwen_turbo", **kwargs) -> SQLGenerator:
        """
        创建SQL生成器
        
        Args:
            generator_type: 生成器类型 ("qwen_turbo", "qwen_coder", "local_qwen")
            **kwargs: 额外参数
            
        Returns:
            SQL生成器实例
        """
        if generator_type == "qwen_turbo":
            return QwenTurboGenerator()
        elif generator_type == "qwen_coder":
            return QwenCoderGenerator()
        elif generator_type == "local_qwen":
            model_path = kwargs.get('model_path', config.local_model_path)
            return LocalQwenGenerator(model_path)
        else:
            raise ValueError(f"不支持的生成器类型: {generator_type}")

def batch_generate_sql(queries: List[str], generator_type: str = "qwen_turbo", 
                      table_description: str = None, output_file: str = None) -> List[Dict]:
    """
    批量生成SQL查询
    
    Args:
        queries: 查询列表
        generator_type: 生成器类型
        table_description: 数据表描述
        output_file: 输出文件路径
        
    Returns:
        生成结果列表
    """
    generator = SQLGeneratorFactory.create_generator(generator_type)
    results = []
    
    print(f"开始批量生成SQL，使用模型: {generator_type}")
    print(f"总共 {len(queries)} 个查询")
    
    for i, query in enumerate(queries):
        print_progress(i + 1, len(queries), query[:50] + "..." if len(query) > 50 else query)
        
        sql, use_time = generator.generate_sql(query, table_description)
        
        result = {
            'QA': query,
            'SQL': sql,
            'time': round(use_time, 2)
        }
        results.append(result)
        
        print(f"SQL生成时间: {use_time:.2f}秒")
        print(f"生成的SQL: {sql[:100]}{'...' if len(sql) > 100 else ''}")
        print("-" * 50)
    
    if output_file:
        from utils import save_results_to_excel
        save_results_to_excel(results, output_file)
    
    return results
