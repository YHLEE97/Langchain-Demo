from langchain_openai import OpenAIEmbeddings


# # 1. [인터페이스] 모든 Provider가 지켜야 할 규칙 정의
# class BaseLLMProvider(ABC):
#     @abstractmethod
#     def create_llm(self, config: dict) -> BaseChatModel:
#         """설정(config)을 받아서 LangChain LLM 객체를 반환해야 함"""
#         pass
    
# 2. [외부 API] OpenAI, Google, Anthropic 등
class CloudEmbeddingProvider():
    def get_gpt_embedding_3_small():
        return OpenAIEmbeddings(model="text-embedding-3-small")

    
    # def create_llm(self, config: dict) -> BaseChatModel:
        
    #     # custom_slm.py에 있는 Wrapper 클래스 사용
    #     return ChatOpenAI(
    #         model_path=str(config["model_path"]),
    #         model_kwargs=config["model_kwargs"],
    #         pipeline_kwargs=config["pipeline_kwargs"]
    #     )
        