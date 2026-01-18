from .settings import settings

class EmbeddingType:
    OPENAI_EMBEDDING_3_SMALL = "text-embedding-3-small"

# =========================================================
# ▼ [여기를 수정하세요] 사용할 Embedding 을 여기서 선택합니다.
# =========================================================
ACTIVE_EMBEDDING = EmbeddingType.OPENAI_EMBEDDING_3_SMALL
# =========================================================

# 모델별 세부 설정 관리
embedding_configs = {
    # 1. OpenAI (Embedding-3-small)
    EmbeddingType.OPENAI_EMBEDDING_3_SMALL: {
    },
}