# database/vector_db.py
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from services.embedding import get_embedding

CHROMA_PATH = "./chroma_db"

def save_to_vector_db(all_splits):
    print(f"--- [VECTOR DB] Chroma DB 저장 중: {CHROMA_PATH} ---")
    
    vector_db = Chroma.from_documents(
        collection_name="example_collection",
        embedding=get_embedding(),
        persist_directory=CHROMA_PATH
    )
    vector_db.add_documents(documents=all_splits)
    
    return vector_db

def get_vector_db():
    """저장된 벡터 DB 불러오기"""
    if not os.path.exists(CHROMA_PATH):
        raise FileNotFoundError(f"'{CHROMA_PATH}' 가 존재하지 않습니다. 먼저 문서를 로드하세요.")
        
    return Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=get_embedding()
    )