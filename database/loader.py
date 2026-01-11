# database/loader.py
import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from database.vector_db import save_to_vector_db
from langchain_community.document_loaders import PyPDFLoader

def load_pdf_file(file_path="../data/reports/nke-10k-2023_korean.pdf"):
    file_path = "../data/reports/nke-10k-2023_korean.pdf"
    loader = PyPDFLoader(file_path)

    docs = loader.load()
    return docs

def split_documents(directory_path="./data"):
    docs = load_pdf_file
    
    # RecursiveCharacterTextSplitter 설정
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,              # 각 청크(chunk)의 최대 문자 수
        chunk_overlap=200,           # 청크 간 중첩(overlap) 문자 수
        add_start_index=True        # 각 청크의 시작 인덱스를 메타데이터로 추가
    )

    all_splits = text_splitter.split_documents(docs)  
    return all_splits
    