# -*- coding: utf-8 -*-
"""
RAG Database Creator for Econometrics by Bruce Hansen
This script creates a FAISS vector database from the PDF for retrieval-augmented generation.
"""

import os
import json
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
from tqdm import tqdm

# Configuration
PDF_PATH = r"D:\AutoRegMonkey\database\Econometrics_by_Bruce_Hansen.pdf"
DB_PATH = r"D:\AutoRegMonkey\database\rag_db"
INDEX_FILE = os.path.join(DB_PATH, "faiss_index.bin")
METADATA_FILE = os.path.join(DB_PATH, "metadata.pkl")
CHUNKS_FILE = os.path.join(DB_PATH, "chunks.json")

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 384 dimensions

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF with page tracking."""
    print(f"正在从 PDF 提取文本: {pdf_path}")
    documents = []
    
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"PDF 共有 {total_pages} 页")
        
        for i, page in enumerate(tqdm(pdf.pages, desc="提取页面")):
            text = page.extract_text()
            if text and text.strip():
                # Clean the text
                text = re.sub(r'\s+', ' ', text)
                text = text.strip()
                
                documents.append({
                    "text": text,
                    "page": i + 1,
                    "source": os.path.basename(pdf_path)
                })
    
    print(f"成功提取 {len(documents)} 页内容")
    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """Split documents into smaller chunks for better retrieval."""
    print(f"正在分割文档 (chunk_size={chunk_size}, overlap={chunk_overlap})...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = []
    for doc in documents:
        splits = text_splitter.split_text(doc["text"])
        for j, split in enumerate(splits):
            chunks.append({
                "text": split,
                "page": doc["page"],
                "chunk_id": j,
                "source": doc["source"]
            })
    
    print(f"文档被分割成 {len(chunks)} 个块")
    return chunks

def create_vector_database(chunks, db_path):
    """Create FAISS vector database."""
    print(f"正在创建向量数据库: {db_path}")
    
    # Create directory if not exists
    os.makedirs(db_path, exist_ok=True)
    
    # Load embedding model
    print(f"加载嵌入模型: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    
    # Extract texts
    texts = [chunk["text"] for chunk in chunks]
    
    # Create embeddings
    print("正在生成向量嵌入...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    embeddings = np.array(embeddings).astype('float32')
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    print(f"向量维度: {dimension}")
    
    # Use IndexFlatIP for inner product (cosine similarity when normalized)
    faiss.normalize_L2(embeddings)  # Normalize for cosine similarity
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    # Save index
    faiss.write_index(index, INDEX_FILE)
    print(f"索引已保存到: {INDEX_FILE}")
    
    # Save metadata
    metadata = {
        "total_chunks": len(chunks),
        "embedding_model": EMBEDDING_MODEL,
        "dimension": dimension
    }
    with open(METADATA_FILE, 'wb') as f:
        pickle.dump(metadata, f)
    print(f"元数据已保存到: {METADATA_FILE}")
    
    # Save chunks
    with open(CHUNKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    print(f"文档块已保存到: {CHUNKS_FILE}")
    
    print(f"成功创建向量数据库，共 {len(chunks)} 个文档块")
    return index

def test_query(query, n_results=3):
    """Test the database with a sample query."""
    print(f"\n测试查询: '{query}'")
    
    # Load index
    index = faiss.read_index(INDEX_FILE)
    
    # Load chunks
    with open(CHUNKS_FILE, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    # Load model and encode query
    model = SentenceTransformer(EMBEDDING_MODEL)
    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype('float32')
    faiss.normalize_L2(query_embedding)
    
    # Search
    scores, indices = index.search(query_embedding, n_results)
    
    print("\n查询结果:")
    print("-" * 50)
    for i, (idx, score) in enumerate(zip(indices[0], scores[0])):
        chunk = chunks[idx]
        print(f"\n结果 {i+1} (页码: {chunk['page']}, 相似度: {score:.4f}):")
        print(f"{chunk['text'][:300]}...")
    
    return [(chunks[idx], score) for idx, score in zip(indices[0], scores[0])]

def main():
    """Main function to create RAG database."""
    print("=" * 60)
    print("RAG 数据库创建工具 - Econometrics by Bruce Hansen")
    print("=" * 60)
    
    # Check if PDF exists
    if not os.path.exists(PDF_PATH):
        print(f"错误: PDF 文件不存在: {PDF_PATH}")
        return
    
    # Extract text from PDF
    documents = extract_text_from_pdf(PDF_PATH)
    
    # Split documents into chunks
    chunks = split_documents(documents, chunk_size=3000, chunk_overlap=500)
    
    # Create vector database
    index = create_vector_database(chunks, DB_PATH)
    
    # Test with sample queries
    print("\n" + "=" * 60)
    print("测试 RAG 数据库")
    print("=" * 60)
    
    test_queries = [
        "What is OLS regression?",
        "How to calculate standard errors?",
        "What is heteroskedasticity?"
    ]
    
    for query in test_queries:
        test_query(query)
        print("\n")
    
    print("=" * 60)
    print("RAG 数据库创建完成!")
    print(f"数据库位置: {DB_PATH}")
    print(f"索引文件: {INDEX_FILE}")
    print(f"文档块数量: {len(chunks)}")
    print("=" * 60)

if __name__ == "__main__":
    main()
