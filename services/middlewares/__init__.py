# tools/__init__.py
from .middleware_llm import summarization_middleware

from .base_middleware import *
from .pii_detection import *
from .message_middleware import *

def get_all_middleware():
    return [*get_middleware_llm(),
            *get_base_middleware(),
            *get_PII_middleware(),
            *get_message_middleware()
            ]
    
def get_middleware_llm():
    """model 이 필요한 Middleware 반환"""
    return [summarization_middleware()]
    
def get_base_middleware():
    """에이전트가 사용할 Base Middleware 를 반환합니다."""
    return [
        #model_limiter(),
        #global_limiter(),
        #toolcall_limiter()
    ]

def get_PII_middleware():
    """에이전트가 사용할 PII= Middleware 를 반환합니다."""
    return [
        email_detection(),
        card_detection(),
        api_detection()
    ]
    

def get_message_middleware():
    """메세지 trim 및 delete 처리 및 securty, 종료"""
    return [
        trim_messages,
        delete_old_messages,
        check_security,
        validate_response
    ]
    