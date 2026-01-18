from langchain.agents.middleware import PIIMiddleware

def email_detection():
    '''
    사용자 입력에서 이메일 주소를 탐지하고 가리기 (redact)
    예: "my email is test@example.com" → "my email is [REDACTED]"
    '''
    return PIIMiddleware("email", 
                      strategy="redact", 
                      apply_to_input=True)

def card_detection():
    '''
    신용카드 번호를 마스킹 처리 (마지막 4자리만 표시)
    예: "1234-5678-9012-3456" → "****-****-****-3456"
    '''
    return PIIMiddleware(
            "credit_card",
            detector=r"\b(?:\d[ -]*?){13,19}\b",  # 숫자 + 하이픈/공백 허용
            strategy="mask",
            apply_to_input=True,
            )

def api_detection():
    '''
    사용자 정의 PII 유형 추가 (정규식 기반)
    예: API 키 형식 "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    감지 시 실행 중단 (block)
    '''
    return PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",  # 탐지할 패턴 (정규식)
            strategy="block",  # 감지 시 오류 발생 (차단)
        )