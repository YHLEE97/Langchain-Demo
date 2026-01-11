# core/prompt.py
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# 에이전트의 페르소나 및 수정(Modify) 지침 정의
INSTRUCTION = """당신은 '가치 투자'를 지향하는 20년 경력의 주식 투자 전문가입니다.
- 지침 1: 분석 요청을 받으면 'get_current_date'로 오늘 날짜를 먼저 확인하세요.
- 지침 2: 특정 종목 주가는 검색 도구를 이용해 검색하세요.
- 제약: 모든 답변 끝에는 "본 분석은 참고용이며, 투자 결정의 책임은 본인에게 있습니다."를 포함하세요."""

# 향후 추가될 Few-shot 예시 데이터
EXAMPLES = [
    # {"input": "삼성전자 주가 알려줘", "output": "오늘 날짜를 확인해보니... 삼성전자 현재가는 ...입니다."}
]

def get_final_prompt():
    example_prompt = ChatPromptTemplate.from_messages([
        ("human", "{input}"),
        ("ai", "{output}"),
    ])

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=EXAMPLES,
    )

    return ChatPromptTemplate.from_messages([
        ("system", INSTRUCTION),
        few_shot_prompt,
        ("user", "{input}")
    ])