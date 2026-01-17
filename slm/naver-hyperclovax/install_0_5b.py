
import os
from dotenv import load_dotenv
from huggingface_hub import login, snapshot_download


# 1. .env 파일 로드 (환경변수로 등록됨)
load_dotenv()

# 2. 환경변수에서 토큰 가져오기
hf_token = os.getenv("HUGGING_FACE_TOKEN")

# 토큰이 잘 가져와졌는지 확인 (디버깅용, 실제 배포시엔 삭제)
if hf_token:
    print(f"토큰 로드 성공: {hf_token[:4]}****") # 보안을 위해 앞 4자리만 출력
    login(token=hf_token) # 로그인 수행
else:
    print("❌ 오류: .env 파일에서 HUGGING_FACE_TOKEN을 찾을 수 없습니다.")
    exit() # 토큰 없으면 종료

# 3. 모델 다운로드 시작
model_id = "naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-0.5B"

current_folder_path = os.path.dirname(os.path.abspath(__file__))
save_dir = current_folder_path + "/HyperCLOVAX-SEED-Text-Instruct-0.5B"   # 저장할 내 컴퓨터 경로

print(f"다운로드 시작: {model_id} -> {save_dir}")

try:
    snapshot_download(
        repo_id=model_id,
        local_dir=save_dir,
        token=hf_token  # 명시적으로 토큰 전달 (login()을 했다면 생략 가능하나 넣는 게 안전)
    )
    print("✅ 다운로드 완료!")
except Exception as e:
    print(f"❌ 다운로드 실패: {e}")
    
    
    