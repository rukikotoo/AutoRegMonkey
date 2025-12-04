<p align="center">
  <img src="title.png" alt="AutoRegMonkey Logo" width="600">
</p>

<h1 align="center">AutoRegMonkey - Intelligent Econometrics Analysis Agent</h1>

<p align="center">
  <a href="#-introduction">Introduction</a> •
  <a href="#✨-features">Features</a> •
  <a href="#🚀-quick-start">Quick Start</a> •
  <a href="#📁-structure">Structure</a> •
  <a href="#⚙️-configuration">Configuration</a> •
  <a href="#📖-usage">Usage</a> •
  <a href="README.md">中文</a>
</p>

## 📋 Introduction

**AutoRegMonkey** is an LLM-based intelligent econometrics analysis agent system. It can understand natural language descriptions of econometric tasks, retrieve relevant knowledge from Bruce Hansen's econometrics textbook via RAG, dynamically invoke Python and Stata for data analysis, and generate professional Chinese reports.

> 💡 **Theoretical Advantage**: Built on Bruce Hansen's classic textbook, the RAG knowledge base may have stronger theoretical foundations than most carbon-based Regmonkeys (human researchers)!

## ✨ Features

- **🤖 Intelligent Task Parsing**: Understands natural language econometric tasks
- **📚 Knowledge-Driven**: Retrieves econometric theory from RAG knowledge base
- **🔧 Toolchain Integration**: Dynamically invokes Python and Stata
- **📈 Professional Reports**: Generates Chinese reports with theory, results, and interpretation
- **📂 Standardized Workflow**: Clear file organization and reproducible processes

## 🚀 Quick Start

### 1. Clone the project
```bash
git clone <project-url>
cd AutoRegMonkey
```

### 2. Install dependencies
```bash
pip install sentence-transformers faiss-cpu pdfplumber langchain numpy pandas
```

### 3. Configure paths
Path configurations are integrated in skill files, no separate configuration needed. If you need to modify local paths, use Claude to help edit skill files.

**Currently configured paths**:
- **Python**: `C:\Users\29165\anaconda3\python.exe`
- **Stata**: `D:\Stata\StataMP-64.exe`

**To modify paths**:
1. Use Claude Code to edit the corresponding skill files:
   - Python path: `.claude/skills/python/SKILL.md`
   - Stata path: `.claude/skills/stata/SKILL.md`
2. Or simply tell Claude: "Please help me modify the Python/Stata path to [new path]"

**Note**: After modification, restart Claude Code for changes to take effect.

### 4. Start using
In Claude Code, enter:
```
autoregmonkey: Analyze the relationship between height and weight
```

## 📁 Directory Structure

```
AutoRegMonkey/
├── .claude/          # Claude configuration
├── data/             # Data directory
├── database/         # RAG database
├── result/           # Output results
├── workspace/        # Temporary files
├── title.png         # Project logo
└── README.md         # This document (Chinese)
```

## ⚙️ Configuration

### Python Environment
- Python 3.8+
- Required packages: `sentence-transformers`, `faiss-cpu`, `pdfplumber`, `langchain`, `numpy`, `pandas`

### Stata Environment (Optional)
- StataMP or StataSE for econometric analysis

### RAG Database
- Pre-built based on Bruce Hansen's "Econometrics"
- Contains 3,538 document chunks
- To rebuild: `python database/create_rag_db.py`

## 📖 Usage

### Basic Format
```
autoregmonkey: <task description>
```

### Examples
```
autoregmonkey: Analyze the effect of height on weight using sample_height_weight.csv
autoregmonkey: Study the relationship between height and BMI, controlling for age
autoregmonkey: Test the significance of the linear relationship between height and weight
```

### Output
- Reports saved in `result/` directory
- Includes analysis process, results, and interpretation
- Temporary files in `workspace/` directory

## 🛠️ Tech Stack

- **LLM Framework**: Claude Code
- **Vector Database**: FAISS
- **Embedding Model**: all-MiniLM-L6-v2
- **Document Processing**: pdfplumber
- **Analysis Tools**: Python + Stata

## ⚠️ Notes

1. Ensure Python and Stata paths in skill files are correct; use Claude to edit if needed
2. Place data files in `data/` directory
3. Backup important data beforehand
4. Verify the accuracy of generated reports

---

<p align="center">
  <a href="README.md">中文版本</a> •
  <em>Intelligent Econometrics Analysis Tool</em>
</p>