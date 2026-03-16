"""
Google Document AI ?„ëµ
?„ê¸°ì²??¬í•¨, ?¤êµ­???¼í•©, êµ¬ê? ?´ë¼?°ë“œ ?ì½”?œìŠ¤???°ë™???„ìš”??ê²½ìš° ?¬ìš©?©ë‹ˆ??
"""
from labzang.shared.strategies.pdf_strategy import PDFExtractionStrategy


class GoogleDocumentStrategy(PDFExtractionStrategy):
    """Google Document AIë¥??¬ìš©??PDF ?ìŠ¤??ì¶”ì¶œ ?„ëµ

    ?¬ìš© ?¬ë?:
    - ?„ê¸°ì²´ê? ?¬í•¨??ë¬¸ì„œ
    - ?¤êµ­?´ê? ?¼í•©??ë¬¸ì„œ
    - êµ¬ê? ?´ë¼?°ë“œ ?ì½”?œìŠ¤?œê³¼ ?°ë™???„ìš”??ê²½ìš°
    """

    def extract(self, file_path: str) -> str:
        """Google Document AIë¥??¬ìš©?˜ì—¬ PDF?ì„œ ?ìŠ¤?¸ë? ì¶”ì¶œ?©ë‹ˆ??

        Args:
            file_path: PDF ?Œì¼ ê²½ë¡œ

        Returns:
            ì¶”ì¶œ???ìŠ¤??        """
        # TODO: Google Document AI êµ¬í˜„
        # from google.cloud import documentai
        # client = documentai.DocumentProcessorServiceClient()
        # with open(file_path, 'rb') as f:
        #     raw_document = documentai.RawDocument(content=f.read(), mime_type='application/pdf')
        #     request = documentai.ProcessRequest(name=processor_name, raw_document=raw_document)
        #     result = client.process_document(request=request)
        #     return result.document.text

        return "Google Document AIë¡?ì¶”ì¶œ???ìŠ¤??

