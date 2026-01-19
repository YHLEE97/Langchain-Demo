# 🦜 LangChain Demo Project

이 프로젝트는 **LangChain** 프레임워크와 Chat GPT 4.0, Naver HyperCLOVA X (SLM) 로컬 모델을 활용한 AI 에이전트 및 챗봇 서비스 데모입니다. Python 기반의 CLI 테스트 및 FastAPI를 이용한 웹 챗봇 인터페이스를 제공합니다.

## 📚 Reference
* [Python docs](https://docs.python.org/ko/3.14/tutorial/index.html)
* [LangChain docs](https://docs.langchain.com/)
* [Hugging Face - HyperCLOVA X](https://huggingface.co/naver-hyperclovax)
* [LangChain 기본 개념 정리 (Notion)](https://www.notion.so/yhlee9753/LangChain-2e50fa89a8b580cc8291d648ca35d59f?source=copy_link)
* [참고 소스 코드 (GitHub)](https://github.com/ironmanciti/Infran_LangChain_V1)

---

## 🚀 Getting Started

프로젝트 실행을 위한 환경 설정 및 설치 가이드입니다.

### 1. 가상환경 설정 및 패키지 설치
Python 3.13 설치가 필요합니다.

Python 가상환경을 생성하고 필수 의존성 패키지를 설치합니다.

```bash
# 1. 가상환경 생성 (.venv)
py -3.13 -m venv .venv
# (Mac/Linux의 경우: python3.13 -m venv .venv)


# 2. 가상환경 활성화 (Windows)
.venv\Scripts\activate
# (Mac/Linux의 경우: source .venv/bin/activate)

# 3. 의존성 패키지 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정 (.env)
```bash
# .env 파일 생성 및 작성 필요
cp .env.example .env
```

### 3. Local SLM Model Setup(Naver HyperCLOVA X)
- 0.5B Model (Test용 초경량)
```bash
# 모델 다운로드 및 설치
python slm/naver-hyperclovax/install_0_5b.py 

# 로드 테스트
python slm/naver-hyperclovax/test_0_5b.py
```
- 1.5B Model (Instruct용 경량)
```bash
# 모델 다운로드 및 설치
python slm/naver-hyperclovax/install_1_5b.py 

# 로드 테스트
python slm/naver-hyperclovax/test_1_5b.py
```

### 4. Config 설정
- config/embedding_config.py - ACTIVE_EMBEDDING 적용
- config/llm_config.py - ACTIVE_MODEL 적용
- config/prompt_config.py - ACTIVE_PROMPT 적용

### 5. Usage
- CLI 기반 테스트 - Test
```bash
python test.py
```
-  웹 챗봇 서비스 실행 (Frontend + Server)
```bash
# 서버 실행 - LangChain (Auto Reload 모드)
uvicorn server:app --reload

# 서버 실행 - LangGraph (Auto Reload 모드)
uvicorn server_graph:app --reload
```
- 접속 주소: http://127.0.0.1:8000

### 6. Deactivate
```bash
deactivate
```

### 📂 Project Structure
```
LANGCHAIN-DEMO/
├── config/                 # 모든 설정값 관리 (모델 선택, 환경변수 등)
│
├── common/                 # 프로젝트 전반에 쓰이는 공통 유틸 (Infra)
│
├── data/                   # data
│
├── database/               # DB 관련 (Vector + RDB 분리)
│   └── vector/             # Vector DB 관련
│   └── rdb/                # RDB 관련
│
├── services/               # 핵심 기능 모듈화
│   ├── embedding/          # Embedding 생성 로직 
│   ├── llm/                # LLM 생성 로직 
│   ├── middlewares/        # Middleware 관리
│   ├── prompt/             # 프롬프트 관리
│   └── tools/              # tools 관리
│
├── agent/                  # 에이전트 조립 
│
├── static/                 # 프론트엔드 리소스
├── templates/              # 프론트엔드 HTML 
├── slm/                    # 로컬 모델 파일
├── main.py                 # CLI 테스트용
├── server.py               # 서버
└── requirements.txt
```

