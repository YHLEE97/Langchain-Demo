from config.settings import setting

class ModelType:
    HYPERCLOVA_LOCAL_1_5B = "HyperCLOVAX-SEED-Text-Instruct-1.5B"
    HYPERCLOVA_LOCAL_0_5B = "HyperCLOVAX-SEED-Text-Instruct-0.5B"
    OPENAI_GPT4 = "openai_gpt4"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"

# =========================================================
# ▼ [여기를 수정하세요] 사용할 모델을 여기서 선택합니다.
# =========================================================
# 1. Main Model
ACTIVE_MODEL = ModelType.OPENAI_GPT4

# 2. Middleware Model
MIDDLEWARE_SUMMARY_MODEL = ModelType.GEMINI_2_5_FLASH
# =========================================================

# 모델별 세부 설정 관리
llm_configs = {
    # 1. 로컬 모델 (HyperCLOVA X 1.5B)
    ModelType.HYPERCLOVA_LOCAL_1_5B: {
        "provider": "local",
        "model_path": setting.SLM_BASE_DIR / "HyperCLOVAX-SEED-Text-Instruct-1.5B",
        "model_kwargs": {
            "device_map": "auto",
            "trust_remote_code": True
        },
        "pipeline_kwargs": {
            "max_new_tokens": 512,
            "temperature": 0.1,
            "repetition_penalty": 1.1
        }
    },
    
    # 2. 로컬 모델 (0.5B - 테스트용)
    ModelType.HYPERCLOVA_LOCAL_0_5B: {
        "provider": "local",
        "model_path": setting.SLM_BASE_DIR / "HyperCLOVAX-SEED-Text-Instruct-0.5B",
        "model_kwargs": {
            "device_map": "auto",
            "trust_remote_code": True
        },
        "pipeline_kwargs": {
            "max_new_tokens": 256,
            "temperature": 0.1
        }
    },

    # 3. OpenAI (GPT-4)
    ModelType.OPENAI_GPT4: {
        "provider": "openai",
        "model_name": "gpt-4o",
        "temperature": 0.7,
        "api_key": setting.OPENAI_API_KEY
    },
    # 4. Gemini (2.5-Flash)
    ModelType.GEMINI_2_5_FLASH: {
        "provider": "google",
        "model_name": "gemini-2.5-flash",
        "temperature": 0.7,
        "api_key": setting.GOOGLE_API_KEY
    }
}