"""EXAONE-2.4B ë¡œì»¬ ëª¨ë¸ provider.

LG AI Research??EXAONE-2.4B ëª¨ë¸??ë¡œì»¬?ì„œ ë¡œë“œ?˜ì—¬
LangChain ?¸í™˜ LLM ?¸ìŠ¤?´ìŠ¤ë¥??ì„±?©ë‹ˆ??
"""

from pathlib import Path
from typing import Optional

from labzang.core.llm.base import LLMType


def create_exaone_local_llm(model_dir: Optional[str] = None) -> LLMType:
    """EXAONE-2.4B ë¡œì»¬ ëª¨ë¸??ë¡œë“œ?©ë‹ˆ??

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
            f"EXAONE ëª¨ë¸ ?¬ìš©???„í•´ ?„ìš”???¨í‚¤ì§€ê°€ ?¤ì¹˜?˜ì? ?Šì•˜?µë‹ˆ?? {e}\n"
            "pip install transformers torch langchain-community ë¥??¤í–‰?˜ì„¸??"
        )

    # ê¸°ë³¸ ëª¨ë¸ ê²½ë¡œ ?¤ì •
    if model_dir is None:
        model_dir = Path(__file__).parent.parent.parent.parent.parent / "artifacts" / "base-models" / "exaone-2.4b"
    else:
        model_dir = Path(model_dir)

    if not model_dir.exists():
        raise FileNotFoundError(f"EXAONE ëª¨ë¸ ?”ë ‰?°ë¦¬ë¥?ì°¾ì„ ???†ìŠµ?ˆë‹¤: {model_dir}")

    print(f"[AI] EXAONE-2.4B ëª¨ë¸ ë¡œë”© ì¤? {model_dir}")

    # GPU ?¬ìš© ê°€???¬ë? ?•ì¸
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[?”ë°”?´ìŠ¤] ?¬ìš© ?”ë°”?´ìŠ¤: {device}")

    try:
        # ? í¬?˜ì´?€ ë¡œë“œ
        print("[ë¡œë”©] ? í¬?˜ì´?€ ë¡œë”© ì¤?..")
        tokenizer = AutoTokenizer.from_pretrained(
            str(model_dir),
            trust_remote_code=True,
            local_files_only=True
        )

        # ?¨ë”© ? í° ?¤ì •
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        print("[ë¡œë”©] EXAONE ëª¨ë¸ ë¡œë”© ì¤?..")

        # ëª¨ë¸ ë¡œë“œ ?¤ì •
        model_kwargs = {
            "torch_dtype": torch.float16 if device == "cuda" else torch.float32,
            "device_map": "auto" if device == "cuda" else None,
            "trust_remote_code": True,
            "local_files_only": True
        }

        # ë©”ëª¨ë¦¬ê? ë¶€ì¡±í•œ ê²½ìš°ë¥??€ë¹„í•œ ?‘ì???¤ì •
        if device == "cuda":
            try:
                from transformers import BitsAndBytesConfig

                # 4bit ?‘ì???¤ì • (ë©”ëª¨ë¦??ˆì•½)
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4"
                )
                model_kwargs["quantization_config"] = quantization_config
                print("[?¤ì •] 4bit ?‘ì???œì„±??)
            except ImportError:
                print("[ê²½ê³ ] BitsAndBytesConfigë¥??¬ìš©?????†ìŠµ?ˆë‹¤. ?¼ë°˜ ëª¨ë“œë¡?ë¡œë“œ?©ë‹ˆ??")

        # ëª¨ë¸ ë¡œë“œ
        model = AutoModelForCausalLM.from_pretrained(
            str(model_dir),
            **model_kwargs
        )

        print("[?¤ì •] ?ìŠ¤???ì„± ?Œì´?„ë¼???ì„± ì¤?..")

        # ?ìŠ¤???ì„± ?Œì´?„ë¼???ì„±
        text_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            device=0 if device == "cuda" else -1,
        )

        # LangChain HuggingFacePipelineë¡??˜í•‘
        llm = HuggingFacePipeline(
            pipeline=text_pipeline,
            model_kwargs={
                "temperature": 0.7,
                "max_new_tokens": 512,
                "do_sample": True,
                "top_p": 0.9,
            }
        )

        print("[?„ë£Œ] EXAONE-2.4B ëª¨ë¸ ë¡œë”© ?„ë£Œ!")
        return llm

    except Exception as e:
        print(f"[?¤ë¥˜] EXAONE ëª¨ë¸ ë¡œë”© ?¤íŒ¨: {e}")
        raise


class ExaoneLocalLLM:
    """EXAONE ëª¨ë¸???„í•œ ê°„ë‹¨???˜í¼ ?´ë˜??""

    def __init__(self, model_dir: Optional[str] = None):
        self.llm = create_exaone_local_llm(model_dir)

    def invoke(self, prompt: str) -> str:
        """?„ë¡¬?„íŠ¸ë¥?ë°›ì•„ ?‘ë‹µ???ì„±?©ë‹ˆ??"""
        try:
            # EXAONE ëª¨ë¸???„ë¡¬?„íŠ¸ ?¬ë§·??            formatted_prompt = f"[ì§ˆë¬¸] {prompt}\n[?µë?] "

            response = self.llm.invoke(formatted_prompt)

            # ?‘ë‹µ?ì„œ ?„ë¡¬?„íŠ¸ ë¶€ë¶??œê±°
            if "[?µë?]" in response:
                response = response.split("[?µë?]")[-1].strip()

            return response
        except Exception as e:
            print(f"[?¤ë¥˜] EXAONE ëª¨ë¸ ?‘ë‹µ ?ì„± ?¤íŒ¨: {e}")
            return f"ì£„ì†¡?©ë‹ˆ?? ?‘ë‹µ ?ì„± ì¤??¤ë¥˜ê°€ ë°œìƒ?ˆìŠµ?ˆë‹¤: {e}"
