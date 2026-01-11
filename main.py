# main.py
from dotenv import load_dotenv
from core.agent import create_my_agent

# 1. 환경 변수 로드
load_dotenv()

# 2. 에이전트 조립
app = create_my_agent()

# 3. 실행
def main():
    query = "오늘 날짜 확인하고 삼성전자 종가 알려줘"
    
    result = app.invoke(
        {
            "messages": [("user", query)],
            "user_id": "user_123",             # 사용자 ID 추가
            "preferences": {"theme": "dark"}   # 사용자 선호도 추가
         },
         {"configurable": {"thread_id": "1"},
          "recursion_limit": 50} 
        )
    print(result["messages"][-1].content)

if __name__ == "__main__":
    main()
    