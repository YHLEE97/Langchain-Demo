# LangChain Demo
[Langchain 기본개념](https://www.notion.so/yhlee9753/LangChain-2e50fa89a8b580cc8291d648ca35d59f?source=copy_link)

[참고 사이트](https://github.com/ironmanciti/Infran_LangChain_V1)
```
# 환경설정
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# .env.example 참고하여 .env 작성 필요

[cmd] python main.py

deactivate

# Naver SLM 설치
python slm/naver-hyperclovax/install_0_5b.py 
python slm/naver-hyperclovax/test_0_5b.py
python slm/naver-hyperclovax/install_1_5b.py 
python slm/naver-hyperclovax/test_1_5b.py

# Model 변경
core/agent - llm 변경
```
