from config import EmbeddingType, ACTIVE_EMBEDDING
from .provider import CloudEmbeddingProvider

def get_embedding():
    """Chat GPT"""
    if ACTIVE_EMBEDDING == EmbeddingType.OPENAI_EMBEDDING_3_SMALL:
        return CloudEmbeddingProvider.get_gpt_embedding_3_small