from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import setting  # settings 객체 가져오기

# 1.  database 폴더 안에 DB 파일 생성
# 결과 경로: 프로젝트루트/database/rdm/chat_history.db
DB_URL = f"sqlite:///{setting.DB_DIR}/chat_history.db"

# 2. 엔진 생성 (SQLite 필수 옵션 포함)
engine = create_engine(
    DB_URL, 
    connect_args={"check_same_thread": False} # FastAPI 멀티스레드 호환용
)

# 3. 세션 생성기
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 모델 베이스
Base = declarative_base()

# 5. DB 세션 의존성 함수 (FastAPI용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()