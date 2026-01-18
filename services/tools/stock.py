import FinanceDataReader as fdr
from langchain_core.tools import tool

@tool
def get_kospi_index() -> str:
    """
    최신 코스피(KOSPI) 지수 정보를 가져옵니다.
    주식 시장의 전반적인 흐름을 파악할 때 사용합니다.
    """
    try:
        df = fdr.DataReader('KS11')
        if df.empty:
            return "코스피 데이터를 찾을 수 없습니다."
            
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        
        current_price = last_row['Close']
        prev_price = prev_row['Close']
        change = current_price - prev_price
        change_percent = (change / prev_price) * 100
        date_str = df.index[-1].strftime('%Y-%m-%d')
        
        return (f"[{date_str} 기준] 현재 KOSPI 지수: {current_price:.2f} "
                f"({'+' if change > 0 else ''}{change:.2f}, "
                f"{'+' if change > 0 else ''}{change_percent:.2f}%)")
    except Exception as e:
        return f"코스피 지수 조회 중 오류 발생: {str(e)}"