from langchain.agents.middleware import SummarizationMiddleware
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain.agents.middleware import ToolRetryMiddleware

def model_limiter():
    '''
    모델 호출 횟수를 제한 설정
    '''
    return ModelCallLimitMiddleware(
            thread_limit=10,  # 스레드(대화 세션)당 최대 10회 호출 가능 
            run_limit=5,      # 한 번의 실행(agent.invoke)당 최대 5회 호출 가능
            exit_behavior="end",  # 한도 초과 시 실행 종료
            )

def global_limiter():
    '''
    Agent가 사용할 수 있는 모든 도구(tool)에 대해 전역적으로 호출 횟수를 제한
    '''
    return ToolCallLimitMiddleware(
            thread_limit=20, 
            run_limit=10)

def toolcall_limiter():
    return ToolRetryMiddleware(
            max_retries=3,       # 최대 3번까지 재시도
            backoff_factor=2.0,  # 지수 백오프 배수 (재시도 시 대기 시간을 2배씩 증가)
            initial_delay=1.0,   # 첫 번째 재시도 전 대기 시간 (1초)
            max_delay=60.0,      # 최대 대기 시간 제한 (60초 이상 대기하지 않음)
            jitter=True,         # 동시에 여러 요청이 몰리는 것을 방지하기 위해 랜덤 지연 추가
            )