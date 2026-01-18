from config import EmbeddingType, ACTIVE_EMBEDDING, embedding_configs
from .provider import CloudEmbeddingProvider

def get_embedding():
    """
    설정(config)에 맞춰 적절한 임베딩 모델 객체를 반환
    """
    # 1. 현재 활성화된 설정(dict)을 가져옵니다.
    if ACTIVE_EMBEDDING not in embedding_configs:
        raise ValueError(f"설정 파일에 '{ACTIVE_EMBEDDING}'에 대한 정의가 없습니다.")
        
    conf = embedding_configs[ACTIVE_EMBEDDING] 
    
    # 2. Provider 인스턴스 생성
    provider = CloudEmbeddingProvider()
    
    # 3. [수정 포인트] 설정을 인자로 넘겨주며 메서드 호출
    return provider.create_embedding(conf)