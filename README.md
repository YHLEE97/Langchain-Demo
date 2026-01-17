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
Python 가상환경을 생성하고 필수 의존성 패키지를 설치합니다.

```bash
# 1. 가상환경 생성 (.venv)
python -m venv .venv

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

### 3. MLocal SLM Model Setup(Naver HyperCLOVA X)
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
- 모델 변경은 core/agent.py 파일 내의 llm 설정 부분에서 수정할 수 있습니다.

### 4. Usage
- CLI 기반 테스트 (Backend) - Test
```bash
python main.py
```
-  웹 챗봇 서비스 실행 (Frontend + Server)
```bash
# 서버 실행 (Auto Reload 모드)
uvicorn server:app --reload
```
- 접속 주소: http://127.0.0.1:8000

### 5. Deactivate
```bash
deactivate
```

### 📂 Project Structure
```
LANGCHAIN-DEMO/
├── .env                  # 환경 변수
├── core/                 # 핵심 로직 (Agent, Prompt)
├── slm/                  # 로컬 SLM 모델 관리
├── api/                  # API 서버 로직 (Optional)
├── static/               # CSS, JS 정적 파일
├── templates/            # HTML 템플릿
├── server.py             # FastAPI 메인 서버
└── main.py               # CLI 테스트 실행 파일
```

