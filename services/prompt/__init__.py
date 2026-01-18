# services/prompt/__init__.py
from .loader import PromptLoader
from config import ACTIVE_PROMPT


def get_prompt():
    """에이전트가 사용할 Prompt 를 반환합니다."""
    return PromptLoader.load(ACTIVE_PROMPT)