from langchain.agents.middleware import SummarizationMiddleware
from core.model import get_gemini_model_2_5_flash

def summarization_middleware():
    """
    메시지 이력이 너무 길어지면 요약하여 컨텍스트를 압축함
    """
    model = get_gemini_model_2_5_flash()
    
    return SummarizationMiddleware(          # 요약 미들웨어 추가
            model=model,                  # 요약에 사용할 모델
            max_tokens_before_summary=4000,  # 토큰 수가 4000에 도달하면 요약 실행
            messages_to_keep=20,             # 요약 후 최근 2개의 메시지만 유지
            summary_prompt="""
            이전 대화 내용을 간결하게 요약하되, 핵심 정보와 결론을 유지하세요.
            불필요한 인사말, 반복된 문장은 생략하고, 사용자의 의도와 모델의 주요 응답만 포함하세요.
            요약 형식:
            - 주요 내용 요약: 
            """  # 선택적 요약 프롬프트
            )
    