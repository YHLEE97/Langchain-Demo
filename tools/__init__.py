# tools/__init__.py
from .utils import get_current_date
from .stock import get_kospi_index
from .search import get_tavily_tool
from .retriever import get_retrieve_context

def get_all_tools():
    """에이전트가 사용할 모든 도구 리스트를 반환합니다."""
    return [
        get_current_date,
        get_kospi_index,
        get_tavily_tool(max_results=3),  # 검색 결과 개수 설정
        get_retrieve_context
    ]