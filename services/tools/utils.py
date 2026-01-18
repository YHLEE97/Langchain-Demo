# tools/utils.py
from datetime import datetime
from langchain_core.tools import tool

@tool
def get_current_date() -> str:
    """
    오늘의 현재 날짜와 요일 정보를 반환합니다.
    최신 뉴스 검색이나 주식 시장 데이터 분석 시 기준 날짜로 활용하세요.
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %A")