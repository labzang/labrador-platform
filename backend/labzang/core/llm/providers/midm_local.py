"""Midm-2.0-Mini-Instruct ë¡œì»¬ ëª¨ë¸ provider.

K-intelligence/Midm-2.0-Mini-Instruct ëª¨ë¸??ë¡œì»¬?ì„œ ë¡œë“œ?˜ì—¬
LangChain ?¸í™˜ LLM ?¸ìŠ¤?´ìŠ¤ë¥??ì„±?©ë‹ˆ??
"""

from pathlib import Path
from typing import Optional

from labzang.core.llm.base import LLMType


def create_midm_local_llm(model_dir: Optional[str] = None) -> LLMType:
    """Midm-2.0-Mini-Instruct ë¡œì»¬ ëª¨ë¸??ë¡œë“œ?©ë‹ˆ??

    Args:
        model_dir: ëª¨ë¸ ?”ë ‰?°ë¦¬ ê²½ë¡œ. None?´ë©´ ê¸°ë³¸ ê²½ë¡œ ?¬ìš©.

    Returns:
        LLMType: LangChain ?¸í™˜ LLM ?¸ìŠ¤?´ìŠ¤.

    Raises:
        ImportError: ?„ìš”???¨í‚¤ì§€ê°€ ?¤ì¹˜?˜ì? ?Šì? ê²½ìš°.
        FileNotFoundError: ëª¨ë¸ ?Œì¼??ì°¾ì„ ???†ëŠ” ê²½ìš°.
    """
    try:
        # ?ˆë¡œ??langchain-huggingface ?¨í‚¤ì§€ ?¬ìš© ?œë„
        try:
            from langchain_huggingface import HuggingFacePipeline
        except ImportError:
            # ë°±ì—…?¼ë¡œ ê¸°ì¡´ ?¨í‚¤ì§€ ?¬ìš©
            from langchain_community.llms import HuggingFacePipeline

        from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
        import torch
    except ImportError as e:
        raise ImportError(
            f"Midm ëª¨ë¸ ?¬ìš©???„í•´ ?„ìš”???¨í‚¤ì§€ê°€ ?¤ì¹˜?˜ì? ?Šì•˜?µë‹ˆ?? {e}\n"
            "pip install transformers torch langchain-community ë¥??¤í–‰?˜ì„¸??"
        )

    # ê¸°ë³¸ ëª¨ë¸ ê²½ë¡œ ?¤ì •
    if model_dir is None:
        model_dir = Path(__file__).parent.parent.parent.parent / "model" / "midm"
    else:
        model_dir = Path(model_dir)

    if not model_dir.exists():
        raise FileNotFoundError(f"Midm ëª¨ë¸ ?”ë ‰?°ë¦¬ë¥?ì°¾ì„ ???†ìŠµ?ˆë‹¤: {model_dir}")

    print(f"[AI] Midm-2.0-Mini-Instruct ëª¨ë¸ ë¡œë”© ì¤? {model_dir}")

    # GPU ?¬ìš© ê°€???¬ë? ?•ì¸
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[?”ë°”?´ìŠ¤] ?¬ìš© ?”ë°”?´ìŠ¤: {device}")

    try:
        # ? í¬?˜ì´?€ ë¡œë“œ
        print("[ë¡œë”©] ? í¬?˜ì´?€ ë¡œë”© ì¤?..")
        tokenizer = AutoTokenizer.from_pretrained(str(model_dir))

        # ëª¨ë¸ ë¡œë“œ (Midm ëª¨ë¸ ?¹ì„±??ë§ê²Œ ?¤ì •)
        print("[ë¡œë”©] ëª¨ë¸ ë¡œë”© ì¤?..")
        model = AutoModelForCausalLM.from_pretrained(
            str(model_dir),
            dtype="auto",  # ?ë™ dtype ? íƒ (torch_dtype ?€??dtype ?¬ìš©)
            device_map="auto",   # ?ë™ ?”ë°”?´ìŠ¤ ë§¤í•‘
            trust_remote_code=True,  # Midm ëª¨ë¸ ?„ìˆ˜ ?µì…˜
        )

        # ?Œì´?„ë¼???ì„± (Midm ëª¨ë¸??ìµœì ?”ëœ ?¤ì •)
        print("[?¤ì •] ?Œì´?„ë¼???ì„± ì¤?..")
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,
            temperature=0.7,
            do_sample=True,
            return_full_text=False,
            pad_token_id=tokenizer.eos_token_id,  # ?¨ë”© ? í° ?¤ì •
        )

        # LangChain ?˜í¼ë¡?ë³€??        llm = HuggingFacePipeline(pipeline=pipe)

        print("[?„ë£Œ] Midm-2.0-Mini-Instruct ëª¨ë¸ ë¡œë”© ?„ë£Œ!")
        return llm

    except Exception as e:
        print(f"[?¤ë¥˜] Midm ëª¨ë¸ ë¡œë”© ì¤??¤ë¥˜ ë°œìƒ: {e}")
        raise


def create_midm_instruct_llm(model_dir: Optional[str] = None) -> LLMType:
    """Midm-2.0-Mini-Instruct ëª¨ë¸??Instruct ?•íƒœë¡?ë¡œë“œ?©ë‹ˆ??

    ???¨ìˆ˜??create_midm_local_llm??ë³„ì¹­?¼ë¡œ, ëª…í™•?±ì„ ?„í•´ ?œê³µ?©ë‹ˆ??
    """
    return create_midm_local_llm(model_dir)
