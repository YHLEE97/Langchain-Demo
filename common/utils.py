# common/utils.py
import os
from pathlib import Path
from typing import List

def ensure_directory(path: Path):
    """폴더가 없으면 생성해주는 안전장치"""
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

def format_docs(docs: List) -> str:
    """
    [RAG 전용] LangChain 검색 문서(Document) 리스트를 하나의 텍스트로 합침.
    나중에 Retriever 사용할 때 필수적으로 쓰입니다.
    """
    return "\n\n".join(doc.page_content for doc in docs)