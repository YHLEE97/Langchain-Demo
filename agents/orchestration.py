from services.tools import get_all_tools
from services.middlewares import get_all_middleware
from services.llm import get_llm
from services.prompt import get_prompt

from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent, AgentState


class CustomAgentState(AgentState):  
    user_id: str
    preferences: dict

def create_my_agent():
    # 모델 로드
    llm = get_llm()
    
    # 통합된 도구 리스트 로드
    tools = get_all_tools()
    
    # Prompt 로드
    prompt = get_prompt()
    
    # 공통 Middle ware 리스트 로드
    base_middleware = get_all_middleware()
    
    # 에이전트 생성 (React Agent 루프 구성)
    # state_modifier를 통해 시스템 메시지를 강제 적용(Enforce)합니다.
    agent = create_agent(
        model=llm,
        tools=tools,  # Agent가 사용할 도구 목록
        middleware=base_middleware,
        state_schema=CustomAgentState,  # 사용자 정의 상태 스키마 등록
        checkpointer=InMemorySaver()   # 단기 메모리 저장소
    )
    
    return agent
