# SQL Copilot - 项目结构说明

## 📁 核心文件结构

```
CASE-SQL Copilot/
├── 📄 核心程序文件
│   ├── config.py              # 配置文件 - API密钥、数据库连接等
│   ├── main.py                # 主程序 - 命令行接口
│   ├── run.py                 # 启动脚本 - 用户友好的菜单界面
│   ├── sql_generator.py       # SQL生成模块 - 支持多种LLM模型
│   ├── sql_evaluator.py       # SQL评测模块 - 执行和验证SQL
│   ├── utils.py               # 工具函数 - 通用功能函数
│   └── requirements.txt       # 依赖包列表
│
├── 📚 文档和示例
│   ├── README.md              # 项目说明文档
│   ├── example.py             # 使用示例脚本
│   └── test_config.py         # 配置测试脚本
│
└── 📊 数据文件
    └── insurance/
        ├── data/              # 保险数据文件
        │   ├── *.xlsx         # Excel数据文件
        │   ├── create_sql.txt # 数据库表结构
        │   └── 数据表字段说明-精简1.txt
        └── qa_list-*.txt      # 查询问题文件
```

## 🎯 文件功能说明

### 核心程序文件
- **`config.py`**: 统一管理所有配置信息
- **`main.py`**: 提供命令行接口，支持多种运行模式
- **`run.py`**: 提供友好的菜单界面，适合新手使用
- **`sql_generator.py`**: 支持多种大语言模型的SQL生成
- **`sql_evaluator.py`**: 执行SQL查询并评测结果
- **`utils.py`**: 通用工具函数，提高代码复用性

### 文档和示例
- **`README.md`**: 项目完整说明文档
- **`example.py`**: 详细的使用示例，展示各种功能
- **`test_config.py`**: 配置测试工具，验证环境设置

### 数据文件
- **`insurance/data/`**: 保险业务数据文件
- **`insurance/qa_list-*.txt`**: 预设的查询问题

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 2. 配置设置
编辑 `config.py` 文件，设置API密钥和数据库连接

### 3. 运行程序
```bash
# 方式1: 使用启动脚本（推荐）
python run.py

# 方式2: 直接运行主程序
python main.py --interactive

# 方式3: 运行示例
python example.py
```

## 📋 文件依赖关系

```
main.py
├── config.py
├── sql_generator.py
├── sql_evaluator.py
└── utils.py

run.py
└── main.py

example.py
├── config.py
├── sql_generator.py
├── sql_evaluator.py
└── utils.py

test_config.py
├── config.py
├── sql_evaluator.py
└── sql_generator.py
```

## 🔧 维护说明

- **添加新功能**: 在对应模块中添加，保持模块化设计
- **修改配置**: 只需修改 `config.py` 文件
- **添加新模型**: 在 `sql_generator.py` 中扩展
- **添加新评测**: 在 `sql_evaluator.py` 中扩展

## 📝 注意事项

1. 所有Python文件都使用UTF-8编码
2. 配置文件支持环境变量覆盖
3. 输出目录会在运行时自动创建
4. 数据文件路径在配置文件中统一管理
