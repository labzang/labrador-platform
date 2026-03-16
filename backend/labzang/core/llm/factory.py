"""LLM ?©í† ë¦??¨ìˆ˜ - ?¤ì •???°ë¼ ?ì ˆ??LLM???ì„±?©ë‹ˆ??"""

from typing import Optional

from labzang.core.config import Settings
from labzang.core.llm.base import LLMType
from labzang.core.llm.providers.openai import create_openai_chat_llm
from labzang.core.llm.providers.korean_hf_local import create_local_korean_llm
from labzang.core.llm.providers.midm_local import create_midm_local_llm


def create_llm_from_config(settings: Settings) -> Optional[LLMType]:
    """?¤ì •???°ë¼ ?ì ˆ??LLM???ì„±?©ë‹ˆ??

    Args:
        settings: ? í”Œë¦¬ì??´ì…˜ ?¤ì • ê°ì²´.

    Returns:
        LLMType: ?ì„±??LLM ?¸ìŠ¤?´ìŠ¤. ?¤ì •??ë¶ˆì™„?„í•˜ë©?None.

    Raises:
        ValueError: ì§€?í•˜ì§€ ?ŠëŠ” LLM providerê°€ ì§€?•ëœ ê²½ìš°.
        FileNotFoundError: ë¡œì»¬ ëª¨ë¸ ê²½ë¡œê°€ ?˜ëª»??ê²½ìš°.
    """
    provider = settings.llm_provider.lower()

    if provider == "openai":
        if not settings.openai_api_key:
            print("[ê²½ê³ ] OpenAI API ?¤ê? ?¤ì •?˜ì? ?Šì•˜?µë‹ˆ??")
            return None
        print("[AI] OpenAI LLM???¬ìš©?©ë‹ˆ??")
        return create_openai_chat_llm()

    elif provider == "korean_local":
        if not settings.local_model_dir:
            print("[ê²½ê³ ] LOCAL_MODEL_DIR???¤ì •?˜ì? ?Šì•˜?µë‹ˆ??")
            return None
        print(f"[ë¡œì»¬] ë¡œì»¬ ?œêµ­??ëª¨ë¸???¬ìš©?©ë‹ˆ?? {settings.local_model_dir}")
        return create_local_korean_llm(settings.local_model_dir)

    elif provider == "midm":
        print("[AI] Midm-2.0-Mini-Instruct ëª¨ë¸???¬ìš©?©ë‹ˆ??")
        # LOCAL_MODEL_DIR???¤ì •?˜ì–´ ?ˆìœ¼ë©??´ë‹¹ ê²½ë¡œ ?¬ìš©, ?†ìœ¼ë©?ê¸°ë³¸ ê²½ë¡œ
        model_dir = settings.local_model_dir if settings.local_model_dir else None
        return create_midm_local_llm(model_dir)

    else:
        raise ValueError(f"ì§€?í•˜ì§€ ?ŠëŠ” LLM provider: {provider}")
