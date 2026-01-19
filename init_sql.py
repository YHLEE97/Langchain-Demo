# run_sql.py
import sqlite3
import os

DB_PATH = "database/chat_history.db" # 경로 확인 필요
SQL_FILE = "resource/sql/init_data.sql"

def apply_sql():
    if not os.path.exists(SQL_FILE):
        print(f"❌ {SQL_FILE} 파일이 없습니다.")
        return

    # DB 연결
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # SQL 파일 읽기
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # 스크립트 실행 (여러 문장 한꺼번에 실행)
        cursor.executescript(sql_script)
        conn.commit()
        print(f"✅ {SQL_FILE} 실행 완료! 데이터가 적재되었습니다.")
        
    except sqlite3.Error as e:
        print(f"❌ SQL 실행 중 오류 발생: {e}")
        conn.rollback()
    finally:
        conn.close()


def run_complex_query():
    conn = sqlite3.connect("database/chat_history.db")
    
    query = """
    SELECT 
        D.DEPT_NAME   AS 부서명,
        E.EMP_NAME    AS 요청자명,
        R.TITLE       AS 요청제목,
        R.STATUS      AS 진행상태,
        R.REQ_DATE    AS 요청일시
    FROM TB_SVC_REQ R
    JOIN TB_EMP E ON R.REQ_EMP_ID = E.EMP_ID
    JOIN TB_DEPT D ON E.DEPT_ID = D.DEPT_ID
    WHERE 
        R.STATUS = ${status}
        AND D.DEPT_NAME = ${dept_name}
        AND R.TITLE LIKE '%접속%'
    """
    
    try:
        # pandas로 쿼리 실행 결과 가져오기
        df = pd.read_sql_query(query, conn)
        
        print(f"📊 검색 결과: {len(df)}건 발견")
        print("-" * 60)
        
        if not df.empty:
            print(df.to_string(index=False)) # 인덱스 번호 없이 출력
        else:
            print("조건에 맞는 데이터가 없습니다.")
            
        print("-" * 60)

    except Exception as e:
        print(f"❌ 쿼리 실행 실패: {e}")
    finally:
        conn.close()
        
if __name__ == "__main__":
    apply_sql()