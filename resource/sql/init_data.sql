-- [초기화] 기존 테이블이 있다면 삭제 (Oracle에서는 DROP TABLE 테이블명 CASCADE CONSTRAINTS; 사용)
DROP TABLE IF EXISTS TB_SVC_REQ;
DROP TABLE IF EXISTS TB_EMP;
DROP TABLE IF EXISTS TB_DEPT;

-- ==========================================
-- 1. 부서 테이블 (TB_DEPT)
-- ==========================================
CREATE TABLE TB_DEPT (
    DEPT_ID     INTEGER PRIMARY KEY,  -- Oracle: NUMBER(10)
    DEPT_NAME   VARCHAR(50) NOT NULL, -- Oracle: VARCHAR2(50)
    LOCATION    VARCHAR(100)
);

-- ==========================================
-- 2. 사원 테이블 (TB_EMP)
-- ==========================================
CREATE TABLE TB_EMP (
    EMP_ID      INTEGER PRIMARY KEY,
    EMP_NAME    VARCHAR(50) NOT NULL,
    EMAIL       VARCHAR(100) UNIQUE,
    JOB_ROLE    VARCHAR(50) DEFAULT 'Staff',
    DEPT_ID     INTEGER,
    -- Foreign Key 설정
    CONSTRAINT FK_EMP_DEPT FOREIGN KEY (DEPT_ID) REFERENCES TB_DEPT(DEPT_ID)
);

-- ==========================================
-- 3. 서비스 요청 테이블 (TB_SVC_REQ) - 핵심 복잡 데이터
-- ==========================================
CREATE TABLE TB_SVC_REQ (
    REQ_ID      INTEGER PRIMARY KEY,
    TITLE       VARCHAR(200) NOT NULL,
    CONTENT     TEXT,                 -- Oracle: CLOB
    STATUS      VARCHAR(20) DEFAULT 'NEW',
    META_INFO   TEXT,                 -- Oracle: CLOB 또는 JSON 타입
    REQ_DATE    DATETIME DEFAULT CURRENT_TIMESTAMP, -- Oracle: DATE DEFAULT SYSDATE
    REQ_EMP_ID  INTEGER,
    
    -- 상태값 제한 (Enum 흉내내기)
    CONSTRAINT CK_STATUS CHECK (STATUS IN ('NEW', 'IN_PROGRESS', 'REVIEW', 'DONE', 'REJECTED')),
    -- Foreign Key 설정
    CONSTRAINT FK_REQ_EMP FOREIGN KEY (REQ_EMP_ID) REFERENCES TB_EMP(EMP_ID)
);

-- ==========================================
-- [데이터 적재] SAMPLE DATA INSERT
-- ==========================================

-- 1. 부서 데이터
INSERT INTO TB_DEPT (DEPT_ID, DEPT_NAME, LOCATION) VALUES (10, 'SCM팀', '부산 공장');
INSERT INTO TB_DEPT (DEPT_ID, DEPT_NAME, LOCATION) VALUES (20, 'IT개발팀', '서울 본사');
INSERT INTO TB_DEPT (DEPT_ID, DEPT_NAME, LOCATION) VALUES (30, '인사팀', '서울 본사');
INSERT INTO TB_DEPT (DEPT_ID, DEPT_NAME, LOCATION) VALUES (40, '품질관리팀', '창원 공장');

-- 2. 사원 데이터
INSERT INTO TB_EMP (EMP_ID, EMP_NAME, EMAIL, JOB_ROLE, DEPT_ID) 
VALUES (101, '김철수', 'cs.kim@company.com', 'Manager', 10);

INSERT INTO TB_EMP (EMP_ID, EMP_NAME, EMAIL, JOB_ROLE, DEPT_ID) 
VALUES (102, '이영희', 'yh.lee@company.com', 'Developer', 20);

INSERT INTO TB_EMP (EMP_ID, EMP_NAME, EMAIL, JOB_ROLE, DEPT_ID) 
VALUES (103, '박민수', 'ms.park@company.com', 'Staff', 30);

INSERT INTO TB_EMP (EMP_ID, EMP_NAME, EMAIL, JOB_ROLE, DEPT_ID) 
VALUES (104, '최지훈', 'jh.choi@company.com', 'Engineer', 10);

-- 3. 서비스 요청(SR) 데이터 (JSON 형태의 텍스트 포함)
-- 김철수(SCM팀)가 올린 서버 장애 요청
INSERT INTO TB_SVC_REQ (TITLE, CONTENT, STATUS, META_INFO, REQ_EMP_ID)
VALUES (
    'ERP 자재 모듈 접속 지연', 
    '오전 10시부터 자재 수급 현황 조회 시 30초 이상 딜레이 발생함.', 
    'NEW', 
    '{"priority": "High", "system": "ERP", "tags": ["성능", "장애"]}', 
    101
);

-- 이영희(IT팀)가 올린 장비 요청
INSERT INTO TB_SVC_REQ (TITLE, CONTENT, STATUS, META_INFO, REQ_EMP_ID)
VALUES (
    'GPU 서버 증설 요청', 
    'LLM 파인튜닝을 위한 A100 장비 할당 요청합니다.', 
    'IN_PROGRESS', 
    '{"priority": "Medium", "budget_code": "IT-2026-001", "tags": ["인프라", "AI"]}', 
    102
);

-- 최지훈(SCM팀)가 올린 권한 요청
INSERT INTO TB_SVC_REQ (TITLE, CONTENT, STATUS, META_INFO, REQ_EMP_ID)
VALUES (
    'WMS 시스템 접근 권한 신청', 
    '신규 입사자 창고관리시스템(WMS) Read/Write 권한 필요.', 
    'DONE', 
    '{"priority": "Low", "user_cnt": 1, "tags": ["계정", "권한"]}', 
    104
);