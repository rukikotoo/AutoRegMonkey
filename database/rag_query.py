# -*- coding: utf-8 -*-
"""
RAG Query Interface for Econometrics by Bruce Hansen
This script provides an interface to query the FAISS RAG database.
"""

import os
import json
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Configuration
DB_PATH = r"D:\AutoRegMonkey\database\rag_db"
INDEX_FILE = os.path.join(DB_PATH, "faiss_index.bin")
METADATA_FILE = os.path.join(DB_PATH, "metadata.pkl")
CHUNKS_FILE = os.path.join(DB_PATH, "chunks.json")
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class EconometricsRAG:
    """RAG interface for querying econometrics content."""
    
    def __init__(self, db_path=DB_PATH):
        """Initialize the RAG interface."""
        self.db_path = db_path
        
        # Load FAISS index
        self.index = faiss.read_index(INDEX_FILE)
        
        # Load chunks
        with open(CHUNKS_FILE, 'r', encoding='utf-8') as f:
            self.chunks = json.load(f)
        
        # Load metadata
        with open(METADATA_FILE, 'rb') as f:
            self.metadata = pickle.load(f)
        
        # Load embedding model
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        
        print(f"已加载 RAG 数据库，共 {len(self.chunks)} 个文档块")
    
    def query(self, question, n_results=5):
        """Query the database and return relevant chunks."""
        # Encode query
        query_embedding = self.model.encode([question])
        query_embedding = np.array(query_embedding).astype('float32')
        faiss.normalize_L2(query_embedding)
        
        # Search
        scores, indices = self.index.search(query_embedding, n_results)
        
        results = []
        for idx, score in zip(indices[0], scores[0]):
            results.append({
                "chunk": self.chunks[idx],
                "score": float(score)
            })
        
        return results
    
    def get_context(self, question, n_results=5):
        """Get context string for LLM prompt."""
        results = self.query(question, n_results)
        
        context_parts = []
        for i, result in enumerate(results):
            chunk = result["chunk"]
            context_parts.append(f"[来源: 第{chunk['page']}页, 相似度: {result['score']:.4f}]\n{chunk['text']}")
        
        return "\n\n---\n\n".join(context_parts)
    
    def search_by_page(self, page_number):
        """Search for chunks from a specific page."""
        results = [chunk for chunk in self.chunks if chunk["page"] == page_number]
        return results
    
    def get_stats(self):
        """Get database statistics."""
        return {
            "total_chunks": len(self.chunks),
            "db_path": DB_PATH,
            "embedding_model": EMBEDDING_MODEL,
            **self.metadata
        }


def interactive_query():
    """Interactive query interface."""
    print("=" * 60)
    print("Econometrics RAG 查询系统")
    print("输入问题进行查询，输入 'quit' 退出")
    print("=" * 60)
    
    rag = EconometricsRAG()
    
    while True:
        print("\n")
        question = input("请输入问题: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("再见!")
            break
        
        if not question:
            continue
        
        results = rag.query(question, n_results=3)
        
        print("\n" + "-" * 50)
        print(f"查询: {question}")
        print("-" * 50)
        
        for i, result in enumerate(results):
            chunk = result["chunk"]
            score = result["score"]
            text = chunk["text"]
            print(f"\n【结果 {i+1}】 - 来源: 第{chunk['page']}页, 相似度: {score:.4f}")
            print(f"{text[:500]}{'...' if len(text) > 500 else ''}")


def demo_with_langchain():
    """Demo using LangChain with the RAG database."""
    from langchain_community.vectorstores import FAISS as LangchainFAISS
    from langchain_community.embeddings import HuggingFaceEmbeddings
    
    # Use HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    # Note: LangChain FAISS requires a different format
    # This is just a demo showing how to integrate
    print("LangChain integration demo - use EconometricsRAG class directly for best results")
    
    return None


if __name__ == "__main__":
    interactive_query()
