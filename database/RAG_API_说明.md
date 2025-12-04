# Econometrics RAG 数据库接口说明

## 数据库概述

- **数据来源**: `Econometrics_by_Bruce_Hansen.pdf` (Bruce Hansen 计量经济学教材)
- **数据库类型**: FAISS 向量数据库
- **嵌入模型**: `all-MiniLM-L6-v2` (384维向量)
- **文档块数量**: 3538 个
- **数据库位置**: `D:\AutoRegMonkey\database\rag_db\`

## 文件结构

```
D:\AutoRegMonkey\database\rag_db\
├── faiss_index.bin    # FAISS向量索引
├── metadata.pkl       # 元数据
└── chunks.json        # 文档块内容（含页码信息）
```

---

## Python 接口使用方法

### 1. 快速查询（推荐）

```python
import sys
sys.path.append(r"D:\AutoRegMonkey\database")
from rag_query import EconometricsRAG

# 初始化
rag = EconometricsRAG()

# 查询相关内容
results = rag.query("What is OLS regression?", n_results=5)

# 遍历结果
for r in results:
    print(f"页码: {r['chunk']['page']}")
    print(f"相似度: {r['score']:.4f}")
    print(f"内容: {r['chunk']['text'][:200]}...")
    print("---")
```

### 2. 获取LLM上下文（用于RAG增强）

```python
from rag_query import EconometricsRAG

rag = EconometricsRAG()

# 获取格式化的上下文字符串，可直接用于LLM prompt
context = rag.get_context("heteroskedasticity robust standard errors", n_results=5)
print(context)
```

**输出格式**:
```
[来源: 第135页, 相似度: 0.5295]
内容文本...

---

[来源: 第274页, 相似度: 0.5554]
内容文本...
```

### 3. 按页码搜索

```python
from rag_query import EconometricsRAG

rag = EconometricsRAG()

# 获取某一页的所有文档块
chunks = rag.search_by_page(page_number=100)
for chunk in chunks:
    print(chunk["text"])
```

### 4. 获取数据库统计信息

```python
from rag_query import EconometricsRAG

rag = EconometricsRAG()
stats = rag.get_stats()
print(stats)
# {'total_chunks': 3538, 'db_path': '...', 'embedding_model': 'all-MiniLM-L6-v2', 'dimension': 384}
```

---

## EconometricsRAG 类 API 参考

### 类初始化

```python
class EconometricsRAG:
    def __init__(self, db_path: str = "D:\\AutoRegMonkey\\database\\rag_db")
```

### 方法

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `query(question, n_results=5)` | question: str, n_results: int | List[dict] | 查询最相关的文档块 |
| `get_context(question, n_results=5)` | question: str, n_results: int | str | 获取格式化的上下文字符串 |
| `search_by_page(page_number)` | page_number: int | List[dict] | 按页码搜索 |
| `get_stats()` | 无 | dict | 获取数据库统计信息 |

### 返回数据结构

**query() 返回的每个结果**:
```python
{
    "chunk": {
        "text": "文档内容...",
        "page": 135,           # PDF页码
        "chunk_id": 2,         # 该页内的块序号
        "source": "Econometrics_by_Bruce_Hansen.pdf"
    },
    "score": 0.5295            # 余弦相似度 (0-1)
}
```

---

## 直接使用底层接口

如果需要更灵活的控制，可以直接使用FAISS和数据文件：

```python
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# 路径配置
DB_PATH = r"D:\AutoRegMonkey\database\rag_db"
INDEX_FILE = f"{DB_PATH}\\faiss_index.bin"
CHUNKS_FILE = f"{DB_PATH}\\chunks.json"

# 加载索引和数据
index = faiss.read_index(INDEX_FILE)
with open(CHUNKS_FILE, 'r', encoding='utf-8') as f:
    chunks = json.load(f)

# 加载模型
model = SentenceTransformer("all-MiniLM-L6-v2")

# 查询
query = "instrumental variables estimation"
query_embedding = model.encode([query]).astype('float32')
faiss.normalize_L2(query_embedding)

# 搜索 top-k
k = 5
scores, indices = index.search(query_embedding, k)

# 获取结果
for idx, score in zip(indices[0], scores[0]):
    chunk = chunks[idx]
    print(f"[页{chunk['page']}] 相似度:{score:.4f}")
    print(chunk['text'][:200])
    print("---")
```
