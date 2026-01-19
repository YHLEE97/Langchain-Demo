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

    template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

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