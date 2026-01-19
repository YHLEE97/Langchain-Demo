from typing import Optional, Type
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session
from database.rdm import get_db, engine

# 1. 입력 변수 스키마 정의 (AI에게 명확한 가이드 제공)
class SearchSRArgs(BaseModel):
    status: Optional[str] = Field(
        default=None, 
        description="조회할 진행 상태 (반드시 다음 중 하나여야 함: 'NEW', 'IN_PROGRESS', 'REVIEW', 'DONE', 'REJECTED')"
    )
    dept_name: Optional[str] = Field(
        default=None, 
        description="조회할 부서명 (예: 'SCM팀', 'IT개발팀', '인사팀', '품질관리팀')"
    )

@tool(args_schema=SearchSRArgs)
def search_service_requests(status: str = None, dept_name: str = None) -> str:
    """
    [필수] 부서명(dept_name)과 진행 상태(status) 두 가지 조건이 모두 있어야 조회가 가능합니다.
    만약 사용자가 두 가지 정보를 모두 제공하지 않았다면, 이 도구를 실행하지 말고 사용자에게 부족한 정보를 되물어보세요.
    """
    
    # --- [검증 로직 1] 필수 변수 누락 체크 ---
    # AI가 실수로 정보를 빼먹고 호출했을 때, 명확히 피드백을 주어 사용자에게 되묻게 만듭니다.
    missing_info = []
    if not status:
        missing_info.append("진행 상태(status)")
    if not dept_name:
        missing_info.append("부서명(dept_name)")
    
    if missing_info:
        return f"❌ 정보 부족: 다음 정보가 누락되었습니다: {', '.join(missing_info)}. 사용자에게 해당 정보를 물어본 뒤 다시 시도해주세요."

    # --- [검증 로직 2] 유효한 값인지 체크 (데이터 정확도 향상) ---
    # DB에 없는 엉뚱한 값을 검색하려 할 때 방지
    valid_statuses = ['NEW', 'IN_PROGRESS', 'REVIEW', 'DONE', 'REJECTED']
    valid_depts = ['SCM팀', 'IT개발팀', '인사팀', '품질관리팀'] # 실제 운영 시엔 DB에서 조회해서 비교 추천

    if status not in valid_statuses:
        return f"⚠️ 유효하지 않은 상태값입니다: '{status}'. 다음 중 하나를 선택해 사용자에게 확인하세요: {valid_statuses}"
    
    if dept_name not in valid_depts:
        return f"⚠️ 존재하지 않는 부서입니다: '{dept_name}'. 정확한 부서명을 사용자에게 확인하세요."

    # --- [실행 로직] SQL 실행 ---
    raw_sql = text("""
        SELECT 
            D.DEPT_NAME   AS 부서명,
            E.EMP_NAME    AS 요청자명,
            E.JOB_ROLE    AS 직급,
            R.TITLE       AS 요청제목,
            R.CONTENT     AS 요청내용,
            R.STATUS      AS 진행상태,
            R.REQ_DATE    AS 요청일시
        FROM TB_SVC_REQ R
        JOIN TB_EMP E ON R.REQ_EMP_ID = E.EMP_ID
        JOIN TB_DEPT D ON E.DEPT_ID = D.DEPT_ID
        WHERE 
            R.STATUS = :status 
            AND D.DEPT_NAME = :dept_name
        ORDER BY R.REQ_DATE DESC
    """)
    
    session = Session(bind=engine)
    
    try:
        result = session.execute(raw_sql, {"status": status, "dept_name": dept_name})
        rows = result.fetchall()
        
        if not rows:
            return f"🔍 검색 결과가 없습니다. (조건: 부서='{dept_name}', 상태='{status}')"
        
        # 결과를 상세하게 포맷팅
        response_text = f"📊 '{dept_name}'의 '{status}' 건 검색 결과 ({len(rows)}건):\n"
        response_text += "=" * 40 + "\n"
        
        for row in rows:
            response_text += (
                f"📌 제목: {row.요청제목}\n"
                f"   - 요청자: {row.요청자명} ({row.직급})\n"
                f"   - 내용: {row.요청내용}\n"
                f"   - 일시: {row.요청일시}\n"
                f"{'-' * 40}\n"
            )
            
        return response_text

    except Exception as e:
        return f"❌ 시스템 오류 발생: 쿼리 실행 중 문제가 생겼습니다. ({str(e)})"
    finally:
        session.close()

# 에이전트가 사용할 도구 목록 내보내기
def get_all_tools():
    return [search_service_requests]