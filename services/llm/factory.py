from config.llm_config import llm_configs, ACTIVE_MODEL, MIDDLEWARE_SUMMARY_MODEL
from .provider import CloudLLMProvider, LocalLLMProvider

def _create_llm_instance(target_model_key: str):
    """
    내부 공통 함수: 모델 키(Key)를 받아서 실제 LLM 객체를 생성
    """
    # 1. 설정 확인
    if target_model_key not in llm_configs:
        raise ValueError(f"❌ 설정 파일(llm_config.py)에 '{target_model_key}'에 대한 정의가 없습니다.")
        
    conf = llm_configs[target_model_key] # 설정 딕셔너리 가져오기
    provider_type = conf["provider"]     # 'openai', 'google', 'local' 등

    # 2. 담당 Provider 선정 (인스턴스 생성)
    if provider_type in ["openai", "google"]:
        provider = CloudLLMProvider()
        
    elif provider_type == "local":
        provider = LocalLLMProvider()
        
    else:
        raise ValueError(f"❌ 알 수 없는 Provider 설정입니다: {provider_type}")

    # 3. Provider에게 설정(conf)을 넘겨주며 생성 요청
    return provider.create_llm(conf)


def get_llm():
    """
    메인 LLM 생성 (ACTIVE_MODEL 사용)
    """
    return _create_llm_instance(ACTIVE_MODEL)


def get_middleware_summary_llm():
    """
    요약용 LLM 생성 (MIDDLEWARE_SUMMARY_MODEL 사용)
    """
    return _create_llm_instance(MIDDLEWARE_SUMMARY_MODEL)
