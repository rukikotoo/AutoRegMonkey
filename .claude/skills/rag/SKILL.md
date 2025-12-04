---
name: rag
description: 查询计量经济学RAG知识库。当用户输入以"rag："开头时，LLM会使用Python查询Bruce Hansen计量经济学教材的RAG数据库，返回相关文档内容。
---

# RAG 查询技能

此技能允许代理查询计量经济学RAG知识库，该知识库基于Bruce Hansen的计量经济学教材构建。

## 概述

- **数据库类型**: FAISS 向量数据库
- **数据库位置**: `D:\AutoRegMonkey\database\rag_db\`

## 使用方法

当用户输入以"rag："开头时，执行以下步骤：

1. **提取查询问题**: 识别"rag："后面的查询文本
2. **调用Python脚本**: 使用用户的Python环境执行RAG查询
3. **返回结果**: 将查询结果格式化后呈现给用户

### Python 脚本模板

强制Python I/O用UTF-8：sys.stdout.reconfigure(encoding='utf-8') 和 sys.stderr.reconfigure(encoding='utf-8')
使用以下Python代码进行查询：

```python
import sys
sys.path.append(r"D:\AutoRegMonkey\database")
from rag_query import EconometricsRAG
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 初始化RAG
rag = EconometricsRAG()

# 执行查询（从用户输入中提取的问题）
results = rag.query("用户的问题", n_results=5)

# 处理并输出结果
output_lines = []
for i, r in enumerate(results):
    chunk = r['chunk']
    score = r['score']
    output_lines.append(f"【结果 {i+1}】 - 来源: 第{chunk['page']}页, 相似度: {score:.4f}")
    output_lines.append(f"{chunk['text'][:500]}{'...' if len(chunk['text']) > 500 else ''}")
    output_lines.append("---")

print("\n".join(output_lines))
```

### 通过Bash执行

在Bash工具中使用以下命令：

```bash
"C:\Users\29165\anaconda3\python.exe" -c "
import sys
sys.path.append(r'D:\AutoRegMonkey\database')
from rag_query import EconometricsRAG

rag = EconometricsRAG()
results = rag.query('用户的问题', n_results=5)

for i, r in enumerate(results):
    chunk = r['chunk']
    score = r['score']
    print(f'【结果 {i+1}】 - 来源: 第{chunk[\"page\"]}页, 相似度: {score:.4f}')
    print(f'{chunk[\"text\"][:500]}{\"...\" if len(chunk[\"text\"]) > 500 else \"\"}')
    print('---')
"
```

注意：将`'用户的问题'`替换为实际查询文本。

## 查询示例

### 示例1: 基础查询
**用户输入**: `rag：什么是OLS回归？`

**执行代码**:
```bash
"C:\Users\29165\anaconda3\python.exe" -c "
import sys
sys.path.append(r'D:\AutoRegMonkey\database')
from rag_query import EconometricsRAG

rag = EconometricsRAG()
results = rag.query('什么是OLS回归？', n_results=5)

for i, r in enumerate(results):
    chunk = r['chunk']
    score = r['score']
    print(f'【结果 {i+1}】 - 来源: 第{chunk[\"page\"]}页, 相似度: {score:.4f}')
    print(f'{chunk[\"text\"][:500]}{\"...\" if len(chunk[\"text\"]) > 500 else \"\"}')
    print('---')
"
```

### 示例2: 获取LLM上下文
如果需要在其他分析中使用RAG上下文，可以使用`get_context()`方法：

```python
context = rag.get_context("heteroskedasticity robust standard errors", n_results=3)
print(context)
```

### 示例3: 按页码搜索
```python
chunks = rag.search_by_page(page_number=100)
for chunk in chunks:
    print(f"第{chunk['page']}页: {chunk['text'][:200]}")
```

## 文件组织

- **原始数据**: `D:\AutoRegMonkey\database\rag_db\` (FAISS索引和文档块)
- **查询接口**: `D:\AutoRegMonkey\database\rag_query.py`
- **API文档**: `D:\AutoRegMonkey\database\RAG_API_说明.md`

## 注意事项

1. **Python环境**: 使用用户的Anaconda Python环境 (`C:\Users\29165\anaconda3\python.exe`)
2. **路径引用**: 确保正确引用包含空格或特殊字符的路径
3. **结果数量**: 默认返回5个最相关结果，可根据需要调整`n_results`参数
4. **输出格式**: 保持输出整洁，限制文本长度以便阅读
5. **错误处理**: 如果查询失败，检查数据库路径和Python模块导入

## 高级用法

### 与其他技能结合
此技能可与`autoregmonkey`技能结合使用，在计量经济学分析过程中实时查询相关知识：

1. 用户输入以"autoregmonkey："开头的计量任务
2. 在分析过程中，使用RAG技能查询相关计量理论
3. 将查询结果融入分析报告

### 批量查询
对于复杂问题，可执行多次查询以获取全面信息：

```python
queries = ["OLS regression", "heteroskedasticity", "instrumental variables"]
for q in queries:
    results = rag.query(q, n_results=2)
    # 处理结果...
```

## 故障排除

- **导入错误**: 确保`sys.path.append(r'D:\AutoRegMonkey\database')`已添加
- **模块未找到**: 检查`rag_query.py`文件是否存在
- **数据库错误**: 确认`D:\AutoRegMonkey\database\rag_db\`目录包含必要文件
- **编码问题**: 使用`encoding='utf-8'`处理中英文文本