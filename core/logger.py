# core/logger.py
import logging
import os
from logging.handlers import TimedRotatingFileHandler

def get_logger(name: str):
    """
    모든 모듈에서 공통으로 사용할 로거 생성 함수
    1. 콘솔 출력 (DEBUG 레벨 이상)
    2. 파일 저장 (매일 자정마다 새로운 파일 생성, logs 폴더)
    """
    # 1. 로그 저장할 폴더 생성
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 2. 로거 생성
    logger = logging.getLogger(name)
    
    # 이미 핸들러가 설정되어 있다면 중복 추가 방지
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG) # 전체 최소 레벨 설정

    # 3. 포맷 설정 (시간 - 로거이름 - 레벨 - 메시지)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # --- 핸들러 1: 콘솔 출력 (터미널) ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) # 콘솔에는 INFO 이상만 출력
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # --- 핸들러 2: 파일 저장 (텍스트) ---
    # TimedRotatingFileHandler: 일정 시간마다 파일 교체
    # when='midnight': 자정마다 교체, interval=1: 1일마다, backupCount=30: 30일치 보관
    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_dir, "app.log"),
        when="midnight",
        interval=1,
        encoding="utf-8",
        backupCount=30 
    )
    file_handler.setLevel(logging.DEBUG) # 파일에는 모든 상세 로그(DEBUG) 기록
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger