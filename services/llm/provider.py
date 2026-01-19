import torch
from abc import ABC, abstractmethod
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFacePipeline, ChatHuggingFace
from langchain_core.language_models import BaseChatModel
from common.logger import get_logger

logger = get_logger(__name__)

# 1. [인터페이스] 모든 Provider의 공통 규약
class BaseLLMProvider(ABC):
    @abstractmethod
    def create_llm(self, config: dict) -> BaseChatModel:
        """설정(config)을 받아서 LangChain LLM 객체를 반환"""
        pass

# 2. [클라우드] OpenAI, Google 등 외부 API 통합
class CloudLLMProvider(BaseLLMProvider):
    def create_llm(self, config: dict) -> BaseChatModel:
        provider_type = config["provider"]
        logger.info(f"클라우드 LLM 연결 중 ({provider_type})")
        logger.info(f"클라우드 LLM 연결 중 ({config})")

        if provider_type == "openai":
            return ChatOpenAI(
                model=config["model_name"],
                temperature=config["temperature"],
                api_key=config["api_key"]
            )
        
        elif provider_type == "google":
            return ChatGoogleGenerativeAI(
                model=config["model_name"],
                temperature=config["temperature"],
                google_api_key=config["api_key"]
            )
        
        else:
            logger.info(f"지원하지 않는 Cloud Provider: {provider_type}")
            raise ValueError(f"지원하지 않는 Cloud Provider: {provider_type}")

# 3. [로컬] HuggingFace, HyperCLOVA 등 로컬 모델 통합
class LocalLLMProvider(BaseLLMProvider):
    def create_llm(self, config: dict) -> BaseChatModel:
        model_path = str(config["model_path"]) # Path 객체를 문자열로 변환
        logger.info(f"로컬 모델 로딩 시작/경로: {model_path}")
        logger.info(f"로컬 모델 : {config}")

        # (1) 토크나이저 로드
        tokenizer = AutoTokenizer.from_pretrained(
            model_path, 
            trust_remote_code=config["model_kwargs"].get("trust_remote_code", False)
        )

        # (2) 모델 로드
        # config['model_kwargs']에 있는 설정(device_map, torch_dtype 등)을 언팩(**)해서 전달
        # 주의: torch_dtype이 문자열("float16")로 왔다면 실제 torch 타입으로 변환 필요할 수 있음
        model_kwargs = config["model_kwargs"].copy()
        if model_kwargs.get("torch_dtype") == "float16":
            model_kwargs["torch_dtype"] = torch.float16

        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            **model_kwargs
        )

        # (3) 파이프라인 생성
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            return_full_text=False, # LangChain 사용 시 필수
            **config["pipeline_kwargs"] # max_new_tokens 등
        )

        # (4) LangChain 래퍼 변환
        # HuggingFacePipeline -> ChatHuggingFace 순서로 감싸야 채팅 모델처럼 동작
        hf_pipeline = HuggingFacePipeline(pipeline=pipe)
        
        logger.info(f"로컬 모델 로딩 완료")
        return ChatHuggingFace(llm=hf_pipeline)


# 4. [클라우드] Hanwha System API LLM
class APILLMProvider(BaseLLMProvider):
    def create_llm(self, config: dict) -> BaseChatModel:
        provider_type = config["provider"]
        logger.info(f"클라우드 API LLM 연결 중 ({provider_type})")
        logger.info(f"클라우드 API LLM 연결 중 ({config})")

        if provider_type == "hanwha_system":
            return ChatOpenAI(
                base_url=config["base_url"],      # vLLM 주소
                api_key=config["api_key"],        # API Key
                model=config["model_name"],       # 타겟 모델명
                temperature=config["temperature"]         
            )
        else:
            logger.info(f"지원하지 않는 Cloud Provider: {provider_type}")
            raise ValueError(f"지원하지 않는 Cloud Provider: {provider_type}")

