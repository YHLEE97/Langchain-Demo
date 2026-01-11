# core/agent.py
from langchain.agents import create_agent
from core.model import get_gpt_model_4o
from core.prompt import INSTRUCTION
from tools import get_all_tools
from middlewares import get_all_middleware

from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain.agents.middleware import ToolRetryMiddleware


def create_my_agent():
    # 모델 로드
    llm = get_gpt_model_4o()
    
    # 통합된 도구 리스트 로드
    tools = get_all_tools()
    
    # 공통 Middle ware 리스트 로드
    base_middleware = get_all_middleware()
    
    # 에이전트 생성 (React Agent 루프 구성)
    # state_modifier를 통해 시스템 메시지를 강제 적용(Enforce)합니다.
    agent = create_agent(
        model=llm,
        tools=tools,  # Agent가 사용할 도구 목록
        middleware=base_middleware
    )
    return agent