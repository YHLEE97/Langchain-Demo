import traceback
import uvicorn # [추가] 서버 실행을 위해 필요
from datetime import datetime

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# [LangChain & LangGraph 관련 임포트]
from langchain_core.messages import HumanMessage
from agents import create_my_graph_agent # LangGraph 에이전트 로드

# [DB 관련 임포트]
from sqlalchemy.orm import Session
from database.rdm import engine, Base, get_db
from database.rdm import ChatSession, ChatMessage, RunTrace
from common.callbacks import DBLoggingCallbackHandler

# [로깅 & 설정]
from common.logger import get_logger
# from config.settings import settings 

# 로거 설정
logger = get_logger(__name__)

# 앱 초기화
app = FastAPI()
Base.metadata.create_all(bind=engine)

# 1. 정적 파일 및 템플릿 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 2. 에이전트 생성 (서버 시작 시 한 번만 로드)
try:
    agent_app = create_my_graph_agent()
    logger.info("✅ LangGraph 에이전트 로드 성공")
except Exception as e:
    logger.error(f"❌ 에이전트 로드 실패: {e}")
    raise e

# 3. 데이터 모델 정의
class ChatRequest(BaseModel):
    query: str
    user_id: str = "user_123"
    thread_id: str = "thread_1"

# --- [헬퍼 함수] ---

def get_or_create_session(db: Session, session_id: str, user_id: str):
    session = db.query(ChatSession).filter_by(session_id=session_id).first()
    if not session:
        session = ChatSession(session_id=session_id, user_id=user_id)
        db.add(session)
        db.commit()
    return session

def save_message(db: Session, session_id: str, role: str, content: str):
    msg = ChatMessage(session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()

def save_error_trace(db: Session, session_id: str, error: Exception, query: str):
    try:
        db.rollback() 
        trace = RunTrace(
            session_id=session_id,
            type="system_error",
            name="chat_endpoint_exception",
            inputs={"user_query": query},
            outputs=None,
            status="error",
            error_message=str(error),
            start_time=datetime.now(),
            end_time=datetime.now()
        )
        db.add(trace)
        db.commit()
        logger.info(f"⚠️ 에러 로그 DB 저장 완료 (Session: {session_id})")
    except Exception as e:
        logger.error(f"❌ 에러 로그 DB 저장 실패: {e}")

# --- [라우터] ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    logger.info(f"📩 요청 수신: thread_id={request.thread_id}, query={request.query}")
    
    try:
        # 1. 세션 확인
        get_or_create_session(db, request.thread_id, request.user_id)
        
        # 2. 사용자 질문 DB 저장
        save_message(db, request.thread_id, "user", request.query)
        
        # 3. 콜백 핸들러
        db_callback = DBLoggingCallbackHandler(session_id=request.thread_id, db=db)
        
        # 4. LangGraph 에이전트 실행
        # [중요] StateGraph 구조에 맞춰 'messages' 리스트 전달
        inputs = {
            "messages": [HumanMessage(content=request.query)],
            "intermediate_steps": [] 
        }
        
        config = {
            "configurable": {"thread_id": request.thread_id},
            "callbacks": [db_callback],
            "recursion_limit": 50 
        }
        
        result = agent_app.invoke(inputs, config)
        
        # 5. 결과 추출
        ai_message = ""
        try:
            if "agent_outcome" in result:
                ai_message = result["agent_outcome"].return_values["output"]
            elif "messages" in result:
                ai_message = result["messages"][-1].content
            else:
                ai_message = "답변을 찾을 수 없습니다."
        except Exception as parse_error:
            logger.warning(f"결과 파싱 중 예외 발생: {parse_error}")
            ai_message = str(result)

        # 6. AI 답변 DB 저장
        save_message(db, request.thread_id, "ai", ai_message)
        
        logger.info(f"🚀 답변 완료: {ai_message[:50]}...")
        return {"response": ai_message}

    except Exception as e:
        logger.error(f"🔥 치명적 오류 발생: {str(e)}", exc_info=True)
        save_error_trace(db, request.thread_id, e, request.query)
        
        save_message(db, request.thread_id, "system", f"System Error: {str(e)}")
        return {"response": "죄송합니다. 시스템 오류가 발생하여 답변을 완료할 수 없습니다."}

# ---------------------------------------------------------
# [핵심 추가] 이 부분이 없어서 서버가 안 켜졌던 것입니다!
# ---------------------------------------------------------
if __name__ == "__main__":
    # 로컬 개발 환경에서 실행 시 uvicorn으로 서버 구동
    print("🚀 서버를 시작합니다... (http://localhost:8000)")
    uvicorn.run("server_graph:app", host="0.0.0.0", port=8000, reload=True)