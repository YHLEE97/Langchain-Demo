# tools/search.py
from langchain_community.tools.tavily_search import TavilySearchResults

def get_tavily_tool(max_results=2):
    """
    Tavily 검색 도구를 반환합니다. 
    최신 주가, 뉴스, 종목 분석 정보를 검색할 때 사용합니다.
    """
    return TavilySearchResults(max_results=max_results)