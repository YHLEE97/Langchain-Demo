from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from common.logger import get_logger 
from config.settings import setting  # settings 객체 가져오기
from agents import create_my_agent
import traceback 
from datetime import datetime  # 이렇게 바꿔주세요!

# DB 관련 임포트
from sqlalchemy.orm import Session
from database.rdm import engine, Base, get_db
from database.rdm import ChatSession, ChatMessage, RunTrace
from common.callbacks import DBLoggingCallbackHandler

# 환경 설정
setting
logger = get_logger(__name__)

app = FastAPI()
Base.metadata.create_all(bind=engine)

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
    
# --- [헬퍼 함수] 세션 관리 ---
def get_or_create_session(db: Session, session_id: str, user_id: str):
    session = db.query(ChatSession).filter_by(session_id=session_id).first()
    if not session:
        session = ChatSession(session_id=session_id, user_id=user_id)
        db.add(session)
        db.commit()
    return session

# --- [헬퍼 함수] 메시지 저장 ---
def save_message(db: Session, session_id: str, role: str, content: str):
    msg = ChatMessage(session_id=session_id, role=role, content=content)
    db.add(msg)
    db.commit()

# --- [추가] 에러 발생 시 Trace 테이블에 기록하는 함수 ---
def save_error_trace(db: Session, session_id: str, error: Exception, query: str):
    """
    시스템 에러가 발생했을 때 RunTrace 테이블에 'error' 상태로 기록합니다.
    """
    try:
        # 혹시 앞선 작업에서 DB 트랜잭션이 실패한 상태일 수 있으므로 롤백
        db.rollback() 
        
        trace = RunTrace(
            session_id=session_id,
            type="system_error",   # 에러 타입 명시
            name="chat_endpoint_exception",
            inputs={"user_query": query}, # 어떤 질문에서 에러가 났는지 저장
            outputs=None,
            status="error",
            error_message=str(error), # 에러 메시지 저장
            # 필요하다면 traceback.format_exc()로 전체 스택을 저장할 수도 있음
            start_time=datetime.now(),
            end_time=datetime.now()
        )
        db.add(trace)
        db.commit()
        logger.info(f"에러 로그가 DB에 저장되었습니다. (Session: {session_id})")
        
    except Exception as e:
        # 에러 로그 저장조차 실패했을 경우 (최악의 상황)
        logger.error(f"에러 로그 DB 저장 실패: {e}")  

# --- [라우터 1] 화면 보여주기 (GET) ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- [라우터 2] 채팅 메시지 처리 (POST) ---
@app.post("/chat")
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    logger.info(f"사용자 요청 수신: user_id={request.user_id}, query={request.query}")
    
    try:
        # 1. 세션 확인 및 생성
        get_or_create_session(db, request.thread_id, request.user_id)
        
        # 2. 사용자 메시지 DB 저장
        save_message(db, request.thread_id, "user", request.query)
        
        # 3. 콜백 핸들러 생성 (DB 세션 주입)
        # 이 핸들러가 Tool 사용 내역을 RunTrace 테이블에 자동 저장합니다.
        db_callback = DBLoggingCallbackHandler(session_id=request.thread_id, db=db)
        
        # 4. LangChain 에이전트 실행 (callbacks 전달)
        result = agent_app.invoke(
            {"messages": [("user", request.query)]},
            {"configurable": {
                "thread_id": request.thread_id},
                "callbacks": [db_callback],
                "recursion_limit": 100  # 기본값 25 -> 50으로 증가
             }
        )
        
        ai_message = result["messages"][-1].content
        
        # 5. AI 응답 메시지 DB 저장
        save_message(db, request.thread_id, "ai", ai_message)
        
        logger.info(f"AI 응답 생성 완료: {result["messages"][-1].content}")
        logger.debug(f"AI 응답 생성 완료: {str(result)}")
        return {"response": ai_message}
    except Exception as e:
        # 1. 파일 로그 남기기 (상세 스택 트레이스 포함)
        logger.error(f"채팅 처리 중 치명적 오류 발생: {str(e)}", exc_info=True)
        
        # 2. DB에 에러 상황 기록 (RunTrace 테이블)
        save_error_trace(db, request.thread_id, e, request.query)
        
        # 3. (선택 사항) 채팅창에도 '에러가 났다'는 메시지를 남기고 싶다면?
        save_message(db, request.thread_id, "system", f"오류 발생: {str(e)}")
        
        return {"response": "죄송합니다. 시스템 오류가 발생하여 답변을 완료할 수 없습니다."}