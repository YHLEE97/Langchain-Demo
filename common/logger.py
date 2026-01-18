import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from config.settings import setting

def get_logger(name: str):
    """
    프로젝트 표준 로거 생성
    - Console: INFO 레벨 이상 출력
    - File: DEBUG 레벨 이상 저장 (매일 자정 로테이션)
    """
    # 1. 로거 생성
    logger = logging.getLogger(name)
    
    # 중복 핸들러 방지 (FastAPI의 reload 등으로 인해 두 번 실행될 때 대비)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG) # 기본은 다 잡음

    # 2. 포맷 설정
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # --- 핸들러 1: 콘솔 (터미널) ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO) # INFO
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # --- 핸들러 2: 파일 저장 ---
    # settings.py에서 정의한 LOG_DIR 사용
    log_file_path = setting.LOG_DIR / "app.log"
    
    file_handler = TimedRotatingFileHandler(
        filename=log_file_path,
        when="midnight",
        interval=1,
        encoding="utf-8",
        backupCount=30
    )
    file_handler.setLevel(logging.DEBUG) # 파일엔 자세히 기록
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger