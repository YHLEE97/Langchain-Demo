# services/prompt/loader.py
import yaml
from langchain_core.prompts import (
    ChatPromptTemplate, 
    FewShotChatMessagePromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from config.settings import settings  # settings.PROMPT_DIR 경로 사용

class PromptLoader:
    @staticmethod
    def load(template_name: str) -> ChatPromptTemplate:
        """
        YAML/YML 파일을 읽어 LangChain ChatPromptTemplate 객체를 생성합니다.
        우선순위: .yaml > .yml
        
        Args:
            template_name (str): 템플릿 파일 이름 (확장자 제외)
        """
        # 1. 파일 경로 탐색 (.yaml 우선, 없으면 .yml 확인)
        path_yaml = settings.PROMPT_DIR / f"{template_name}.yaml"
        path_yml = settings.PROMPT_DIR / f"{template_name}.yml"
        
        target_file = None

        if path_yaml.exists():
            target_file = path_yaml
        elif path_yml.exists():
            target_file = path_yml
        else:
            # 둘 다 없을 경우 에러 발생
            raise FileNotFoundError(
                f"❌ 프롬프트 파일을 찾을 수 없습니다. 경로를 확인해주세요.\n"
                f" - {path_yaml}\n"
                f" - {path_yml}"
            )

        # 2. 파일 읽기
        with open(target_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        messages = []

        # 3. [System Message] 추가
        if "system_message" in data and data["system_message"]:
            messages.append(SystemMessagePromptTemplate.from_template(data["system_message"]))

        # 4. [Few-Shot Examples] 추가
        examples = data.get("few_shot_examples")
        
        if examples and isinstance(examples, list) and len(examples) > 0:
            example_prompt = ChatPromptTemplate.from_messages([
                ("human", "{input}"),
                ("ai", "{output}"),
            ])
            
            few_shot_prompt = FewShotChatMessagePromptTemplate(
                example_prompt=example_prompt,
                examples=examples,
            )
            messages.append(few_shot_prompt)

        # 5. [Human Input] 사용자 입력 자리 추가
        messages.append(HumanMessagePromptTemplate.from_template("{input}"))

        return ChatPromptTemplate.from_messages(messages)