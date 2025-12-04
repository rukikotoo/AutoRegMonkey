<p align="center">
  <img src="title.png" alt="AutoRegMonkey Logo" width="600">
</p>

<h1 align="center">🐒 AutoRegMonkey - 智能计量经济学分析代理</h1>

<p align="center">
  <a href="#简介">📋 简介</a> •
  <a href="#功能特性">✨ 功能特性</a> •
  <a href="#快速开始">🚀 快速开始</a> •
  <a href="#目录结构">📁 目录结构</a> •
  <a href="#配置">⚙️ 配置</a> •
  <a href="#使用方法">📖 使用方法</a> •
  <a href="README.en.md">English</a>
</p>

---

## 📋 简介

**AutoRegMonkey** 是一个基于大语言模型 (LLM) 的智能计量经济学分析代理系统。它可以理解自然语言描述的计量经济学任务，并基于 Bruce Hansen 计量经济学教材的知识库进行智能检索与任务解析，从而自动生成高质量分析报告。
**理论优势**：系统搭载 Bruce Hansen 经典教材构建的 RAG 知识库，理论储备相比多数碳基Regmonkey更为扎实！

---

## ✨ 功能特性

- 🤖 **智能任务解析**：自然语言理解一键任务分析
- 📚 **知识驱动**：RAG 知识库计量理论高效检索
- 🔧 **工具链集成**：自动调用 Python / Stata，灵活分析
- 📈 **专业报告输出**：自动生成包含理论、结果与解释的中文报告
- 📂 **规范工作流**：标准化文件组织与复现流程

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone <项目地址>
cd AutoRegMonkey
```

### 2. 安装依赖

```bash
pip install sentence-transformers faiss-cpu pdfplumber langchain numpy pandas
```

### 3. 配置路径

无需单独配置，已集成于技能文件。如需修改本地路径，请参考如下方式：

**当前已配置路径**：
- **Python**: `C:\Users\29165\anaconda3\python.exe`
- **Stata**: `D:/Stata/StataMP-64.exe`
  > ⚠️ Stata 路径中的反斜杠尤其要留意！

**修改方法**：
1. 使用 Claude 编辑技能文件：
   - Python路径：`.claude/skills/python/SKILL.md`
   - Stata路径：`.claude/skills/stata/SKILL.md`
2. 或输入："请帮我修改 Python/Stata 路径为 [新路径]"

**注意**：修改后需重启 Claude Code 让更改生效。

### 4. 启动分析

在 Claude Code 输入命令：
```
autoregmonkey：分析身高和体重的关系
```

---

## 📁 目录结构

```
AutoRegMonkey/
├── .claude/          # Claude 配置
├── data/             # 数据文件目录
├── database/         # RAG 数据库
├── result/           # 报告输出
├── workspace/        # 临时文件
├── title.png         # 项目 Logo
└── README.md         # 文档说明
```

---

## ⚙️ 配置

#### Python 环境
- 版本要求：Python 3.8+
- 必需包：`sentence-transformers`, `faiss-cpu`, `pdfplumber`, `langchain`, `numpy`, `pandas`

#### Stata 环境 (可选)
- StataMP / StataSE 支持用于计量分析

#### RAG 数据库
- 已预置 Bruce Hansen《Econometrics》知识库
- 支持自定义扩展：`python database/create_rag_db.py`
  可将领域论文加入数据库

---

## 📖 使用方法

#### 基本格式
```
autoregmonkey：<任务描述>
```

#### 示例命令
```
autoregmonkey：使用 sample_height_weight.csv 分析身高对体重的影响
autoregmonkey：研究身高和 BMI 的关系，控制年龄因素
autoregmonkey：检验身高和体重的线性关系显著性
```

#### 输出说明
- 分析报告保存在 `result/` 目录
- 包含详细分析过程、结果和理论解释
- 临时文件保存在 `workspace/` 目录

---

## 🛠️ 技术栈

| 组件         | 说明                                        |
|--------------|---------------------------------------------|
| LLM 框架     | Claude Code                                 |
| 向量数据库   | FAISS                                       |
| 嵌入模型     | all-MiniLM-L6-v2                            |
| 文档处理     | pdfplumber                                  |
| 分析工具     | Python / Stata                              |

---

## ⚠️ 注意事项

1. 确认技能文件中 Python / Stata 路径正确，如需修改请用 Claude 编辑
2. 数据文件请放在 `data/` 目录下
3. 重要数据请预先备份
4. 使用后请自行检查结果准确性

---

<p align="center">
  <a href="README.en.md">🔗 View in English</a> <br/>
  <em>智能计量经济学分析工具 · AutoRegMonkey</em>
</p>
