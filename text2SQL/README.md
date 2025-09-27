# SQL Copilot - 自助式数据报表开发

## 项目简介

这是一个基于大语言模型的Text2SQL项目，旨在实现自然语言到SQL查询的自动转换，特别针对保险行业的数据分析场景。项目使用多种大语言模型（包括Qwen系列模型）来生成SQL查询语句，并提供完整的评测体系。

## 项目特色

- 🤖 **多模型支持**：支持Qwen-turbo、Qwen-coder-plus等多种大语言模型
- 📊 **保险行业数据**：专门针对保险业务场景设计的数据表结构
- 🔍 **智能SQL生成**：将自然语言查询自动转换为SQL语句
- 📈 **结果评测**：提供完整的SQL执行结果评测和可视化
- 🛠️ **易于使用**：基于Jupyter Notebook的交互式开发环境

## 项目结构

```
CASE-SQL Copilot/
├── README.md                           # 项目说明文档
├── qwen-coder1.ipynb                   # Qwen2.5-Coder模型测试
├── codegeex-1.ipynb                    # CodeGeeX模型测试
└── insurance/                          # 保险数据模块
    ├── requirements.txt                # Python依赖包
    ├── data/                          # 数据文件目录
    │   ├── create_sql.txt             # 数据库表结构定义
    │   ├── 数据表字段说明-精简1.txt    # 数据表字段说明
    │   ├── CustomerInfo.xlsx          # 客户信息数据
    │   ├── PolicyInfo.xlsx            # 保单信息数据
    │   ├── ClaimInfo.xlsx             # 理赔信息数据
    │   ├── BeneficiaryInfo.xlsx       # 受益人信息数据
    │   ├── AgentInfo.xlsx             # 代理人信息数据
    │   ├── ProductInfo.xlsx            # 产品信息数据
    │   └── EmployeeInfo.xlsx           # 员工信息数据
    ├── qa_list-1.txt                  # 查询问题列表1
    ├── qa_list-2.txt                  # 查询问题列表2
    ├── SQL查询-Chat.ipynb             # 使用Qwen-turbo进行SQL查询
    ├── SQL查询-Coder.ipynb            # 使用Qwen-coder-plus进行SQL查询
    └── SQL结果评测.ipynb               # SQL执行结果评测
```

## 数据表结构

项目包含7个核心数据表，模拟真实的保险业务场景：

### 1. 客户信息表（CustomerInfo）
- 客户基本信息：姓名、性别、出生日期、身份证号等
- 联系方式：地址、电话、邮箱
- 业务信息：客户类型、来源、状态等

### 2. 保单信息表（PolicyInfo）
- 保单基本信息：保单号、客户ID、产品ID
- 保单状态：生效、终止、暂停等
- 受益人信息：受益人姓名、关系
- 保费信息：支付状态、支付日期、支付方式

### 3. 理赔信息表（ClaimInfo）
- 理赔基本信息：理赔号、保单号、理赔日期
- 理赔详情：类型、金额、状态、描述
- 审核信息：审核人、审核日期、支付信息

### 4. 受益人信息表（BeneficiaryInfo）
- 受益人基本信息：姓名、性别、出生日期
- 联系信息：地址、电话、邮箱

### 5. 代理人信息表（AgentInfo）
- 代理人基本信息：姓名、性别、出生日期
- 职业信息：证书号、执照信息、佣金结构

### 6. 保险产品信息表（ProductInfo）
- 产品基本信息：产品名称、类型、保险金额范围
- 产品特性：保险期限、保费、缴费频率
- 业务规则：投保年龄限制、理赔流程

### 7. 员工信息表（EmployeeInfo）
- 员工基本信息：姓名、性别、出生日期
- 工作信息：职位、部门、工资、上级主管

## 功能特性

### 1. 自然语言查询转换
- 支持中文自然语言查询
- 自动识别查询意图和所需数据表
- 生成标准SQL语句

### 2. 多模型对比
- **Qwen-turbo**：通用对话模型，适合复杂查询理解
- **Qwen-coder-plus**：专业代码生成模型，SQL生成更准确
- **Qwen2.5-Coder**：最新代码模型，支持本地部署

### 3. 查询示例
项目包含丰富的查询示例，涵盖：
- 统计分析：平均值、最大值、最小值计算
- 趋势分析：时间序列数据趋势
- 关联查询：多表关联分析
- 业务分析：客户行为、代理人业绩等

### 4. 结果评测
- SQL语法检查
- 执行结果验证
- 结果格式化和可视化
- 错误诊断和修复建议

## 快速开始

### 环境要求
- Python 3.8+
- Jupyter Notebook
- MySQL数据库（可选，用于结果验证）

### 安装依赖

```bash
# 进入项目目录
cd insurance

# 安装依赖包
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 配置API密钥

在使用模型API之前，需要配置相应的API密钥：

```python
# 在notebook中设置API密钥
dashscope.api_key = "your-api-key-here"
```

### 运行示例

1. **基础查询测试**
   ```python
   # 打开 SQL查询-Chat.ipynb 或 SQL查询-Coder.ipynb
   # 运行示例查询
   query = "查询每种保险类型的保险金额的平均值、最大值和最小值"
   sql_result = get_sql(query, table_description)
   ```

2. **结果评测**
   ```python
   # 打开 SQL结果评测.ipynb
   # 执行SQL并获取结果
   isok, result = get_markdown_result(session, sql)
   ```

## 使用说明

### 1. 查询问题格式
- 使用中文描述查询需求
- 明确指定需要的数据维度
- 可以包含统计函数要求（平均值、总和等）

### 2. 模型选择建议
- **简单查询**：推荐使用Qwen-turbo
- **复杂SQL**：推荐使用Qwen-coder-plus
- **本地部署**：推荐使用Qwen2.5-Coder

### 3. 结果优化
- 检查生成的SQL语法
- 验证查询结果的合理性
- 根据业务需求调整查询逻辑

## 技术栈

- **大语言模型**：Qwen系列、CodeGeeX
- **数据处理**：Pandas、SQLAlchemy
- **数据库**：MySQL
- **开发环境**：Jupyter Notebook
- **API服务**：DashScope、OpenAI兼容接口

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

## 许可证

本项目采用 MIT 许可证。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件

---

**注意**：本项目仅用于学习和研究目的，请遵守相关法律法规和API使用条款。
