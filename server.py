from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from common.logger import get_logger 
from config import settings
from agents import create_my_agent
    

# 환경 설정
settings.setting()
logger = get_logger(__name__)

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
    logger.info(f"사용자 요청 수신: user_id={request.user_id}, query={request.query}")
    
    try:
        # LangChain 에이전트 실행
        result = agent_app.invoke(
            {"messages": [("user", request.query)]},
            {"configurable": {"thread_id": request.thread_id}}
        )
        ai_message = result["messages"][-1].content
        logger.info(f"AI 응답 생성 완료: {result["messages"][-1].content}")
        logger.debug(f"AI 응답 생성 완료: {str(result)}")
        return {"response": ai_message}
    except Exception as e:
        logger.error(f"채팅 처리 중 오류 발생: {str(e)}", exc_info=True)
        return {"response": f"오류가 발생했습니다: {str(e)}"}