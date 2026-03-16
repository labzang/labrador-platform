"""
PDF ì¶”ì¶œ ?„ëžµ Enum
KoELECTRA ëª¨ë¸??? íƒ???ˆì´ë¸”ì— ?°ë¼ ?ì ˆ???„ëžµ??ë§¤í•‘?©ë‹ˆ??
"""
from enum import Enum
from typing import Type
from labzang.shared.strategies.pdf_strategy import PDFExtractionStrategy


class PDFStrategyType(Enum):
    """PDF ì¶”ì¶œ ?„ëžµ ?€??Enum

    KoELECTRA ëª¨ë¸??ì¶œë ¥ ?ˆì´ë¸?0-6)ê³?ë§¤í•‘?©ë‹ˆ??
    """
    PY_MU_PDF = 0
    PDF_PLUMBER = 1
    PDF_MINER_SIX = 2
    PY_PDF = 3
    LLAMA_PARSE = 4
    AWS_TEXTRACT = 5
    GOOGLE_DOCUMENT = 6

    @classmethod
    def from_label(cls, label: int) -> "PDFStrategyType":
        """?ˆì´ë¸?ë²ˆí˜¸ë¡œë???PDFStrategyType??ë°˜í™˜?©ë‹ˆ??

        Args:
            label: KoELECTRA ëª¨ë¸??ì¶œë ¥???ˆì´ë¸?(0-6)

        Returns:
            PDFStrategyType enum ê°?
        Raises:
            ValueError: ? íš¨?˜ì? ?Šì? ?ˆì´ë¸”ì¸ ê²½ìš°
        """
        try:
            return cls(label)
        except ValueError:
            raise ValueError(f"? íš¨?˜ì? ?Šì? ?ˆì´ë¸”ìž…?ˆë‹¤: {label}. 0-6 ?¬ì´??ê°’ì„ ?…ë ¥?˜ì„¸??")

    def get_strategy_class(self) -> Type[PDFExtractionStrategy]:
        """??Enum ê°’ì— ?´ë‹¹?˜ëŠ” ?„ëžµ ?´ëž˜?¤ë? ?™ì ?¼ë¡œ ë¡œë“œ?˜ì—¬ ë°˜í™˜?©ë‹ˆ??

        Returns:
            PDFExtractionStrategyë¥?êµ¬í˜„???„ëžµ ?´ëž˜??        """
        from labzang.shared.strategy_imples.pdf.py_mu_pdf import PyMuPDFStrategy
        from labzang.shared.strategy_imples.pdf.pdf_plumber import PDFPlumberStrategy
        from labzang.shared.strategy_imples.pdf.pdf_miner_six import PDFMinerSixStrategy
        from labzang.shared.strategy_imples.pdf.py_pdf import PyPDFStrategy
        from labzang.shared.strategy_imples.pdf.llama_parse import LlamaParseStrategy
        from labzang.shared.strategy_imples.pdf.aws_textract import AWSTextractStrategy
        from labzang.shared.strategy_imples.pdf.google_document import GoogleDocumentStrategy

        strategy_map = {
            PDFStrategyType.PY_MU_PDF: PyMuPDFStrategy,
            PDFStrategyType.PDF_PLUMBER: PDFPlumberStrategy,
            PDFStrategyType.PDF_MINER_SIX: PDFMinerSixStrategy,
            PDFStrategyType.PY_PDF: PyPDFStrategy,
            PDFStrategyType.LLAMA_PARSE: LlamaParseStrategy,
            PDFStrategyType.AWS_TEXTRACT: AWSTextractStrategy,
            PDFStrategyType.GOOGLE_DOCUMENT: GoogleDocumentStrategy,
        }

        return strategy_map[self]

    def get_strategy_name(self) -> str:
        """?„ëžµ???´ë¦„??ë°˜í™˜?©ë‹ˆ??"""
        name_map = {
            PDFStrategyType.PY_MU_PDF: "PyMuPDF",
            PDFStrategyType.PDF_PLUMBER: "PDFPlumber",
            PDFStrategyType.PDF_MINER_SIX: "PDFMinerSix",
            PDFStrategyType.PY_PDF: "PyPDF",
            PDFStrategyType.LLAMA_PARSE: "LlamaParse",
            PDFStrategyType.AWS_TEXTRACT: "AWSTextract",
            PDFStrategyType.GOOGLE_DOCUMENT: "GoogleDocument",
        }
        return name_map[self]

