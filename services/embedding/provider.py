from langchain_openai import OpenAIEmbeddings
from abc import ABC, abstractmethod
from langchain_core.embeddings import Embeddings
from common.logger import get_logger

logger = get_logger(__name__)

# 1. [인터페이스] 모든 임베딩 Provider가 지켜야 할 규칙
class BaseEmbeddingProvider(ABC):
    @abstractmethod
    def create_embedding(self, config: dict) -> Embeddings:
        """설정(config)을 받아서 LangChain Embeddings 객체를 반환"""
        pass
    
# 2. [Cloud] OpenAI, Google 등 외부 API
class CloudEmbeddingProvider(BaseEmbeddingProvider):
    def create_embedding(self, config: dict) -> Embeddings:
        logger.info(f"클라우드 임베딩 연결 중: {config['model_name']}")
        logger.info(f"클라우드 임베딩 연결 중: {config}")
        
        # provider가 openai일 경우
        if config["provider"] == "openai":
            return OpenAIEmbeddings(
                model=config["model_name"],
                api_key=config["api_key"]
            )
        else:
            # logger.info(f"지원하지 않는 Cloud Provider: {config['provider']}")
            logger.info(f"지원하지 않는 Cloud Provider: {config['provider']}")
            raise ValueError(f"지원하지 않는 Cloud Provider: {config['provider']}")
        