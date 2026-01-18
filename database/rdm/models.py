# database/models.py
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .connection import Base

# 1. 대화방 (세션)
class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    session_id = Column(String, primary_key=True, index=True) # thread_id와 매핑
    user_id = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # 관계 설정 (Cascade: 세션 지우면 메시지/로그도 다 삭제)
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    traces = relationship("RunTrace", back_populates="session", cascade="all, delete-orphan")

# 2. 주고받은 메시지 (UI 표시용)
class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("chat_sessions.session_id"))
    
    role = Column(String) # 'user', 'ai', 'system'
    content = Column(Text) # 대화 내용
    created_at = Column(DateTime, default=datetime.now)
    
    session = relationship("ChatSession", back_populates="messages")

# 3. 내부 실행 로그 (Tool, Middleware, LLM 등)
class RunTrace(Base):
    __tablename__ = "run_traces"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("chat_sessions.session_id"))
    
    type = Column(String) # 'tool', 'llm', 'middleware', 'chain'
    name = Column(String) # 'tavily_search', 'stock_api' 등
    
    inputs = Column(JSON) # 입력값 저장
    outputs = Column(JSON, nullable=True) # 출력값 저장
    
    status = Column(String) # 'started', 'success', 'error'
    error_message = Column(Text, nullable=True)
    
    start_time = Column(DateTime, default=datetime.now)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True) # 실행 시간(초)
    
    session = relationship("ChatSession", back_populates="traces")