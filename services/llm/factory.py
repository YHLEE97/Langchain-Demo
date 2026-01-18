from config.llm_config import ACTIVE_MODEL, ModelType, MIDDLEWARE_SUMMARY_MODEL
from .provider import CloudLLMProvider,LocalLLMProvider
# 각 모델 provider import...

def get_llm():
    """Chat GPT"""
    if ACTIVE_MODEL == ModelType.OPENAI_GPT4:
        return CloudLLMProvider.get_gpt_model_4o()
    
    """Gemini"""
    if ACTIVE_MODEL == ModelType.GEMINI_2_5_FLASH:
        return CloudLLMProvider.get_gemini_model_2_5_flash()
    
    """Naver_HYPERCLOVA"""
    if ACTIVE_MODEL == ModelType.HYPERCLOVA_LOCAL_1_5B:
        return LocalLLMProvider.get_naver_hyperclovax_1_5b()
    if ACTIVE_MODEL == ModelType.HYPERCLOVA_LOCAL_0_5B:
        return LocalLLMProvider.get_naver_hyperclovax_0_5b()
    

def get_middleware_summary_llm():
    """Chat GPT"""
    if MIDDLEWARE_SUMMARY_MODEL == ModelType.OPENAI_GPT4:
        return CloudLLMProvider.get_gpt_model_4o()
    
    """Gemini"""
    if MIDDLEWARE_SUMMARY_MODEL == ModelType.GEMINI_2_5_FLASH:
        return CloudLLMProvider.get_gemini_model_2_5_flash()
    
    """Naver_HYPERCLOVA"""
    if MIDDLEWARE_SUMMARY_MODEL == ModelType.HYPERCLOVA_LOCAL_1_5B:
        return LocalLLMProvider.get_naver_hyperclovax_1_5b()
    if MIDDLEWARE_SUMMARY_MODEL == ModelType.HYPERCLOVA_LOCAL_0_5B:
        return LocalLLMProvider.get_naver_hyperclovax_0_5b()