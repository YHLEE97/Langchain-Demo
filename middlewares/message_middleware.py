from langchain.agents.middleware import before_model
from langchain.agents.middleware import after_model
from langchain.agents import  AgentState
from langgraph.runtime import Runtime
from typing import Any
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain.messages import RemoveMessage, AIMessage
import re

# --- 회사 정책 패턴 (간단 버전) ---
POLICY_PATTERNS = [
    r"password", r"api[_-]?key", r"secret",
    r"주민등록번호", r"internal", r"confidential"
]

@before_model
def check_security(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """간단한 보안 검사 — 마지막 사용자 입력에 금칙어가 포함되어 있는지 확인."""
    messages = state["messages"]
    if not messages:
        return None

    # 가장 마지막 메시지의 내용 문자열 추출
    text = str(messages[-1].content)

    # 금칙어 탐지
    if any(re.search(p, text, re.IGNORECASE) for p in POLICY_PATTERNS):
        warning = (
            "보안 정책 위반 가능성이 있는 내용이 감지되었습니다!!!\n"
            "비밀번호, API 키, 주민등록번호 등 민감한 정보를 포함하지 말아주세요."
        )
        return {
            "messages": [
                RemoveMessage(id=messages[-1].id),  # 마지막 입력 제거
                AIMessage(content=warning),        # 경고 메시지 추가
            ]
        }

    # 이상 없으면 그대로 진행
    return None

@before_model
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """컨텍스트 윈도우에 맞추기 위해 최근 몇 개의 메시지만 유지합니다."""
    messages = state["messages"]
    
    # 메시지가 3개 이하면 트리밍 불필요
    if len(messages) <= 3:
        return None  # 변경사항 없음
    
    # 첫 번째 메시지 보존 (보통 시스템 메시지나 초기 컨텍스트)
    first_msg = messages[0]
    
    # 최근 3-4개 메시지 선택 (대화의 자연스러운 흐름 유지를 위해 짝수/홀수 고려)
    recent_messages = messages[-3:] if len(messages) % 2 == 0 else messages[-4:]
    
    # 새로운 메시지 리스트 구성
    new_messages = [first_msg] + recent_messages
    
    # 모든 기존 메시지를 제거하고 새 메시지로 교체
    return {
        "messages": [
            RemoveMessage(id=REMOVE_ALL_MESSAGES),  # 모든 메시지 제거
            *new_messages  # 선택된 메시지만 다시 추가
        ]
    }


@after_model
def delete_old_messages(state: AgentState, runtime: Runtime) -> dict | None:
    """대화가 너무 길어지지 않도록 오래된 메시지를 삭제합니다."""
    messages = state["messages"]
    if len(messages) > 2:
        # 가장 오래된 두 개의 메시지를 제거
        # print("\n[delete_old_messages] 삭제된 메시지:")
        # for m in messages[:2]:
        #     print(f" - ({m.type}) {m.content}")
        return {"messages": [RemoveMessage(id=m.id) for m in messages[:2]]}
    return None

@after_model
def validate_response(state: AgentState, runtime: Runtime) -> dict | None:
    """정치적 또는 종교적 내용을 포함한 메시지를 자동으로 제거합니다."""
    
    # 정치/종교 관련 금칙어 목록 (필요 시 확장 가능)
    POLITICAL_OR_RELIGIOUS_WORDS = [
        "정치", "대통령", "선거", "정부", "야당", "여당",
        "보수", "진보", "민주당", "국민의힘", "정당",
        "종교", "기독교", "천주교", "불교", "이슬람", "힌두교",
        "신앙", "예수", "하느님", "알라", "교회", "성당", "사찰"
    ]
    
    last_message = state["messages"][-1]  # 모델의 마지막 응답 메시지
    content = str(last_message.content).lower() 
    
    # 금칙어 중 하나라도 포함되어 있으면 메시지 제거
    if any(word.lower() in content for word in POLITICAL_OR_RELIGIOUS_WORDS):
        print("정치/종교 관련 응답 감지 → 메시지 제거됨\n제거된 메시지 ==> ")
        print(content)
        return {"messages": [RemoveMessage(id=last_message.id)]}
    
    return None  # 문제가 없으면 그대로 유지
