from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models import BaseChatModel
from abc import ABC, abstractmethod
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
import os
from config import ModelType


# # 1. [인터페이스] 모든 Provider가 지켜야 할 규칙 정의
# class BaseLLMProvider(ABC):
#     @abstractmethod
#     def create_llm(self, config: dict) -> BaseChatModel:
#         """설정(config)을 받아서 LangChain LLM 객체를 반환해야 함"""
#         pass
    
# 2. [외부 API] OpenAI, Google, Anthropic 등
class CloudLLMProvider():
    def get_gpt_model_4o(model_name="gpt-4o-mini", temperature=0):
        return ChatOpenAI(model=model_name, temperature=temperature)

    def get_gemini_model_2_5_flash(model_name="gemini-2.5-flash", temperature=0):
        return ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

# 3. [로컬 모델] Naver HYPERCLOVA
class LocalLLMProvider():
    current_file_path = os.path.abspath(__file__)
    current_folder_path = os.path.dirname(current_file_path)
    
    def get_naver_hyperclovax_1_5b():
        model_folder_name = ModelType.HYPERCLOVA_LOCAL_1_5B
        return LocalLLMProvider.load_naver_hyperclovax(model_folder_name)
    
    def get_naver_hyperclovax_0_5b():
        model_folder_name = ModelType.HYPERCLOVA_LOCAL_0_5B
        return LocalLLMProvider.load_naver_hyperclovax(model_folder_name)
    
    def load_naver_hyperclovax(current_folder_path,model_folder_name):
        local_model_path = os.path.join(current_folder_path, model_folder_name)

        # 2. 토크나이저 및 모델 로드 (트랜스포머 라이브러리 사용)
        # trust_remote_code=True는 HyperCLOVA X 같은 커스텀 모델에 필수일 수 있습니다.
        tokenizer = AutoTokenizer.from_pretrained(local_model_path, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            local_model_path,
            trust_remote_code=True,
            device_map="auto", # GPU가 있으면 자동 사용, 없으면 CPU 사용
            torch_dtype=torch.float16 # 메모리 절약을 위해 float16 사용 (선택사항)
        )
        
        # 3. 허깅페이스 파이프라인 생성 (Text Generation 작업)
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,      # 생성할 최대 토큰 수
            repetition_penalty=1.1,  # 반복 방지
            temperature=0.1,         # 창의성 조절 (낮을수록 사실적)
            return_full_text=False   # 질문 내용을 답변에서 제외할지 여부
        )
        
        # 4. 랭체인(LangChain) 객체로 변환 (Wrapper)
        return HuggingFacePipeline(pipeline=pipe)
        
        
        
    
    # def create_llm(self, config: dict) -> BaseChatModel:
        
    #     # custom_slm.py에 있는 Wrapper 클래스 사용
    #     return ChatOpenAI(
    #         model_path=str(config["model_path"]),
    #         model_kwargs=config["model_kwargs"],
    #         pipeline_kwargs=config["pipeline_kwargs"]
    #     )
        