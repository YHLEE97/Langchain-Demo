import operator
import re # [추가] 정규표현식 사용 (파싱용)
from typing import Annotated, List, Union, TypedDict

# [Core 임포트]
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import BaseMessage
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser 

# [Graph 관련]
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# [프로젝트 모듈]
from services.llm.factory import get_llm
from services.tools import get_all_tools


# ---------------------------------------------------------
# 1. [직접 구현] 포맷팅 & 파서 함수 (노란줄 해결!)
# ---------------------------------------------------------

# (1) format_log_to_str 대체 함수
def format_steps(intermediate_steps):
    """도구 사용 기록(intermediate_steps)을 프롬프트용 문자열로 변환"""
    log = ""
    for action, observation in intermediate_steps:
        # (Action 로그) + (그에 대한 결과 Observation)
        log += (action.log + f"\nObservation: {observation}\n")
    return log

# (2) ReActSingleInputOutputParser 대체 함수
def parse_react_output(text: str) -> Union[AgentAction, AgentFinish]:
    """LLM의 텍스트 출력을 분석해서 Action인지 Final Answer인지 판단"""
    
    # 1. "Final Answer:"가 포함되어 있으면 종료 신호
    if "Final Answer:" in text:
        return AgentFinish(
            return_values={"output": text.split("Final Answer:")[-1].strip()},
            log=text
        )
    
    # 2. "Action:"과 "Action Input:" 패턴 찾기 (정규표현식)
    # 예: Action: search_tool \n Action Input: 날씨
    regex = r"Action: (.*?)[\n]*Action Input: ([\s\S]*)"
    match = re.search(regex, text, re.DOTALL)
    
    # 3. 매칭되면 도구 실행 신호 (AgentAction)
    if match:
        action = match.group(1).strip()
        action_input = match.group(2)
        # LLM이 가끔 멍청하게 줄바꿈 뒤에 이상한 말을 붙일 때 자르는 처리
        if "\n" in action_input:
             action_input = action_input.split("\n")[0].strip()
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=text)
    
    # 4. 포맷이 안 맞으면 그냥 전체를 답변으로 처리 (에러 방지)
    return AgentFinish(
        return_values={"output": text},
        log=text
    )

# ---------------------------------------------------------
# 2. State 정의
# ---------------------------------------------------------
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list, operator.add]

# ---------------------------------------------------------
# 3. 커스텀 도구 실행기 (Node)
# ---------------------------------------------------------
def execute_tools(state: AgentState):
    print("🛠️ [Graph] 도구 실행 노드 진입")
    agent_action = state["agent_outcome"]
    tools = get_all_tools()
    tool_map = {t.name: t for t in tools}
    
    output = None
    if agent_action.tool in tool_map:
        tool_to_use = tool_map[agent_action.tool]
        try:
            output = tool_to_use.invoke(agent_action.tool_input)
        except Exception as e:
            output = f"Tool Error: {str(e)}"
    else:
        output = f"Error: Tool '{agent_action.tool}' not found."
        
    print(f"   -> 도구 결과: {str(output)[:50]}...")
    return {
        "intermediate_steps": [(agent_action, str(output))]
    }

# ---------------------------------------------------------
# 4. 그래프 생성 함수
# ---------------------------------------------------------
def create_my_graph_agent():
    llm = get_llm()
    tools = get_all_tools()
    
    tool_names = ", ".join([t.name for t in tools])

    template = """당신은 사용자의 요청을 해결하기 위해 도구(Tool)를 사용할 수 있는 똑똑한 AI 비서입니다.
    
    사용 가능한 도구 목록:
    {tools}
    
    사용자가 질문을 하면, 아래의 [생각의 과정]을 거쳐서 답변하세요.
    
    [생각의 과정 가이드]
    1. 사용자의 질문을 해결하는 데 도구가 필요한지 생각합니다.
    2. 도구가 필요하다면 'Action'과 'Action Input'을 출력합니다.
    3. 도구 사용 결과(Observation)가 나오면, 그것을 보고 최종 답변(Final Answer)을 합니다.
    
    [출력 형식 예시 - 반드시 이 형식을 지키세요!]
    
    Question: SCM팀의 진행중인 요청 찾아줘
    Thought: 사용자가 SCM팀의 진행중(IN_PROGRESS)인 문서를 찾고 있어. search_service_requests 도구를 써야 해.
    Action: search_service_requests
    Action Input: "IN_PROGRESS", "SCM팀"
    Observation: (도구 실행 결과가 여기에 나옵니다)
    Thought: 도구 결과를 보니 3건이 검색되었네. 이걸 사용자에게 알려주자.
    Final Answer: SCM팀의 진행중인 요청은 총 3건입니다. 주요 내용은...
    
    [중요 규칙]
    - 'Action Input'에는 도구에 들어갈 인자 값만 쉼표(,)나 따옴표로 명확히 적으세요.
    - 도구가 필요 없으면 바로 'Final Answer:'를 출력하세요.
    - 상태(status) 값 매핑: '신규'->'NEW', '진행중'->'IN_PROGRESS', '완료'->'DONE', '반려'->'REJECTED'
    
    이제 시작합니다!
    
    Question: {input}
    Thought:{agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)

    # 1. LLM에 Stop Sequence 설정
    llm_with_stop = llm.bind(stop=["\nObservation"])

    # 2. 에이전트 실행 파이프라인 구성 (수동 파서 적용)
    # - format_steps: 위에 직접 만든 함수 사용
    # - parse_react_output: 위에 직접 만든 파서 함수 사용 (RunnableLambda로 감쌈)
    agent_runnable = (
        RunnablePassthrough.assign(
            agent_scratchpad=lambda x: format_steps(x["intermediate_steps"]),
        )
        | prompt.partial(tools=str(tools), tool_names=tool_names)
        | llm_with_stop
        | StrOutputParser() # <--- str parser
        | parse_react_output # <--- 여기서 직접 만든 함수 호출
    )

    # ---------------------------------------------------------
    # Node 정의
    # ---------------------------------------------------------
    def run_agent(state: AgentState):
        print("🤖 [Graph] 에이전트 생각 중...")
        messages = state['messages']
        user_input = messages[-1].content if messages else ""
        
        outcome = agent_runnable.invoke({
            "input": user_input,
            "intermediate_steps": state.get("intermediate_steps", [])
        })
        
        return {"agent_outcome": outcome}

    def should_continue(state: AgentState):
        last_outcome = state["agent_outcome"]
        if isinstance(last_outcome, AgentFinish):
            return "end"
        return "continue"

    # ---------------------------------------------------------
    # Graph 조립
    # ---------------------------------------------------------
    workflow = StateGraph(AgentState)

    workflow.add_node("agent", run_agent)
    workflow.add_node("action", execute_tools)

    workflow.set_entry_point("agent")

    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "continue": "action",
            "end": END
        }
    )

    workflow.add_edge("action", "agent")

    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    return app