from langchain.tools import tool
from database.vector_db import get_vector_db

@tool(response_format="content_and_artifact")  #텍스트 설명 + 실제 결과물
def get_retrieve_context(query: str):
    """질문(query)에 답하기 위해 관련 정보를 검색합니다."""
    
    # 벡터 스토어(Vector Store)에서 유사한 문서 2개 검색
    vector_db = get_vector_db()
    retrieved_docs = vector_db.similarity_search(query, k=2)
    
    # 검색된 문서들을 문자열로 직렬화 (출처 정보 + 본문)
    serialized = "\n\n".join(
        (f"출처(Source): {doc.metadata}\n내용(Content): {doc.page_content}")
        for doc in retrieved_docs
    )
    
    # 문자열(serialized)과 실제 문서 객체 리스트(retrieved_docs)를 함께 반환
    return serialized, retrieved_docs