import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler
from concurrent_log_handler import ConcurrentRotatingFileHandler
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
    log_dir = setting.LOG_DIR
    log_filename = "app.log"
    log_file_path = os.path.join(str(log_dir), log_filename)
    
    file_handler = ConcurrentRotatingFileHandler(
        filename=log_file_path,
        mode="a",
        maxBytes=10 * 1024 * 1024,  # 10MB가 넘으면 파일을 나눔
        backupCount=30,             # 지난 로그 파일 30개 보관
        encoding="utf-8",
        use_gzip=False              # 압축 사용 여부 (False 권장)
    )
    
    file_handler.setLevel(logging.DEBUG) # 파일엔 자세히 기록
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger