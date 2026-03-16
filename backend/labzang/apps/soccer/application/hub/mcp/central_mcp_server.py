"""ì¶•êµ¬ ?„ë©”??ì¤‘ì•™ MCP ?œë²„.

ì¶•êµ¬ ?„ë©”???„ìš© LLM ëª¨ë¸(ExaOne, KoELECTRA)ê³??´ì„ ì¤‘ì•™?ì„œ ê´€ë¦¬í•©?ˆë‹¤.
"""
import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional

import torch
from fastmcp import FastMCP
from transformers import AutoModel, AutoTokenizer, AutoModelForCausalLM, pipeline

try:
    from langchain_huggingface import HuggingFacePipeline
except ImportError:
    from langchain_community.llms import HuggingFacePipeline

from labzang.core.llm.providers.exaone_local import create_exaone_local_llm

logger = logging.getLogger(__name__)


class SoccerCentralMCPServer:
    """ì¶•êµ¬ ?„ë©”??ì¤‘ì•™ MCP ?œë²„.

    ì¶•êµ¬ ?„ë©”???„ìš© LLM ëª¨ë¸ê³??´ì„ ì¤‘ì•™?ì„œ ê´€ë¦¬í•©?ˆë‹¤.
    """

    _instance: Optional["SoccerCentralMCPServer"] = None
    _initialized: bool = False

    def __new__(cls):
        """?±ê????¨í„´."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """SoccerCentralMCPServer ì´ˆê¸°??"""
        if self._initialized:
            return

        logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ì´ˆê¸°???œìž‘")

        # FastMCP ?œë²„ ?ì„±
        self.mcp = FastMCP(name="soccer_central_mcp_server")

        # ëª¨ë¸ ê²½ë¡œ ?¤ì •
        self._setup_paths()

        # ëª¨ë¸ ë¡œë“œ (ì§€??ë¡œë”©)
        self.exaone_llm: Optional[Any] = None
        self.koelectra_model: Optional[AutoModel] = None
        self.koelectra_tokenizer: Optional[AutoTokenizer] = None

        # ???€?¥ì†Œ (ì§ì ‘ ?¸ì¶œ??
        self._tools: Dict[str, Any] = {}

        # ???¤ì •
        self._setup_exaone_tools()
        self._setup_koelectra_tools()
        self._setup_filesystem_tools()
        self._setup_integrated_tools()

        self._initialized = True
        logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ì´ˆê¸°???„ë£Œ")

    def _setup_paths(self) -> None:
        """ê²½ë¡œ ?¤ì •."""
        current_file = Path(__file__)
        # app/domain/v1/soccer/hub/mcp/central_mcp_server.py
        # -> mcp -> hub -> soccer -> v1 -> domain -> app -> ?„ë¡œ?íŠ¸ ë£¨íŠ¸ (7?¨ê³„ ??
        project_root = current_file.parent.parent.parent.parent.parent.parent.parent
        self.project_root = project_root
        self.exaone_model_dir = project_root / "artifacts" / "base-models" / "exaone-2.4b"
        self.koelectra_model_dir = project_root / "artifacts" / "models--monologg--koelectra-small-v3-discriminator"

    def _load_exaone_model(self):
        """ExaOne ëª¨ë¸??ë¡œë“œ?©ë‹ˆ??(ì§€??ë¡œë”©)."""
        if self.exaone_llm is None:
            logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ëª¨ë¸ ë¡œë”© ì¤?..")
            if not self.exaone_model_dir.exists():
                logger.warning(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ëª¨ë¸ ?”ë ‰? ë¦¬ë¥?ì°¾ì„ ???†ìŠµ?ˆë‹¤: {self.exaone_model_dir}")
                try:
                    self.exaone_llm = create_exaone_local_llm()
                except Exception as e:
                    logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ëª¨ë¸ ë¡œë“œ ?¤íŒ¨: {e}", exc_info=True)
                    raise
            else:
                try:
                    device = "cuda" if torch.cuda.is_available() else "cpu"
                    logger.info(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ?¬ìš© ?”ë°”?´ìŠ¤: {device}")

                    tokenizer = AutoTokenizer.from_pretrained(
                        str(self.exaone_model_dir),
                        trust_remote_code=True,
                        local_files_only=True
                    )

                    if tokenizer.pad_token is None:
                        tokenizer.pad_token = tokenizer.eos_token

                    model_kwargs = {
                        "torch_dtype": torch.float16 if device == "cuda" else torch.float32,
                        "device_map": "auto" if device == "cuda" else None,
                        "trust_remote_code": True,
                        "local_files_only": True
                    }

                    model = AutoModelForCausalLM.from_pretrained(
                        str(self.exaone_model_dir),
                        **model_kwargs
                    )

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

                    self.exaone_llm = HuggingFacePipeline(
                        pipeline=text_pipeline,
                        model_kwargs={
                            "temperature": 0.7,
                            "max_new_tokens": 512,
                            "do_sample": True,
                            "top_p": 0.9,
                        }
                    )

                    logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ëª¨ë¸ ë¡œë”© ?„ë£Œ")
                except Exception as e:
                    logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ëª¨ë¸ ë¡œë”© ?¤íŒ¨: {e}", exc_info=True)
                    raise
        return self.exaone_llm

    def _load_koelectra_model(self) -> tuple[AutoModel, AutoTokenizer]:
        """KoELECTRA ëª¨ë¸??ë¡œë“œ?©ë‹ˆ??(ì§€??ë¡œë”©)."""
        if self.koelectra_model is None or self.koelectra_tokenizer is None:
            logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] KoELECTRA ëª¨ë¸ ë¡œë”© ì¤?..")
            if not self.koelectra_model_dir.exists():
                raise FileNotFoundError(f"KoELECTRA ëª¨ë¸ ?”ë ‰? ë¦¬ë¥?ì°¾ì„ ???†ìŠµ?ˆë‹¤: {self.koelectra_model_dir}")

            try:
                tokenizer = AutoTokenizer.from_pretrained(
                    str(self.koelectra_model_dir),
                    local_files_only=True,
                )
                logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] KoELECTRA ? í¬?˜ì´?€ ë¡œë“œ ?„ë£Œ")

                device = "cuda" if torch.cuda.is_available() else "cpu"
                model = AutoModel.from_pretrained(
                    str(self.koelectra_model_dir),
                    local_files_only=True,
                ).to(device)
                model.eval()
                logger.info(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] KoELECTRA ëª¨ë¸ ë¡œë“œ ?„ë£Œ (?”ë°”?´ìŠ¤: {device})")

                self.koelectra_model = model
                self.koelectra_tokenizer = tokenizer
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] KoELECTRA ëª¨ë¸ ë¡œë”© ?¤íŒ¨: {e}", exc_info=True)
                raise RuntimeError(f"KoELECTRA ëª¨ë¸ ë¡œë”© ?¤íŒ¨: {e}") from e

        return self.koelectra_model, self.koelectra_tokenizer

    def _setup_exaone_tools(self) -> None:
        """ExaOne ëª¨ë¸???„í•œ FastMCP ?´ì„ ?¤ì •?©ë‹ˆ??"""
        @self.mcp.tool()
        def exaone_generate_text(prompt: str, max_tokens: int = 512) -> Dict[str, Any]:
            """ExaOne ëª¨ë¸???¬ìš©?˜ì—¬ ?ìŠ¤?¸ë? ?ì„±?©ë‹ˆ??

            Args:
                prompt: ?ì„±???ìŠ¤?¸ì˜ ?„ë¡¬?„íŠ¸
                max_tokens: ìµœë? ?ì„± ? í° ??
            Returns:
                ?ì„± ê²°ê³¼ ?•ì…”?ˆë¦¬
            """
            try:
                llm = self._load_exaone_model()
                formatted_prompt = f"[ì§ˆë¬¸] {prompt}\n[?µë?] "
                response = llm.invoke(formatted_prompt)

                if "[?µë?]" in response:
                    response = response.split("[?µë?]")[-1].strip()

                logger.info(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ?ìŠ¤???ì„± ?„ë£Œ: {len(response)}??)
                return {
                    "success": True,
                    "generated_text": response,
                    "prompt": prompt,
                    "length": len(response)
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ?ìŠ¤???ì„± ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        @self.mcp.tool()
        def exaone_analyze_player_data(player_data: Dict[str, Any]) -> Dict[str, Any]:
            """ExaOne ëª¨ë¸???¬ìš©?˜ì—¬ ? ìˆ˜ ?°ì´?°ë? ë¶„ì„?©ë‹ˆ??"""
            try:
                data_text = json.dumps(player_data, ensure_ascii=False, indent=2)
                prompt = f"?¤ìŒ ? ìˆ˜ ?°ì´?°ë? ë¶„ì„?˜ê³  ì£¼ìš” ?¹ì§•???”ì•½?´ì£¼?¸ìš”:\n\n{data_text}"

                llm = self._load_exaone_model()
                formatted_prompt = f"[ì§ˆë¬¸] {prompt}\n[?µë?] "
                response = llm.invoke(formatted_prompt)

                if "[?µë?]" in response:
                    response = response.split("[?µë?]")[-1].strip()

                logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ? ìˆ˜ ?°ì´??ë¶„ì„ ?„ë£Œ")
                return {
                    "success": True,
                    "analysis": response,
                    "player_data": player_data
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ? ìˆ˜ ?°ì´??ë¶„ì„ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        @self.mcp.tool()
        def exaone_analyze_team_data(team_data: Dict[str, Any]) -> Dict[str, Any]:
            """ExaOne ëª¨ë¸???¬ìš©?˜ì—¬ ?€ ?°ì´?°ë? ë¶„ì„?©ë‹ˆ??"""
            try:
                data_text = json.dumps(team_data, ensure_ascii=False, indent=2)
                prompt = f"?¤ìŒ ?€ ?°ì´?°ë? ë¶„ì„?˜ê³  ì£¼ìš” ?¹ì§•???”ì•½?´ì£¼?¸ìš”:\n\n{data_text}"

                llm = self._load_exaone_model()
                formatted_prompt = f"[ì§ˆë¬¸] {prompt}\n[?µë?] "
                response = llm.invoke(formatted_prompt)

                if "[?µë?]" in response:
                    response = response.split("[?µë?]")[-1].strip()

                logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ?€ ?°ì´??ë¶„ì„ ?„ë£Œ")
                return {
                    "success": True,
                    "analysis": response,
                    "team_data": team_data
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ?€ ?°ì´??ë¶„ì„ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        @self.mcp.tool()
        def exaone_analyze_schedule_data(schedule_data: Dict[str, Any]) -> Dict[str, Any]:
            """ExaOne ëª¨ë¸???¬ìš©?˜ì—¬ ê²½ê¸° ?¼ì • ?°ì´?°ë? ë¶„ì„?©ë‹ˆ??"""
            try:
                data_text = json.dumps(schedule_data, ensure_ascii=False, indent=2)
                prompt = f"?¤ìŒ ê²½ê¸° ?¼ì • ?°ì´?°ë? ë¶„ì„?˜ê³  ì£¼ìš” ?¹ì§•???”ì•½?´ì£¼?¸ìš”:\n\n{data_text}"

                llm = self._load_exaone_model()
                formatted_prompt = f"[ì§ˆë¬¸] {prompt}\n[?µë?] "
                response = llm.invoke(formatted_prompt)

                if "[?µë?]" in response:
                    response = response.split("[?µë?]")[-1].strip()

                logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ê²½ê¸° ?¼ì • ?°ì´??ë¶„ì„ ?„ë£Œ")
                return {
                    "success": True,
                    "analysis": response,
                    "schedule_data": schedule_data
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ê²½ê¸° ?¼ì • ?°ì´??ë¶„ì„ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        @self.mcp.tool()
        def exaone_analyze_stadium_data(stadium_data: Dict[str, Any]) -> Dict[str, Any]:
            """ExaOne ëª¨ë¸???¬ìš©?˜ì—¬ ê²½ê¸°???°ì´?°ë? ë¶„ì„?©ë‹ˆ??"""
            try:
                data_text = json.dumps(stadium_data, ensure_ascii=False, indent=2)
                prompt = f"?¤ìŒ ê²½ê¸°???°ì´?°ë? ë¶„ì„?˜ê³  ì£¼ìš” ?¹ì§•???”ì•½?´ì£¼?¸ìš”:\n\n{data_text}"

                llm = self._load_exaone_model()
                formatted_prompt = f"[ì§ˆë¬¸] {prompt}\n[?µë?] "
                response = llm.invoke(formatted_prompt)

                if "[?µë?]" in response:
                    response = response.split("[?µë?]")[-1].strip()

                logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ê²½ê¸°???°ì´??ë¶„ì„ ?„ë£Œ")
                return {
                    "success": True,
                    "analysis": response,
                    "stadium_data": stadium_data
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ê²½ê¸°???°ì´??ë¶„ì„ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        # ???±ë¡
        self._tools["exaone_generate_text"] = exaone_generate_text
        self._tools["exaone_analyze_player_data"] = exaone_analyze_player_data
        self._tools["exaone_analyze_team_data"] = exaone_analyze_team_data
        self._tools["exaone_analyze_schedule_data"] = exaone_analyze_schedule_data
        self._tools["exaone_analyze_stadium_data"] = exaone_analyze_stadium_data

        logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ???¤ì • ?„ë£Œ")

    def _setup_koelectra_tools(self) -> None:
        """KoELECTRA ëª¨ë¸???„í•œ FastMCP ?´ì„ ?¤ì •?©ë‹ˆ??"""
        @self.mcp.tool()
        def koelectra_embed_text(text: str) -> Dict[str, Any]:
            """KoELECTRA ëª¨ë¸???¬ìš©?˜ì—¬ ?ìŠ¤?¸ë? ?„ë² ?©ìœ¼ë¡?ë³€?˜í•©?ˆë‹¤."""
            try:
                model, tokenizer = self._load_koelectra_model()
                device = "cuda" if torch.cuda.is_available() else "cpu"
                inputs = tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512,
                    padding=True
                ).to(device)

                with torch.no_grad():
                    outputs = model(**inputs)
                    embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy().tolist()[0]

                logger.info(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] KoELECTRA ?ìŠ¤???„ë² ???ì„± ?„ë£Œ: {len(embedding)}ì°¨ì›")
                return {
                    "success": True,
                    "embedding": embedding,
                    "dimension": len(embedding),
                    "text_length": len(text)
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] KoELECTRA ?„ë² ???ì„± ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        @self.mcp.tool()
        def koelectra_classify_text(text: str) -> Dict[str, Any]:
            """KoELECTRA ëª¨ë¸???¬ìš©?˜ì—¬ ?ìŠ¤?¸ë? ë¶„ë¥˜?©ë‹ˆ??"""
            try:
                model, tokenizer = self._load_koelectra_model()
                device = "cuda" if torch.cuda.is_available() else "cpu"
                inputs = tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512,
                    padding=True
                ).to(device)

                with torch.no_grad():
                    outputs = model(**inputs)
                    cls_embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy().tolist()[0]

                logger.info(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] KoELECTRA ?ìŠ¤??ë¶„ë¥˜ ?„ë£Œ")
                return {
                    "success": True,
                    "cls_embedding": cls_embedding,
                    "text": text
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] KoELECTRA ë¶„ë¥˜ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        # ???±ë¡
        self._tools["koelectra_embed_text"] = koelectra_embed_text
        self._tools["koelectra_classify_text"] = koelectra_classify_text

        logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] KoELECTRA ???¤ì • ?„ë£Œ")

    def _setup_filesystem_tools(self) -> None:
        """os?€ pathlib ?¼ì´ë¸ŒëŸ¬ë¦¬ë? ?¬ìš©???Œì¼ ?œìŠ¤???´ì„ ?¤ì •?©ë‹ˆ??"""
        project_root = self.project_root

        @self.mcp.tool()
        def path_exists(path: str) -> Dict[str, Any]:
            """ê²½ë¡œê°€ ì¡´ìž¬?˜ëŠ”ì§€ ?•ì¸?©ë‹ˆ??"""
            try:
                path_obj = Path(path)
                if not path_obj.is_absolute():
                    path_obj = project_root / path_obj

                try:
                    path_obj.resolve().relative_to(project_root.resolve())
                except ValueError:
                    return {
                        "success": False,
                        "error": "?„ë¡œ?íŠ¸ ë£¨íŠ¸ ë°–ì˜ ê²½ë¡œ???‘ê·¼?????†ìŠµ?ˆë‹¤"
                    }

                exists = path_obj.exists()
                is_file = path_obj.is_file() if exists else False
                is_dir = path_obj.is_dir() if exists else False

                return {
                    "success": True,
                    "path": str(path_obj),
                    "exists": exists,
                    "is_file": is_file,
                    "is_dir": is_dir
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ê²½ë¡œ ?•ì¸ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        @self.mcp.tool()
        def list_directory(path: str = ".") -> Dict[str, Any]:
            """?”ë ‰? ë¦¬ ?´ìš©???˜ì—´?©ë‹ˆ??"""
            try:
                path_obj = Path(path)
                if not path_obj.is_absolute():
                    path_obj = project_root / path_obj

                try:
                    path_obj.resolve().relative_to(project_root.resolve())
                except ValueError:
                    return {
                        "success": False,
                        "error": "?„ë¡œ?íŠ¸ ë£¨íŠ¸ ë°–ì˜ ê²½ë¡œ???‘ê·¼?????†ìŠµ?ˆë‹¤"
                    }

                if not path_obj.exists():
                    return {
                        "success": False,
                        "error": "ê²½ë¡œê°€ ì¡´ìž¬?˜ì? ?ŠìŠµ?ˆë‹¤"
                    }

                if not path_obj.is_dir():
                    return {
                        "success": False,
                        "error": "?”ë ‰? ë¦¬ê°€ ?„ë‹™?ˆë‹¤"
                    }

                items = []
                for item in path_obj.iterdir():
                    items.append({
                        "name": item.name,
                        "is_file": item.is_file(),
                        "is_dir": item.is_dir(),
                        "size": item.stat().st_size if item.is_file() else None
                    })

                return {
                    "success": True,
                    "path": str(path_obj),
                    "items": sorted(items, key=lambda x: (not x["is_dir"], x["name"])),
                    "count": len(items)
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ?”ë ‰? ë¦¬ ?˜ì—´ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        @self.mcp.tool()
        def read_file(file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
            """?Œì¼ ?´ìš©???½ìŠµ?ˆë‹¤."""
            try:
                path_obj = Path(file_path)
                if not path_obj.is_absolute():
                    path_obj = project_root / path_obj

                try:
                    path_obj.resolve().relative_to(project_root.resolve())
                except ValueError:
                    return {
                        "success": False,
                        "error": "?„ë¡œ?íŠ¸ ë£¨íŠ¸ ë°–ì˜ ê²½ë¡œ???‘ê·¼?????†ìŠµ?ˆë‹¤"
                    }

                if not path_obj.exists():
                    return {
                        "success": False,
                        "error": "?Œì¼??ì¡´ìž¬?˜ì? ?ŠìŠµ?ˆë‹¤"
                    }

                if not path_obj.is_file():
                    return {
                        "success": False,
                        "error": "?Œì¼???„ë‹™?ˆë‹¤"
                    }

                file_size = path_obj.stat().st_size
                if file_size > 10 * 1024 * 1024:
                    return {
                        "success": False,
                        "error": "?Œì¼???ˆë¬´ ?½ë‹ˆ??(10MB ?œí•œ)"
                    }

                content = path_obj.read_text(encoding=encoding)

                return {
                    "success": True,
                    "path": str(path_obj),
                    "content": content,
                    "size": file_size,
                    "encoding": encoding
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ?Œì¼ ?½ê¸° ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        @self.mcp.tool()
        def get_path_info(path: str) -> Dict[str, Any]:
            """ê²½ë¡œ???ì„¸ ?•ë³´ë¥?ì¡°íšŒ?©ë‹ˆ??"""
            try:
                path_obj = Path(path)
                if not path_obj.is_absolute():
                    path_obj = project_root / path_obj

                try:
                    path_obj.resolve().relative_to(project_root.resolve())
                except ValueError:
                    return {
                        "success": False,
                        "error": "?„ë¡œ?íŠ¸ ë£¨íŠ¸ ë°–ì˜ ê²½ë¡œ???‘ê·¼?????†ìŠµ?ˆë‹¤"
                    }

                if not path_obj.exists():
                    return {
                        "success": True,
                        "path": str(path_obj),
                        "exists": False,
                        "absolute_path": str(path_obj.resolve())
                    }

                stat_info = path_obj.stat()

                return {
                    "success": True,
                    "path": str(path_obj),
                    "absolute_path": str(path_obj.resolve()),
                    "exists": True,
                    "is_file": path_obj.is_file(),
                    "is_dir": path_obj.is_dir(),
                    "size": stat_info.st_size if path_obj.is_file() else None,
                    "created": stat_info.st_ctime,
                    "modified": stat_info.st_mtime,
                    "parent": str(path_obj.parent),
                    "name": path_obj.name,
                    "stem": path_obj.stem,
                    "suffix": path_obj.suffix
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ê²½ë¡œ ?•ë³´ ì¡°íšŒ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        @self.mcp.tool()
        def join_paths(*paths: str) -> Dict[str, Any]:
            """?¬ëŸ¬ ê²½ë¡œë¥?ê²°í•©?©ë‹ˆ??"""
            try:
                combined = Path(*paths)
                return {
                    "success": True,
                    "combined_path": str(combined),
                    "parts": list(combined.parts)
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ê²½ë¡œ ê²°í•© ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        @self.mcp.tool()
        def get_environment_variable(name: str, default: Optional[str] = None) -> Dict[str, Any]:
            """?˜ê²½ ë³€?˜ë? ?½ìŠµ?ˆë‹¤."""
            try:
                value = os.getenv(name, default)
                return {
                    "success": True,
                    "name": name,
                    "value": value,
                    "exists": name in os.environ
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ?˜ê²½ ë³€???½ê¸° ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        @self.mcp.tool()
        def get_current_directory() -> Dict[str, Any]:
            """?„ìž¬ ?‘ì—… ?”ë ‰? ë¦¬ë¥?ë°˜í™˜?©ë‹ˆ??"""
            try:
                cwd = Path.cwd()
                return {
                    "success": True,
                    "current_directory": str(cwd),
                    "absolute_path": str(cwd.resolve())
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ?„ìž¬ ?”ë ‰? ë¦¬ ì¡°íšŒ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        # ???±ë¡
        self._tools["path_exists"] = path_exists
        self._tools["list_directory"] = list_directory
        self._tools["read_file"] = read_file
        self._tools["get_path_info"] = get_path_info
        self._tools["join_paths"] = join_paths
        self._tools["get_environment_variable"] = get_environment_variable
        self._tools["get_current_directory"] = get_current_directory

        logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ?Œì¼?œìŠ¤?????¤ì • ?„ë£Œ")

    def _setup_integrated_tools(self) -> None:
        """KoELECTRA?€ ExaOne???°ê²°?˜ëŠ” ?µí•© FastMCP ?´ì„ ?¤ì •?©ë‹ˆ??"""
        @self.mcp.tool()
        async def koelectra_to_exaone_pipeline(text: str) -> Dict[str, Any]:
            """KoELECTRAë¡??ìŠ¤?¸ë? ?„ë² ?©í•œ ??ExaOne?¼ë¡œ ë¶„ì„?˜ëŠ” ?Œì´?„ë¼??"""
            try:
                logger.info(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ?µí•© ?Œì´?„ë¼???œìž‘: {text[:50]}...")

                # 1?¨ê³„: KoELECTRAë¡??„ë² ???ì„±
                model, tokenizer = self._load_koelectra_model()
                device = "cuda" if torch.cuda.is_available() else "cpu"
                inputs = tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512,
                    padding=True
                ).to(device)

                with torch.no_grad():
                    outputs = model(**inputs)
                    embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy().tolist()[0]

                logger.info(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] KoELECTRA ?„ë² ???ì„± ?„ë£Œ: {len(embedding)}ì°¨ì›")

                # 2?¨ê³„: ExaOne?¼ë¡œ ?ìŠ¤??ë¶„ì„
                analysis_prompt = f"?¤ìŒ ?ìŠ¤?¸ë? ë¶„ì„?˜ê³  ì£¼ìš” ?´ìš©???”ì•½?´ì£¼?¸ìš”:\n\n{text}"
                llm = self._load_exaone_model()
                formatted_prompt = f"[ì§ˆë¬¸] {analysis_prompt}\n[?µë?] "
                exaone_result = llm.invoke(formatted_prompt)

                if "[?µë?]" in exaone_result:
                    exaone_result = exaone_result.split("[?µë?]")[-1].strip()

                logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ExaOne ë¶„ì„ ?„ë£Œ")

                return {
                    "success": True,
                    "koelectra_embedding": {
                        "dimension": len(embedding),
                        "sample": embedding[:10]
                    },
                    "exaone_analysis": exaone_result,
                    "original_text": text
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ?µí•© ?Œì´?„ë¼??ì²˜ë¦¬ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e)
                }

        @self.mcp.tool()
        async def analyze_player_with_models(player_data: Dict[str, Any]) -> Dict[str, Any]:
            """KoELECTRA?€ ExaOne???¬ìš©?˜ì—¬ ? ìˆ˜ ?°ì´?°ë? ì¢…í•© ë¶„ì„?©ë‹ˆ??"""
            try:
                logger.info(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ? ìˆ˜ ?°ì´??ë¶„ì„ ?œìž‘: {player_data.get('player_name', 'Unknown')}")

                data_text = json.dumps(player_data, ensure_ascii=False, indent=2)

                # 1?¨ê³„: KoELECTRAë¡??°ì´???„ë² ??                model, tokenizer = self._load_koelectra_model()
                device = "cuda" if torch.cuda.is_available() else "cpu"
                inputs = tokenizer(
                    data_text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512,
                    padding=True
                ).to(device)

                with torch.no_grad():
                    outputs = model(**inputs)
                    embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy().tolist()[0]

                # 2?¨ê³„: ExaOne?¼ë¡œ ?°ì´??ë¶„ì„
                analysis_prompt = (
                    f"?¤ìŒ ? ìˆ˜ ?°ì´?°ë? ë¶„ì„?˜ê³  ì£¼ìš” ?¹ì§•, ê°•ì , ?½ì ???”ì•½?´ì£¼?¸ìš”:\n\n{data_text}"
                )
                llm = self._load_exaone_model()
                exaone_result = llm.invoke(f"[ì§ˆë¬¸] {analysis_prompt}\n[?µë?] ")

                if "[?µë?]" in exaone_result:
                    exaone_result = exaone_result.split("[?µë?]")[-1].strip()

                logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ? ìˆ˜ ?°ì´??ë¶„ì„ ?„ë£Œ")

                return {
                    "success": True,
                    "player_data": player_data,
                    "koelectra_embedding": {
                        "dimension": len(embedding),
                        "sample": embedding[:10]
                    },
                    "exaone_analysis": exaone_result,
                    "summary": {
                        "embedding_dim": len(embedding),
                        "analysis_length": len(exaone_result)
                    }
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ? ìˆ˜ ?°ì´??ë¶„ì„ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e),
                    "player_data": player_data
                }

        @self.mcp.tool()
        async def analyze_team_with_models(team_data: Dict[str, Any]) -> Dict[str, Any]:
            """KoELECTRA?€ ExaOne???¬ìš©?˜ì—¬ ?€ ?°ì´?°ë? ì¢…í•© ë¶„ì„?©ë‹ˆ??"""
            try:
                logger.info(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ?€ ?°ì´??ë¶„ì„ ?œìž‘: {team_data.get('team_name', 'Unknown')}")

                data_text = json.dumps(team_data, ensure_ascii=False, indent=2)

                # 1?¨ê³„: KoELECTRAë¡??°ì´???„ë² ??                model, tokenizer = self._load_koelectra_model()
                device = "cuda" if torch.cuda.is_available() else "cpu"
                inputs = tokenizer(
                    data_text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512,
                    padding=True
                ).to(device)

                with torch.no_grad():
                    outputs = model(**inputs)
                    embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy().tolist()[0]

                # 2?¨ê³„: ExaOne?¼ë¡œ ?°ì´??ë¶„ì„
                analysis_prompt = (
                    f"?¤ìŒ ?€ ?°ì´?°ë? ë¶„ì„?˜ê³  ì£¼ìš” ?¹ì§•, ? ìˆ˜ êµ¬ì„±, ?„ìˆ  ?•ë³´ë¥??”ì•½?´ì£¼?¸ìš”:\n\n{data_text}"
                )
                llm = self._load_exaone_model()
                exaone_result = llm.invoke(f"[ì§ˆë¬¸] {analysis_prompt}\n[?µë?] ")

                if "[?µë?]" in exaone_result:
                    exaone_result = exaone_result.split("[?µë?]")[-1].strip()

                logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ?€ ?°ì´??ë¶„ì„ ?„ë£Œ")

                return {
                    "success": True,
                    "team_data": team_data,
                    "koelectra_embedding": {
                        "dimension": len(embedding),
                        "sample": embedding[:10]
                    },
                    "exaone_analysis": exaone_result,
                    "summary": {
                        "embedding_dim": len(embedding),
                        "analysis_length": len(exaone_result)
                    }
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ?€ ?°ì´??ë¶„ì„ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e),
                    "team_data": team_data
                }

        @self.mcp.tool()
        async def analyze_schedule_with_models(schedule_data: Dict[str, Any]) -> Dict[str, Any]:
            """KoELECTRA?€ ExaOne???¬ìš©?˜ì—¬ ê²½ê¸° ?¼ì • ?°ì´?°ë? ì¢…í•© ë¶„ì„?©ë‹ˆ??"""
            try:
                logger.info(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ê²½ê¸° ?¼ì • ?°ì´??ë¶„ì„ ?œìž‘: {schedule_data.get('match_date', 'Unknown')}")

                data_text = json.dumps(schedule_data, ensure_ascii=False, indent=2)

                # 1?¨ê³„: KoELECTRAë¡??°ì´???„ë² ??                model, tokenizer = self._load_koelectra_model()
                device = "cuda" if torch.cuda.is_available() else "cpu"
                inputs = tokenizer(
                    data_text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512,
                    padding=True
                ).to(device)

                with torch.no_grad():
                    outputs = model(**inputs)
                    embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy().tolist()[0]

                # 2?¨ê³„: ExaOne?¼ë¡œ ?°ì´??ë¶„ì„
                analysis_prompt = (
                    f"?¤ìŒ ê²½ê¸° ?¼ì • ?°ì´?°ë? ë¶„ì„?˜ê³  ì£¼ìš” ?¹ì§•, ê²½ê¸° ?•ë³´ë¥??”ì•½?´ì£¼?¸ìš”:\n\n{data_text}"
                )
                llm = self._load_exaone_model()
                exaone_result = llm.invoke(f"[ì§ˆë¬¸] {analysis_prompt}\n[?µë?] ")

                if "[?µë?]" in exaone_result:
                    exaone_result = exaone_result.split("[?µë?]")[-1].strip()

                logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ê²½ê¸° ?¼ì • ?°ì´??ë¶„ì„ ?„ë£Œ")

                return {
                    "success": True,
                    "schedule_data": schedule_data,
                    "koelectra_embedding": {
                        "dimension": len(embedding),
                        "sample": embedding[:10]
                    },
                    "exaone_analysis": exaone_result,
                    "summary": {
                        "embedding_dim": len(embedding),
                        "analysis_length": len(exaone_result)
                    }
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ê²½ê¸° ?¼ì • ?°ì´??ë¶„ì„ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e),
                    "schedule_data": schedule_data
                }

        @self.mcp.tool()
        async def analyze_stadium_with_models(stadium_data: Dict[str, Any]) -> Dict[str, Any]:
            """KoELECTRA?€ ExaOne???¬ìš©?˜ì—¬ ê²½ê¸°???°ì´?°ë? ì¢…í•© ë¶„ì„?©ë‹ˆ??"""
            try:
                logger.info(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ê²½ê¸°???°ì´??ë¶„ì„ ?œìž‘: {stadium_data.get('stadium_name', 'Unknown')}")

                data_text = json.dumps(stadium_data, ensure_ascii=False, indent=2)

                # 1?¨ê³„: KoELECTRAë¡??°ì´???„ë² ??                model, tokenizer = self._load_koelectra_model()
                device = "cuda" if torch.cuda.is_available() else "cpu"
                inputs = tokenizer(
                    data_text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512,
                    padding=True
                ).to(device)

                with torch.no_grad():
                    outputs = model(**inputs)
                    embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy().tolist()[0]

                # 2?¨ê³„: ExaOne?¼ë¡œ ?°ì´??ë¶„ì„
                analysis_prompt = (
                    f"?¤ìŒ ê²½ê¸°???°ì´?°ë? ë¶„ì„?˜ê³  ì£¼ìš” ?¹ì§•, ?˜ìš© ?¸ì›, ?„ì¹˜ ?•ë³´ë¥??”ì•½?´ì£¼?¸ìš”:\n\n{data_text}"
                )
                llm = self._load_exaone_model()
                exaone_result = llm.invoke(f"[ì§ˆë¬¸] {analysis_prompt}\n[?µë?] ")

                if "[?µë?]" in exaone_result:
                    exaone_result = exaone_result.split("[?µë?]")[-1].strip()

                logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ê²½ê¸°???°ì´??ë¶„ì„ ?„ë£Œ")

                return {
                    "success": True,
                    "stadium_data": stadium_data,
                    "koelectra_embedding": {
                        "dimension": len(embedding),
                        "sample": embedding[:10]
                    },
                    "exaone_analysis": exaone_result,
                    "summary": {
                        "embedding_dim": len(embedding),
                        "analysis_length": len(exaone_result)
                    }
                }
            except Exception as e:
                logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ê²½ê¸°???°ì´??ë¶„ì„ ?¤íŒ¨: {e}", exc_info=True)
                return {
                    "success": False,
                    "error": str(e),
                    "stadium_data": stadium_data
                }

        # ???±ë¡
        self._tools["koelectra_to_exaone_pipeline"] = koelectra_to_exaone_pipeline
        self._tools["analyze_player_with_models"] = analyze_player_with_models
        self._tools["analyze_team_with_models"] = analyze_team_with_models
        self._tools["analyze_schedule_with_models"] = analyze_schedule_with_models
        self._tools["analyze_stadium_with_models"] = analyze_stadium_with_models

        logger.info("[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ?µí•© ???¤ì • ?„ë£Œ (KoELECTRA + ExaOne)")

    def get_mcp_server(self) -> FastMCP:
        """MCP ?œë²„ ?¸ìŠ¤?´ìŠ¤ë¥?ë°˜í™˜?©ë‹ˆ??"""
        return self.mcp

    async def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """?´ì„ ?¸ì¶œ?©ë‹ˆ??(?´ë¼?´ì–¸?¸ìš©)."""
        if tool_name not in self._tools:
            return {
                "success": False,
                "error": f"?´ì„ ì°¾ì„ ???†ìŠµ?ˆë‹¤: {tool_name}"
            }

        try:
            tool_func = self._tools[tool_name]
            # async ?¨ìˆ˜?¸ì? ?•ì¸
            import inspect
            if inspect.iscoroutinefunction(tool_func):
                result = await tool_func(**kwargs)
            else:
                result = tool_func(**kwargs)
            return result
        except Exception as e:
            logger.error(f"[ì¶•êµ¬ ì¤‘ì•™ MCP ?œë²„] ???¸ì¶œ ?¤íŒ¨: {tool_name}, {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }


# ?„ì—­ ?±ê????¸ìŠ¤?´ìŠ¤
_soccer_central_mcp_server: Optional[SoccerCentralMCPServer] = None


def get_soccer_central_mcp_server() -> SoccerCentralMCPServer:
    """ì¶•êµ¬ ?„ë©”??ì¤‘ì•™ MCP ?œë²„ ?±ê????¸ìŠ¤?´ìŠ¤ë¥?ë°˜í™˜?©ë‹ˆ??"""
    global _soccer_central_mcp_server
    if _soccer_central_mcp_server is None:
        _soccer_central_mcp_server = SoccerCentralMCPServer()
    return _soccer_central_mcp_server

