# config/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# 1. .env 파일 로드
load_dotenv()

class Settings:
    # --- [경로 설정] 프로젝트 루트를 기준으로 모든 경로를 자동 계산 ---
    # settings.py의 위치(config 폴더)의 부모(루트 폴더)
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # 로그 폴더
    LOG_DIR = BASE_DIR / "logs"
    
    # 로컬 모델 저장 폴더 (slm)
    SLM_BASE_DIR = BASE_DIR / "slm"
    
    # Naver-Hyperclovax 모델 저장 폴더 (slm/naver-hyperclovax)
    SLM_NAVER_DIR = BASE_DIR / "slm" / "naver-hyperclovax"
    
    # 프롬프트 템플릿 폴더 
    PROMPT_DIR = BASE_DIR / "services" / "prompt" / "templates"

    # --- [API 키 설정] (.env에서 가져옴) ---
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    HUGGING_FACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

    # --- [앱 설정] ---
    APP_NAME = "My AI Assistant"
    DEBUG = True  # 배포 시 False로 변경

# 전역 인스턴스 생성
settings = Settings()

# 로그 폴더가 없으면 미리 생성 (안전장치)
if not settings.LOG_DIR.exists():
    settings.LOG_DIR.mkdir(parents=True, exist_ok=True)