# server.py
import sys
import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

# core 모듈 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.agent import create_my_agent

# 환경 설정
load_dotenv()

app = FastAPI()

# 1. 정적 파일(CSS, JS) 연결
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. HTML 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 3. 에이전트 로드
agent_app = create_my_agent()

# 데이터 모델
class ChatRequest(BaseModel):
    query: str
    user_id: str = "user_123"
    thread_id: str = "thread_1"

# --- [라우터 1] 화면 보여주기 (GET) ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- [라우터 2] 채팅 메시지 처리 (POST) ---
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # LangChain 에이전트 실행
        result = agent_app.invoke(
            {"messages": [("user", request.query)]},
            {"configurable": {"thread_id": request.thread_id}}
        )
        ai_message = result["messages"][-1].content
        return {"response": ai_message}
    except Exception as e:
        return {"response": f"오류가 발생했습니다: {str(e)}"}