import os
import time
from dotenv import load_dotenv
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline

# 1. 환경변수 로드 (GPU 설정 등을 위해 필요할 수 있음)
load_dotenv()

# ------------------------------------------------------------
# [중요] 다운로드받은 모델이 저장된 '로컬 폴더 경로'를 지정하세요
# ------------------------------------------------------------
current_file_path = os.path.abspath(__file__)
current_folder_path = os.path.dirname(current_file_path)
model_folder_name = "HyperCLOVAX-SEED-Text-Instruct-0.5B"
local_model_path = os.path.join(current_folder_path, model_folder_name)


print(f"로컬 모델 로딩 중... 경로: {local_model_path}")
print("토크나이저 및 모델 로드")

# 2. 토크나이저 및 모델 로드 (트랜스포머 라이브러리 사용)
# trust_remote_code=True는 HyperCLOVA X 같은 커스텀 모델에 필수일 수 있습니다.
tokenizer = AutoTokenizer.from_pretrained(local_model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    local_model_path,
    trust_remote_code=True,
    device_map="auto", # GPU가 있으면 자동 사용, 없으면 CPU 사용
    torch_dtype=torch.float16 # 메모리 절약을 위해 float16 사용 (선택사항)
)

print("허깅페이스 파이프라인 생성")
# 3. 허깅페이스 파이프라인 생성 (Text Generation 작업)
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,      # 생성할 최대 토큰 수
    repetition_penalty=1.1,  # 반복 방지
    temperature=0.1,         # 창의성 조절 (낮을수록 사실적)
    return_full_text=False   # 질문 내용을 답변에서 제외할지 여부
)

print("허깅페이스 파이프라인 생성랭체인(LangChain) 객체로 변환 (Wrapper)")
# 4. 랭체인(LangChain) 객체로 변환 (Wrapper)
local_llm = HuggingFacePipeline(pipeline=pipe)

print("✅ 로컬 모델이 랭체인에 성공적으로 연결되었습니다!")

# ------------------------------------------------------------
# 5. 테스트 (랭체인 문법으로 실행)
# ------------------------------------------------------------
start_time = time.time()  # 현재 시간 기록 (초 단위)
response = local_llm.invoke("안녕하세요! 자기소개 좀 해주세요.")
end_time = time.time()    # 종료 시간 기록
elapsed_time = end_time - start_time
print("\n[AI 답변]:")
print(response)
print(f"⏱️ 소요 시간: {elapsed_time:.2f}초") # 소수점 둘째 자리까지 출력